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
        r"|\bcurl\b[^\n]*\s(-d|--data|--data-raw|--data-binary)\b"
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

_INERTE = re.compile(r"^\s*(echo|printf|:|#)\b", re.I)
_MSG_GIT = re.compile(r"(-m|--message)\s+('[^']*'|\"[^\"]*\")")
_REDIRECT = re.compile(r">>?\s*([^\s;|&]+)")
_EXEC_INDIRETA = re.compile(
    r"\b(bash|sh|zsh)\s+-c\s|\bpowershell(\.exe)?\s+(-Command|-c)\s|\beval\s", re.I
)
_PY_INLINE = re.compile(r"\bpython[0-9.]*\s+-c\s", re.I)
_PY_PERIGO = re.compile(
    r"shutil\.rmtree|os\.remove|os\.unlink|os\.rmdir|subprocess"
    r"|requests\.(post|put|delete|patch)|urlopen",
    re.I,
)

_LEITURA = {"Read", "Glob", "Grep", "NotebookRead"}
_ESCRITA = {"Write", "Edit", "NotebookEdit"}
_COMANDO = {"Bash", "PowerShell"}


def classificar(ferramenta: str, entrada: dict, *, raiz: Path, config: dict) -> Classificacao:
    """Classifica uma ação. Qualquer exceção vira TRAVADO (falha segura)."""
    try:
        if ferramenta in _LEITURA:
            return _classificar_leitura(entrada, config)
        if ferramenta in _ESCRITA:
            return _classificar_escrita(entrada, config)
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


def _classificar_leitura(entrada: dict, config: dict) -> Classificacao:
    alvo = str(
        entrada.get("file_path") or entrada.get("path") or entrada.get("pattern") or ""
    )
    if _e_segredo(alvo, config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {Path(alvo).name}")
    return Classificacao(LIVRE, "", "leitura")


def _classificar_escrita(entrada: dict, config: dict) -> Classificacao:
    alvo = str(entrada.get("file_path") or entrada.get("notebook_path") or "")
    if not alvo:
        return Classificacao(RASTREADO, "", "escrita sem alvo identificável")
    if _e_segredo(alvo, config):
        return Classificacao(TRAVADO, "R5", f"arquivo de segredo: {Path(alvo).name}")
    caminho = Path(alvo)
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


def _classificar_comando(comando: str, config: dict) -> Classificacao:
    if not comando.strip():
        return Classificacao(LIVRE, "", "comando vazio")
    resultado = Classificacao(LIVRE, "", "nenhuma regra travada casou")
    for segmento in _dividir_segmentos(comando):
        resultado = _pior(resultado, _classificar_segmento(segmento, config))
    return resultado


def _classificar_segmento(segmento: str, config: dict) -> Classificacao:
    for alvo in _REDIRECT.findall(segmento):
        if _e_segredo(alvo, config):
            return Classificacao(TRAVADO, "R5", f"redirecionamento para segredo: {alvo}")

    if _INERTE.match(segmento):
        return Classificacao(LIVRE, "", "emissor inerte")

    limpo = _MSG_GIT.sub(" ", segmento) if re.match(r"\s*git\b", segmento) else segmento

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
        return Classificacao(RASTREADO, "R8", "execução indireta")

    return Classificacao(LIVRE, "", "comando sem regra travada")


def _familias(config: dict) -> tuple[tuple[str, str, str], ...]:
    extras = tuple(
        (item["regra"], item["motivo"], item["padrao"])
        for item in config.get("travado_extra", [])
    )
    return FAMILIAS + extras
