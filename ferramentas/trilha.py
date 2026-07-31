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
"""
from __future__ import annotations

import json
from pathlib import Path


def caminho(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "trilha.jsonl"


def registrar(raiz: Path, entrada: dict) -> None:
    """Faz append de `entrada` como uma linha JSON em `caminho(raiz)`.

    Cria `.engine/` se preciso. Qualquer erro (permissão, disco cheio, caminho
    inválido) é silenciado: registrar é acessório, a ação já aconteceu e não pode
    ser desfeita só porque a trilha não pôde ser gravada.
    """
    try:
        alvo = caminho(raiz)
        alvo.parent.mkdir(parents=True, exist_ok=True)
        linha = json.dumps(entrada, ensure_ascii=False)
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
