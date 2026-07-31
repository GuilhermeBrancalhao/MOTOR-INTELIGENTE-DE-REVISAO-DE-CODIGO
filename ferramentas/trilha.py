"""Trilha auditável do ENGINE: registro append-only de ações em `<projeto>/.engine/trilha.jsonl`.

Uma linha por ação, cada uma um objeto JSON isolado (formato JSON Lines). É a fonte
de verdade para idempotência e para os relatórios de fase/ciclo (`ferramentas.relatorio`,
F2-T3) — nunca o índice de uma API externa, nunca o contador em memória de um hook.

`registrar` é ACESSÓRIO: chamado de dentro do hook `PostToolUse` (`hooks/engine_trilha.py`)
depois que a ferramenta já executou. Uma falha aqui (disco cheio, diretório sem
permissão, corrida com outro processo) não pode derrubar o turno do usuário — por isso
`registrar` nunca propaga exceção, only best-effort.

`ler` é tolerante a corrupção: uma linha malformada (JSON inválido, ou JSON válido que
não é objeto) é pulada e vira um aviso em `_avisos`, nunca interrompe a leitura das
linhas boas nem derruba quem chama.

**A trilha nunca guarda credencial em claro.** O `alvo` de uma ação de comando é o
comando CRU — e comando cru carrega segredo com frequência (`psql
"postgresql://user:senha@host/db"`, `curl -H "Authorization: Bearer …"`). Esses
comandos são `rastreado` pela política de risco (executam, não travam), então sem
redação eles iam literais para o disco e voltavam ao contexto no relatório de fase e
no verbo `retomar`. `redigir` roda dentro de `registrar`: o dado nunca chega ao
disco em claro. Quem imprime a trilha aplica `redigir` de novo, por defesa em
profundidade — trilha gravada antes desta correção continua em claro no arquivo.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from ferramentas import risco

#: O que aparece no lugar do trecho redigido. Um marcador visível, não uma máscara
#: de asteriscos: quem lê o relatório precisa saber que houve supressão ali.
MARCA_REDIGIDO = "«redigido»"

#: Senha embutida em URL (`esquema://usuario:senha@host`). O usuário é preservado
#: (é o que identifica a conexão no relatório); só a senha some.
_URL_COM_SENHA = re.compile(r"([A-Za-z][A-Za-z0-9+.\-]*://[^\s:/@]+:)([^\s@/]+)(@)")

#: Valor de um cabeçalho `Authorization:` — em `-H "Authorization: Bearer sk-proj-…"`
#: ou solto. O valor termina na aspa que fecha o argumento, ou no fim da linha.
#: Existe além de `_PADROES_CREDENCIAL` porque o token portado por esse cabeçalho
#: quase nunca tem prefixo reconhecível (`sk-proj-…` não casa `sk-[A-Za-z0-9]{16,}`).
_CABECALHO_AUTORIZACAO = re.compile(r"(authorization\s*:\s*)([^\"'\n]+)", re.I)


def caminho(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "trilha.jsonl"


def redigir(texto: str) -> str:
    """Substitui por `MARCA_REDIGIDO` todo trecho que pareça uma credencial.

    Três fontes de padrão, nesta ordem:

    1. valor de cabeçalho `Authorization:` (o mais abrangente — engole o token
       inteiro, seja qual for a forma dele);
    2. senha em URL (`esquema://usuario:senha@host`);
    3. os padrões de chave conhecida de `ferramentas/risco.py` (`sk-`, `ghp_`,
       `github_pat_`, `AKIA`, `xox…`, JWT, `BEGIN … PRIVATE KEY`).

    O item 3 vem do módulo de risco de propósito, por referência e não por cópia:
    `risco.py` é política selada da Fase 1 e é a fonte única do que conta como
    credencial. Duas listas iguais em dois arquivos divergem na primeira vez que
    uma delas ganha um padrão novo.
    """
    if not isinstance(texto, str) or not texto:
        return texto
    saida = _CABECALHO_AUTORIZACAO.sub(lambda casa: casa.group(1) + MARCA_REDIGIDO, texto)
    saida = _URL_COM_SENHA.sub(
        lambda casa: casa.group(1) + MARCA_REDIGIDO + casa.group(3), saida
    )
    return risco._PADROES_CREDENCIAL.sub(MARCA_REDIGIDO, saida)


def _entrada_redigida(entrada: dict) -> dict:
    """Aplica `redigir` a todo valor de texto da entrada, preservando o resto.

    Redige a entrada inteira, não só `alvo`: o campo que carrega o comando cru hoje
    é `alvo`, mas um campo novo com texto de ação amanhã herdaria a proteção sem
    ninguém precisar lembrar dela.
    """
    if not isinstance(entrada, dict):
        return entrada
    return {
        chave: redigir(valor) if isinstance(valor, str) else valor
        for chave, valor in entrada.items()
    }


def registrar(raiz: Path, entrada: dict) -> None:
    """Faz append de `entrada` como uma linha JSON em `caminho(raiz)`.

    Cria `.engine/` se preciso. Qualquer erro (permissão, disco cheio, caminho
    inválido) é silenciado: registrar é acessório, a ação já aconteceu e não pode
    ser desfeita só porque a trilha não pôde ser gravada.

    O que vai para o disco é a entrada REDIGIDA — ver `redigir`.
    """
    try:
        alvo = caminho(raiz)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        linha = json.dumps(_entrada_redigida(entrada), ensure_ascii=False)
        with alvo.open("a", encoding="utf-8") as arquivo:
            arquivo.write(linha + "\n")
    except Exception:  # noqa: BLE001 — registrar é acessório, nunca propaga
        pass


def ler(raiz: Path) -> dict:
    """Lê a trilha inteira. Arquivo ausente devolve listas vazias, nunca levanta.

    Cada linha corrompida (JSON inválido, ou JSON válido que não é objeto) é pulada
    e vira um aviso em `_avisos` com o número da linha (1-based); as linhas boas ao
    redor continuam sendo lidas normalmente. Linha em branco é ignorada em silêncio
    (não é corrupção, é só um separador supérfluo).
    """
    alvo = caminho(raiz)
    linhas: list[dict] = []
    avisos: list[str] = []
    if not alvo.is_file():
        return {"linhas": linhas, "_avisos": avisos}

    try:
        texto = alvo.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as erro:
        avisos.append(f"trilha ilegível ({erro.__class__.__name__}): {erro}")
        return {"linhas": linhas, "_avisos": avisos}

    for numero, bruta in enumerate(texto.splitlines(), start=1):
        if not bruta.strip():
            continue
        try:
            item = json.loads(bruta)
        except json.JSONDecodeError:
            avisos.append(f"linha {numero} da trilha ilegível (JSON inválido); ignorada")
            continue
        if not isinstance(item, dict):
            avisos.append(f"linha {numero} da trilha ilegível (não é um objeto JSON); ignorada")
            continue
        linhas.append(item)

    return {"linhas": linhas, "_avisos": avisos}
