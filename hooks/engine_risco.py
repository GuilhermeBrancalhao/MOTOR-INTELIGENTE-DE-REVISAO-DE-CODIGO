#!/usr/bin/env python3
"""Hook PreToolUse do ENGINE.

Contrato (confirmado na documentação oficial do Claude Code, hooks.md):
o evento chega em JSON no STDIN com, entre outras chaves, `tool_name`,
`tool_input` e `cwd`. A saída do processo comunica a decisão:
  saída 0  -> a ação segue
  saída 2  -> a ação é bloqueada; o stderr explica o motivo a Claude/ao usuário

Falha segura: qualquer erro no caminho de decisão bloqueia. A única exceção é o motor
desligado — aí o hook não tem opinião sobre nada.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import config, estado, risco  # noqa: E402


def principal() -> int:
    try:
        evento = json.load(sys.stdin)
    except Exception:  # noqa: BLE001
        print("ENGINE: evento do hook ilegível; bloqueando por segurança", file=sys.stderr)
        return 2

    raiz = Path(evento.get("cwd") or ".")

    dados = estado.carregar(raiz)
    if not dados or not dados.get("ativo"):
        return 0

    try:
        cfg = config.carregar(raiz)
        veredito = risco.classificar(
            evento.get("tool_name", ""),
            evento.get("tool_input") or {},
            raiz=raiz,
            config=cfg,
        )
    except Exception as erro:  # noqa: BLE001
        print(
            f"ENGINE: falha ao classificar ({erro}); bloqueando por segurança",
            file=sys.stderr,
        )
        return 2

    if dados.get("ciclo", {}).get("modo") == "dry" and veredito.nivel != risco.LIVRE:
        print("ENGINE [modo seco]: nenhuma escrita é executada neste ciclo", file=sys.stderr)
        return 2

    if veredito.nivel == risco.TRAVADO:
        print(
            f"ENGINE [{veredito.regra}] ação travada: {veredito.motivo}.\n"
            f"Apresente ao usuário o que pretende fazer e o impacto, e peça confirmação "
            f"com opções clicáveis antes de tentar de novo.",
            file=sys.stderr,
        )
        return 2

    if veredito.nivel == risco.RASTREADO:
        alvo = (evento.get("tool_input") or {}).get("file_path")
        if alvo:
            try:
                estado.registrar_diff(raiz, alvo)
            except Exception:  # noqa: BLE001
                pass  # registrar é acessório; não pode bloquear ação já liberada
    return 0


if __name__ == "__main__":
    sys.exit(principal())
