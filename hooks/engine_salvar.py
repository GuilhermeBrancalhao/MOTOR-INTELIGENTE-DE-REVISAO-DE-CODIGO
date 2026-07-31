#!/usr/bin/env python3
"""Hook PreCompact do ENGINE.

Contrato (confirmado na documentação oficial do Claude Code, hooks.md, via
subagente `claude-code-guide`): o evento chega em JSON no STDIN com, entre
outras chaves, `session_id`, `transcript_path`, `cwd`, `permission_mode`,
`hook_event_name` ("PreCompact") e `compaction_trigger` ("manual" ou "auto").
Saída 0 -> a compactação prossegue (stdout é ignorado). Saída 2 BLOQUEIA a
compactação — e bloquear a compactação nunca é o que este hook quer: ele existe
para que o motor sobreviva a ela, não para atrasá-la.

Por isso a política de saída aqui é **sempre 0**, em qualquer circunstância,
inclusive erro. O trabalho deste hook é acessório (consolidar um resumo no
estado antes que o contexto seja compactado) — se não conseguir, a compactação
segue de qualquer jeito, e o cartão de `engine_contexto.py` no próximo turno
continua funcionando a partir do que já estava salvo.

Consolidação: com o motor ligado, grava em `estado.json`:
  - `ultima_consolidacao`: data/hora ISO deste PreCompact.
  - `resumo_trilha`: contagem de ações por nível de risco (`livre`,
    `rastreado`, `travado`, ou o que aparecer), somada da trilha — não fica
    presa à sessão atual, porque a trilha é o registro de disco, não de
    contexto, mas **só do ciclo corrente** (ver `_linhas_do_ciclo_corrente`
    abaixo): mesmo defeito que `ferramentas/relatorio.py` já corrigiu para o
    relatório de ciclo — sem o filtro, `estado.novo_ciclo` zera o estado mas
    não a trilha (append-only por contrato), e a consolidação do PreCompact no
    ciclo 2 reportava números do ciclo 1.

Motor desligado, estado ausente/corrompido, ou qualquer erro no caminho: sai 0
sem gravar nada. Nunca atrapalha a compactação.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from _comum import forcar_utf8, raiz_do_ciclo  # noqa: E402

# Ver `_comum.forcar_utf8`: sem isso, acento no resumo sai como mojibake no
# console do Windows.
forcar_utf8()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import estado, relatorio, trilha  # noqa: E402


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _linhas_do_ciclo_corrente(dados: dict, trilha_dados: dict) -> list[dict]:
    """Filtra a trilha pelo ciclo corrente, reaproveitando a MESMA regra de
    `ferramentas/relatorio.py` (`_id_do_ciclo` + `_do_ciclo_corrente`) — não
    duplicada aqui, importada por referência, para não divergir se a regra de
    compatibilidade com trilha antiga (sem carimbo de `ciclo`) mudar num dos
    dois lugares e não no outro.
    """
    linhas, _ignoradas = relatorio._do_ciclo_corrente(
        trilha_dados.get("linhas") or [], relatorio._id_do_ciclo(dados)
    )
    return linhas


def _resumo_por_nivel(linhas: list[dict]) -> dict:
    """Conta as ações da trilha por nível de risco.

    Genérico de propósito: não assume os três nomes de `ferramentas.risco`
    (`livre`/`rastreado`/`travado`) — uma linha sem o campo `risco` (trilha
    antiga, ou linha corrompida que passou por algum motivo) conta como
    `"desconhecido"` em vez de quebrar a consolidação.
    """
    resumo: dict = {}
    for linha in linhas:
        nivel = linha.get("risco") if isinstance(linha, dict) else None
        chave = nivel if isinstance(nivel, str) and nivel else "desconhecido"
        resumo[chave] = resumo.get(chave, 0) + 1
    return resumo


def principal() -> int:
    # Rede de segurança de nível externo: este hook NUNCA pode bloquear a
    # compactação (saída 2) — só sabe sair 0. A consolidação é conveniência.
    try:
        try:
            evento = json.load(sys.stdin)
        except Exception:  # noqa: BLE001
            return 0

        if not isinstance(evento, dict):
            return 0

        raiz = raiz_do_ciclo(Path(evento.get("cwd") or "."))

        dados = estado.carregar(raiz)
        if not dados or not dados.get("ativo"):
            return 0

        trilha_dados = trilha.ler(raiz)
        linhas_do_ciclo = _linhas_do_ciclo_corrente(dados, trilha_dados)
        dados["ultima_consolidacao"] = _agora()
        dados["resumo_trilha"] = _resumo_por_nivel(linhas_do_ciclo)

        try:
            estado.gravar(raiz, dados)
        except Exception:  # noqa: BLE001
            pass
        return 0
    except Exception:  # noqa: BLE001
        return 0


if __name__ == "__main__":
    sys.exit(principal())
