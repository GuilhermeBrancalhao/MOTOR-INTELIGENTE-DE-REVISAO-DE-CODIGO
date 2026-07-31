#!/usr/bin/env python3
"""Hook PostToolUse do ENGINE.

Contrato (confirmado na documentação oficial do Claude Code, hooks.md, via
subagente `claude-code-guide`): o evento chega em JSON no STDIN com, entre
outras chaves, `tool_name`, `tool_input`, `tool_response`/`tool_output` e `cwd` —
as mesmas chaves de entrada que `PreToolUse` usa (`engine_risco.py`), porque o
próprio Claude Code monta o payload de forma consistente entre os eventos de
ferramenta. A diferença central de `PostToolUse` é que a ferramenta **já
executou** quando o hook roda: não existe mais "bloquear a ação", só o que o
Claude vê depois (stdout JSON estruturado com `decision`/`hookSpecificOutput`,
ou stderr com a saída 2). Este hook não usa nada disso — ele só observa e grava.

Por isso a política de saída aqui é a mais simples possível: **sempre sai 0**.
Não há decisão a bloquear (a ação já aconteceu) e não há conveniência a
proteger feito o cartão do `UserPromptSubmit` — só um registro acessório. Se o
registro falhar, o hook não pode fazer o turno parecer quebrado por causa de
uma trilha que não gravou; a ação em si sempre valeu.

Falha segura: qualquer erro em qualquer ponto do caminho — stdin ilegível,
estado corrompido, classificador com exceção, gravação da trilha — sai 0 sem
propagar. O único jeito de este hook não gravar uma linha é o motor estar
desligado (aí ele deliberadamente não tem nada a registrar).
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from _comum import forcar_utf8, raiz_do_ciclo  # noqa: E402

# Ver `_comum.forcar_utf8`: sem isso, acento na trilha sai como mojibake no
# console do Windows.
forcar_utf8()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import config, estado, risco, trilha  # noqa: E402


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


#: Marcas de que a ação registrada é uma invocação da PRÓPRIA CLI do ENGINE.
#: Comparadas contra o texto normalizado (barras para frente, minúsculas), porque no
#: Windows o comando chega com barra invertida (`ferramentas\cli.py`).
_MARCAS_DO_MOTOR = ("ferramentas/cli.py", "ferramentas.cli")


def _e_do_motor(tool_input: dict, alvo: str) -> bool:
    """Diz se a ação é uma chamada à CLI do próprio ENGINE.

    Existe por causa do buraco central do gate (`hooks/engine_gate.py`): o único
    jeito de entrar em BUILD/TESTE/REVISAO é rodar `cli.py fase BUILD` por um
    comando de shell — e esse comando dispara este hook, que gravava na trilha uma
    linha JÁ com `fase: BUILD`. A partir daí o gate sempre achava "ação da fase" e
    nunca cobrava evidência de nada. Evidência de uma fase não pode ser satisfeita
    pela própria chamada que mudou para essa fase.
    """
    candidatos = [alvo, tool_input.get("command")]
    for texto in candidatos:
        if not isinstance(texto, str):
            continue
        normalizado = texto.replace("\\", "/").lower()
        if any(marca in normalizado for marca in _MARCAS_DO_MOTOR):
            return True
    return False


def _alvo(tool_name: str, tool_input: dict) -> str:
    """Extrai um alvo textual legível da ação, para a coluna `alvo` da trilha.

    Ferramenta de arquivo: o caminho. Ferramenta de comando: o comando cru.
    Sem um campo reconhecido (ferramenta não mapeada, ou entrada vazia), o
    próprio nome da ferramenta já é melhor do que uma linha em branco.
    """
    for chave in ("file_path", "notebook_path", "path", "pattern"):
        valor = tool_input.get(chave)
        if valor:
            return str(valor)
    comando = tool_input.get("command")
    if comando:
        return str(comando)
    return tool_name


def principal() -> int:
    # Rede de segurança de nível externo: este hook roda depois que a ação já
    # aconteceu, então não há nada a proteger bloqueando — só o registro é
    # acessório, e ele nunca pode fazer o processo sair com código != 0.
    try:
        try:
            evento = json.load(sys.stdin)
        except Exception:  # noqa: BLE001
            return 0

        if not isinstance(evento, dict):
            return 0

        tool_name = evento.get("tool_name")
        if not isinstance(tool_name, str) or not tool_name:
            return 0

        tool_input = evento.get("tool_input")
        if not isinstance(tool_input, dict):
            tool_input = {}

        raiz = raiz_do_ciclo(Path(evento.get("cwd") or "."))

        dados = estado.carregar(raiz)
        if not dados or not dados.get("ativo"):
            return 0

        try:
            cfg = config.carregar(raiz)
            veredito = risco.classificar(tool_name, tool_input, raiz=raiz, config=cfg)
        except Exception:  # noqa: BLE001
            return 0

        alvo = _alvo(tool_name, tool_input)
        entrada = {
            "quando": _agora(),
            "fase": dados.get("fase", "?"),
            "ferramenta": tool_name,
            "alvo": alvo,
            "risco": veredito.nivel,
            "regra": veredito.regra,
            # Sem o id do ciclo na linha, `novo_ciclo` zerava o estado mas não a
            # trilha, e o relatório do ciclo 2 contava as ações do ciclo 1 como se
            # fossem suas. A separação por ciclo tem de estar no DADO, não na
            # esperança de que alguém apague o arquivo entre um ciclo e outro.
            "ciclo": str((dados.get("ciclo") or {}).get("id") or ""),
        }
        if _e_do_motor(tool_input, alvo):
            # Chave presente só quando é verdadeira: mantém a linha enxuta e deixa
            # `linha.get("do_motor")` valer como "ação de trabalho de verdade?".
            entrada["do_motor"] = True
        trilha.registrar(raiz, entrada)
        return 0
    except Exception:  # noqa: BLE001
        return 0


if __name__ == "__main__":
    sys.exit(principal())
