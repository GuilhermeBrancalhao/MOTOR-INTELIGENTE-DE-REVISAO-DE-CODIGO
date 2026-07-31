"""Utilidades compartilhadas entre os hooks do ENGINE.

Dois problemas valem para qualquer hook do plugin, não só para o que os resolveu
primeiro (`engine_risco.py`, PreToolUse):

1. Sem forçar UTF-8 nos fluxos padrão, acentuação em mensagens de hook sai como
   mojibake no console do Windows (cp1252 por padrão) — e essa mensagem é o que o
   Claude ou o usuário lê para decidir o que fazer, então ilegível é o mesmo que
   nenhuma mensagem.
2. O `cwd` do evento pode ser um subdiretório do projeto (ex.: dentro de um
   pacote); sem subir a árvore até achar `.engine/estado.json`, o hook não acha o
   estado e o motor aparenta desligado — indistinguível de "motor realmente
   desligado", então a proteção cai sem ninguém notar.

Módulo sem dependência de `ferramentas` de propósito: os hooks importam isto antes
de qualquer outra coisa, inclusive antes de ajustar `sys.path` para achar o pacote
`ferramentas`.
"""
from __future__ import annotations

import sys
from pathlib import Path

#: Limite de níveis que `raiz_do_ciclo` sobe procurando `.engine/estado.json`.
#: Evita um loop sem fim num caminho patológico (link simbólico circular etc.).
LIMITE_NIVEIS_RAIZ = 30


def forcar_utf8() -> None:
    """Reconfigura stdin/stdout/stderr para UTF-8.

    `reconfigure` pode não existir (stream substituído por algo sem esse método,
    comum em teste) ou recusar o encoding; nos dois casos seguimos com o stream
    original em vez de travar o hook por causa disso.
    """
    for fluxo in (sys.stdin, sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def raiz_do_ciclo(inicio: Path) -> Path:
    """Sobe a árvore de diretórios a partir de `inicio` até achar `.engine/estado.json`.

    O Claude Code roda o hook com `cwd` igual ao diretório de trabalho corrente da
    sessão, que pode ser um subdiretório do projeto. `estado.carregar` só olha
    `<raiz>/.engine/estado.json` — sem subir a árvore, o hook não acha o estado.

    Sobe no máximo `LIMITE_NIVEIS_RAIZ` níveis. Se não achar nada, devolve `inicio`.
    """
    atual = Path(inicio)
    for _ in range(LIMITE_NIVEIS_RAIZ):
        if (atual / ".engine" / "estado.json").is_file():
            return atual
        pai = atual.parent
        if pai == atual:
            break
        atual = pai
    return Path(inicio)
