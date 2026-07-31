#!/usr/bin/env python3
"""Hook PreToolUse do ENGINE.

Contrato (confirmado na documentação oficial do Claude Code, hooks.md):
o evento chega em JSON no STDIN com, entre outras chaves, `tool_name`,
`tool_input` e `cwd`. A saída do processo comunica a decisão:
  saída 0  -> a ação segue
  saída 2  -> a ação é bloqueada; o stderr explica o motivo a Claude/ao usuário

A saída 1 NÃO tem bloqueio garantido pelo contrato do Claude Code — para este hook
ela é tão ruim quanto liberar. Por isso `principal()` inteira roda dentro de um
único try/except de nível externo: qualquer falha não prevista no caminho de
decisão devolve 2, nunca deixa a exceção subir e virar 1.

Falha segura: qualquer erro no caminho de decisão bloqueia. A única exceção é o motor
desligado — aí o hook não tem opinião sobre nada.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _comum import forcar_utf8, raiz_do_ciclo  # noqa: E402

# Força UTF-8 nos três descritores padrão — ver `_comum.forcar_utf8` para o motivo
# (mojibake de acentuação no console do Windows) e o comportamento de falha segura.
forcar_utf8()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import config, estado, risco  # noqa: E402

#: Ferramentas de escrita. Em modo seco, TODA chamada a uma delas é bloqueada,
#: mesmo quando `risco.classificar` devolve LIVRE (arquivo novo, ou sob `tests/`) —
#: "nenhuma escrita é executada neste ciclo" vale para a ferramenta usada, não só
#: para o nível de risco. Sem essa checagem por ferramenta, `Write` num arquivo novo
#: passava direto em modo seco: LIVRE é o mesmo nível que uma leitura, e o gate
#: antigo (`veredito.nivel != risco.LIVRE`) não distinguia as duas coisas.
_FERRAMENTAS_ESCRITA = {"Write", "Edit", "NotebookEdit"}


def principal() -> int:
    # Rede de segurança de nível externo (CRÍTICO 1): qualquer entrada, por mais
    # malformada, tem que sair 0 ou 2 — nunca 1. Os `try/except` internos abaixo
    # cobrem os casos esperados com mensagens específicas; este envolve o caminho
    # inteiro para pegar o que sobrar (ex.: `cwd` que não é string, e por isso
    # derruba `Path(...)` antes de qualquer try interno).
    try:
        try:
            evento = json.load(sys.stdin)
        except Exception:  # noqa: BLE001
            print("ENGINE: evento do hook ilegível; bloqueando por segurança", file=sys.stderr)
            return 2

        if not isinstance(evento, dict):
            # `null`, `[]`, `"texto"` etc. decodificam como JSON válido mas não são
            # o objeto de evento que o contrato promete — tratar como ilegível.
            print("ENGINE: evento do hook ilegível; bloqueando por segurança", file=sys.stderr)
            return 2

        tool_name = evento.get("tool_name")
        if not isinstance(tool_name, str) or not tool_name:
            # O contrato do hook (hooks.md) promete `tool_name` como string não vazia
            # em todo evento PreToolUse. Sem ele não há o que classificar — e não é
            # o mesmo caso do "ferramenta desconhecida" (que `risco.classificar` trata
            # como RASTREADO de propósito): aqui o próprio evento está quebrado.
            print(
                "ENGINE: evento do hook ilegível (tool_name ausente); bloqueando por segurança",
                file=sys.stderr,
            )
            return 2

        tool_input = evento.get("tool_input")
        if tool_input is not None and not isinstance(tool_input, dict):
            # `tool_input` como string (ou qualquer coisa que não seja objeto) não é
            # um formato do contrato: sem bloquear aqui, o `.get` mais abaixo (na
            # ramificação RASTREADO) estourava DEPOIS que a decisão já tinha sido
            # tomada — o bug original saía 1 em vez de 0/2 exatamente por isso.
            print(
                "ENGINE: evento do hook ilegível (tool_input não é objeto); "
                "bloqueando por segurança",
                file=sys.stderr,
            )
            return 2
        if tool_input is None:
            # Omitir `tool_input` é uma forma válida e comum do contrato (ferramenta
            # sem argumentos) — normaliza para vazio, não bloqueia.
            tool_input = {}

        raiz = raiz_do_ciclo(Path(evento.get("cwd") or "."))

        dados = estado.carregar(raiz)
        if not dados or not dados.get("ativo"):
            return 0

        try:
            cfg = config.carregar(raiz)
            veredito = risco.classificar(
                tool_name,
                tool_input,
                raiz=raiz,
                config=cfg,
            )
        except Exception as erro:  # noqa: BLE001
            print(
                f"ENGINE: falha ao classificar ({erro}); bloqueando por segurança",
                file=sys.stderr,
            )
            return 2

        eh_ferramenta_de_escrita = tool_name in _FERRAMENTAS_ESCRITA
        if dados.get("ciclo", {}).get("modo") == "dry" and (
            eh_ferramenta_de_escrita or veredito.nivel != risco.LIVRE
        ):
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
            alvo = tool_input.get("file_path")
            if alvo:
                try:
                    estado.registrar_diff(raiz, alvo)
                except Exception:  # noqa: BLE001
                    pass  # registrar é acessório; não pode bloquear ação já liberada
        return 0
    except Exception as erro:  # noqa: BLE001
        print(f"ENGINE: falha inesperada ({erro}); bloqueando por segurança", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(principal())
