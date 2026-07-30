"""Classificador de risco do ENGINE.

Regra de ouro: na dúvida, TRAVADO. Este módulo nunca libera por falha.

As famílias são casadas sobre o comando CRU, de propósito: SQL perigoso quase sempre
chega dentro de aspas (`psql -c "DROP TABLE x"`), então limpar literais antes de casar
cegaria justamente a família mais cara. A proteção contra falso positivo é estreita e
explícita: emissores inertes (`echo`, `printf`) e o texto de `-m` do git.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

LIVRE = "livre"
RASTREADO = "rastreado"
TRAVADO = "travado"

_ORDEM = {LIVRE: 0, RASTREADO: 1, TRAVADO: 2}


@dataclass(frozen=True)
class Classificacao:
    nivel: str
    regra: str
    motivo: str


FAMILIAS: tuple[tuple[str, str, str], ...] = (
    (
        "R1",
        "escrita de rede",
        r"\bcurl\b[^\n]*\s-X\s*(POST|PUT|PATCH|DELETE)\b"
        r"|\bcurl\b[^\n]*\s--request\s+(POST|PUT|PATCH|DELETE)\b"
        r"|\bcurl\b[^\n]*\s(-d|--data|--data-raw|--data-binary)\b"
        r"|\bcurl\b[^\n]*\s(--upload-file|-T)\b"
        r"|\bwget\b[^\n]*--post",
    ),
    (
        "R2",
        "git que sai da máquina ou reescreve história",
        r"\bgit\s+(push|rebase)\b"
        r"|\bgit\s+reset\s+--hard\b"
        r"|\bgit\s+clean\s+-[a-zA-Z]*f"
        r"|\bgit\s+checkout\s+--\s",
    ),
    (
        "R3",
        "deleção",
        r"(^|[\s;|&])(rm|rmdir|del|erase)\s|\bRemove-Item\b",
    ),
    (
        "R4",
        "alteração destrutiva de banco",
        r"\b(DROP|TRUNCATE)\s+(TABLE|DATABASE|SCHEMA)\b"
        r"|\bALTER\s+TABLE\b"
        r"|\bDELETE\s+FROM\b(?![^;\"']*\bWHERE\b)"
        r"|\b(alembic|flyway|liquibase)\b[^\n]*\b(upgrade|migrate)\b"
        r"|\bmanage\.py\s+migrate\b",
    ),
    (
        "R6",
        "deploy ou infraestrutura",
        r"\bdocker\s+push\b"
        r"|\bkubectl\s+apply\b"
        r"|\bterraform\s+apply\b"
        r"|\bgh\s+workflow\s+run\b"
        r"|\bnpm\s+publish\b"
        r"|\btwine\s+upload\b",
    ),
    (
        "R7",
        "instalação global",
        r"\bnpm\s+(i|install)\b[^\n]*\s-g\b"
        r"|\bpip[0-9.]*\s+install\b"
        r"|\bwinget\s+install\b"
        r"|\bchoco\s+install\b",
    ),
)

_INERTE = re.compile(r"^\s*(echo|printf|#)\b", re.I)
_MSG_GIT = re.compile(r"(-m|--message)\s+('[^']*'|\"[^\"]*\")")
_SUBST_COMANDO = re.compile(r"\$\(|`|\$\{")
_REDIRECT = re.compile(r">>?\s*([^\s;|&]+)")
_EXEC_INDIRETA = re.compile(
    r"\b(bash|sh|zsh)\s+-c\s|\bpowershell(\.exe)?\s+(-Command|-c)\s|\beval\s", re.I
)
_CANO_INTERPRETE = re.compile(
    r"\|\s*(sudo\s+)?"
    r"(bash|sh|zsh|ksh|python[0-9.]*|perl|ruby|node"
    r"|powershell(\.exe)?|iex|invoke-expression)\b",
    re.I,
)
_PY_INLINE = re.compile(r"\bpython[0-9.]*\s+-c\s", re.I)
_PY_PERIGO = re.compile(
    r"shutil\.rmtree|shutil\.move|os\.remove|os\.unlink|os\.rmdir|subprocess"
    r"|requests\.(post|put|delete|patch)|urlopen"
    r"|os\.system|os\.popen|os\.exec\w*|os\.spawn\w*"
    r"|\beval\(|\bexec\(|Path\(.*\)\.unlink",
    re.I,
)

_LEITURA = {"Read", "Glob", "Grep", "NotebookRead"}
_ESCRITA = {"Write", "Edit", "NotebookEdit"}
_COMANDO = {"Bash", "PowerShell"}


def classificar(ferramenta: str, entrada: dict, *, raiz: Path, config: dict) -> Classificacao:
    """Classifica uma ação. Qualquer exceção vira TRAVADO (falha segura)."""
    try:
        if ferramenta in _LEITURA:
            return _classificar_leitura(entrada, raiz, config)
        if ferramenta in _ESCRITA:
            return _classificar_escrita(entrada, raiz, config)
        if ferramenta in _COMANDO:
            return _classificar_comando(str(entrada.get("command", "")), config)
        return Classificacao(RASTREADO, "", f"ferramenta não classificada: {ferramenta}")
    except Exception as erro:  # noqa: BLE001 — falha segura é o requisito
        return Classificacao(
            TRAVADO,
            "R0",
            f"classificador falhou ({erro.__class__.__name__}); travando por segurança",
        )


def _pior(a: Classificacao, b: Classificacao) -> Classificacao:
    return b if _ORDEM[b.nivel] > _ORDEM[a.nivel] else a


def _e_segredo(alvo: str, config: dict) -> bool:
    if not alvo:
        return False
    caminho = Path(alvo)
    nome = caminho.name
    inteiro = caminho.as_posix()
    for padrao in config.get("padroes_segredo", []):
        if fnmatch(nome, padrao) or fnmatch(inteiro, f"*{padrao}"):
            return True
    return False


def _resolver_alvo(alvo: str, raiz: Path) -> Path:
    """Resolve um alvo relativo contra a raiz do projeto hospedeiro.

    Caminho absoluto passa direto — o comportamento para esse caso fica idêntico
    ao de antes. Caminho relativo (`.env`, `src/x.py`) hoje é checado contra o
    diretório de trabalho do processo, que pode não ser o projeto hospedeiro; sem
    isso, a checagem de segredo/existência mira no lugar errado.
    """
    caminho = Path(alvo)
    if caminho.is_absolute():
        return caminho
    return raiz / caminho


def _classificar_leitura(entrada: dict, raiz: Path, config: dict) -> Classificacao:
    alvo = str(
        entrada.get("file_path") or entrada.get("path") or entrada.get("pattern") or ""
    )
    if not alvo:
        return Classificacao(LIVRE, "", "leitura")
    caminho = _resolver_alvo(alvo, raiz)
    if _e_segredo(caminho.as_posix(), config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {caminho.name}")
    return Classificacao(LIVRE, "", "leitura")


def _classificar_escrita(entrada: dict, raiz: Path, config: dict) -> Classificacao:
    alvo = str(entrada.get("file_path") or entrada.get("notebook_path") or "")
    if not alvo:
        return Classificacao(RASTREADO, "", "escrita sem alvo identificável")
    caminho = _resolver_alvo(alvo, raiz)
    if _e_segredo(caminho.as_posix(), config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {caminho.name}")
    if "tests" in caminho.parts or caminho.name.startswith("test_"):
        return Classificacao(LIVRE, "", "arquivo de teste")
    if caminho.exists():
        return Classificacao(RASTREADO, "", "arquivo já existe em disco")
    return Classificacao(LIVRE, "", "arquivo novo")


def _dividir_segmentos(comando: str) -> list[str]:
    """Divide o comando nos separadores de shell (`&&`, `||`, `;`, `|`), mas nunca
    dentro de aspas simples ou duplas.

    Um separador dentro de aspas não encadeia comandos: é conteúdo literal, como o
    `;` em `python -c "import shutil; shutil.rmtree('x')"`. Dividir ali cegava a
    checagem de `python -c` perigoso — a expressão nunca aparecia inteira em um único
    segmento.
    """
    segmentos: list[str] = []
    atual: list[str] = []
    aspas: str | None = None
    i = 0
    n = len(comando)
    while i < n:
        ch = comando[i]
        if aspas:
            atual.append(ch)
            if ch == aspas:
                aspas = None
            i += 1
            continue
        if ch in ("'", '"'):
            aspas = ch
            atual.append(ch)
            i += 1
            continue
        if comando[i : i + 2] in ("&&", "||"):
            segmentos.append("".join(atual))
            atual = []
            i += 2
            continue
        if ch in (";", "|"):
            segmentos.append("".join(atual))
            atual = []
            i += 1
            continue
        atual.append(ch)
        i += 1
    segmentos.append("".join(atual))
    return segmentos


_LIMITE_PROFUNDIDADE_INDIRETA = 3


def _classificar_comando(comando: str, config: dict, profundidade: int = 0) -> Classificacao:
    if not comando.strip():
        return Classificacao(LIVRE, "", "comando vazio")
    if _CANO_INTERPRETE.search(comando):
        # Checagem sobre o comando INTEIRO, antes de dividir em segmentos: dividir
        # primeiro quebra `curl ... | bash` em "curl ..." de um lado e "bash" do
        # outro, e nenhum dos dois pedaços isolados casa nenhuma família — o "baixar
        # e executar" só aparece quando os dois lados são vistos juntos.
        return Classificacao(
            TRAVADO, "R8", "cano para interpretador (baixar e executar)"
        )
    resultado = Classificacao(LIVRE, "", "nenhuma regra travada casou")
    for segmento in _dividir_segmentos(comando):
        resultado = _pior(resultado, _classificar_segmento(segmento, config, profundidade))
    return resultado


def _classificar_segmento(segmento: str, config: dict, profundidade: int = 0) -> Classificacao:
    for alvo_cru in _REDIRECT.findall(segmento):
        # O alvo pode vir entre aspas (`> ".env"`): tira as aspas antes de comparar
        # com os padrões de segredo, senão o fnmatch nunca casa e o redirecionamento
        # sai LIVRE por engano.
        alvo = alvo_cru.strip("'\"")
        if _e_segredo(alvo, config):
            return Classificacao(TRAVADO, "R5", f"redirecionamento para segredo: {alvo}")

    if _INERTE.match(segmento):
        if _SUBST_COMANDO.search(segmento):
            # A válvula do emissor inerte só pode valer para texto LITERAL. `echo`/
            # `printf` seguido de `$(...)`, crase ou `${...}` não imprime texto: o
            # shell expande e executa o comando escondido antes do "echo" rodar —
            # mesmo tratamento que já existe para o `-m` do git.
            return Classificacao(
                TRAVADO, "R8", "substituição de comando dentro do argumento"
            )
        return Classificacao(LIVRE, "", "emissor inerte")

    eh_git = re.match(r"\s*git\b", segmento)
    if eh_git:
        msg = _MSG_GIT.search(segmento)
        if msg and _SUBST_COMANDO.search(msg.group(2)):
            # A válvula de falso positivo do `-m` só vale para texto literal. Se o
            # argumento contém `$(`, crase ou `${`, é substituição de comando —
            # `git commit -m "$(rm -rf /dados)"` executaria o comando escondido.
            return Classificacao(
                TRAVADO, "R8", "substituição de comando dentro do argumento"
            )
        limpo = _MSG_GIT.sub(" ", segmento)
    else:
        limpo = segmento

    for regra, motivo, padrao in _familias(config):
        if re.search(padrao, limpo, re.I):
            return Classificacao(TRAVADO, regra, motivo)

    if _PY_INLINE.search(segmento):
        if _PY_PERIGO.search(segmento):
            return Classificacao(TRAVADO, "R8", "python -c com chamada perigosa")
        return Classificacao(
            RASTREADO, "R8", "python -c: conteúdo não inspecionável a fundo"
        )

    if _EXEC_INDIRETA.search(segmento):
        return _classificar_execucao_indireta(segmento, config, profundidade)

    return Classificacao(LIVRE, "", "comando sem regra travada")


def _classificar_execucao_indireta(
    segmento: str, config: dict, profundidade: int
) -> Classificacao:
    """Extrai o payload entre aspas de uma execução indireta e reclassifica-o.

    `bash -c "rm -rf x"` não pode sair RASTREADO só por reconhecer a superfície
    do padrão: o comando real mora dentro das aspas. Sem extrair e reclassificar
    esse literal recursivamente, um `rm` disfarçado de `bash -c` escaparia — foi
    exatamente esse escape que motivou (erradamente) alargar a âncora de R3 no
    lugar de tratar a execução indireta de verdade.
    """
    if profundidade >= _LIMITE_PROFUNDIDADE_INDIRETA:
        return Classificacao(
            TRAVADO, "R8", "aninhamento de subcomando além do limite"
        )

    casamento = _EXEC_INDIRETA.search(segmento)
    payload = _extrair_payload_indireto(segmento[casamento.end() :])
    if payload is None:
        return Classificacao(
            TRAVADO, "R8", "execução indireta sem payload legível"
        )

    resultado_payload = _classificar_comando(payload, config, profundidade + 1)
    resultado_segmento = Classificacao(RASTREADO, "R8", "execução indireta")
    return _pior(resultado_segmento, resultado_payload)


def _extrair_payload_indireto(resto: str) -> str | None:
    """Devolve o literal entre aspas (simples ou duplas) logo após o disparador
    de execução indireta, ou `None` se não houver aspas para extrair."""
    casamento = re.search(r"(['\"])(.*)\1", resto, re.S)
    if not casamento:
        return None
    return casamento.group(2)


def _familias(config: dict) -> tuple[tuple[str, str, str], ...]:
    extras = tuple(
        (item["regra"], item["motivo"], item["padrao"])
        for item in config.get("travado_extra", [])
    )
    return FAMILIAS + extras
