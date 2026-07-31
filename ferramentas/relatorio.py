"""Relatórios de ciclo e de fase do ENGINE, montados a partir do estado e da trilha.

Nunca inventa números: contagens por nível e arquivos tocados vêm sempre de
`trilha.ler` (F2-T2); objetivo, fases, decisões, diffs pendentes e pendências vêm
sempre de `estado.carregar` (Fase 1). Sem trilha, a seção de ações diz isso; sem
estado, o relatório de ciclo diz que o motor nunca ligou neste projeto — nenhum dos
dois casos gera um número inventado.

`de_ciclo` e `de_fase` NUNCA levantam exceção: estado ausente, corrompido, trilha
corrompida ou argumento estranho (fase `None`, tipo errado) degradam para texto
honesto. `estado.carregar` e `trilha.ler` já são tolerantes por conta própria; a
rede de segurança extra aqui (`_carregar_estado_seguro`/`_carregar_trilha_segura` e
o `try/except` de nível externo em cada função pública) cobre o resto — por exemplo
`raiz` que não converte para `Path`.
"""
from __future__ import annotations

from pathlib import Path

from ferramentas import estado, trilha

#: Ordem fixa de exibição das contagens — sempre as três, mesmo quando zero.
NIVEIS: tuple[str, ...] = ("livre", "rastreado", "travado")

#: Mesmas ferramentas de escrita que `risco._ESCRITA` classifica (Write/Edit/
#: NotebookEdit); repetido aqui (não importado) porque é um detalhe de LEITURA da
#: trilha, não de classificação — os dois módulos não precisam ficar acoplados.
FERRAMENTAS_ESCRITA: frozenset[str] = frozenset({"Write", "Edit", "NotebookEdit"})

MOTOR_NUNCA_LIGOU = "ENGINE: motor nunca ligou neste projeto (sem `.engine/estado.json`)."
SEM_ACAO_NA_TRILHA = "Nenhuma ação registrada (trilha ausente ou vazia)."
FALHA_AO_MONTAR = "ENGINE: não foi possível montar o relatório a partir do estado atual."


def _carregar_estado_seguro(raiz: Path) -> dict | None:
    """`estado.carregar` já devolve `None` para ausente/corrompido; isto só blinda
    contra um `raiz` que nem vira `Path` (ex.: `None`)."""
    try:
        return estado.carregar(Path(raiz))
    except Exception:  # noqa: BLE001 — relatório nunca pode levantar
        return None


def _carregar_trilha_segura(raiz: Path) -> dict:
    """`trilha.ler` já é tolerante a corrupção; isto blinda contra `raiz` estranho
    e contra um retorno que, por algum motivo, não tenha o formato esperado."""
    try:
        dados = trilha.ler(Path(raiz))
        if isinstance(dados, dict) and isinstance(dados.get("linhas"), list):
            dados.setdefault("_avisos", [])
            return dados
    except Exception:  # noqa: BLE001 — relatório nunca pode levantar
        pass
    return {"linhas": [], "_avisos": []}


def _contagem_por_nivel(linhas: list[dict]) -> dict[str, int]:
    contagem = {nivel: 0 for nivel in NIVEIS}
    for linha in linhas:
        if not isinstance(linha, dict):
            continue
        nivel = linha.get("risco")
        if nivel in contagem:
            contagem[nivel] += 1
    return contagem


def _arquivos_tocados(linhas: list[dict]) -> list[str]:
    """Alvos distintos das ações de escrita, na ordem em que apareceram na trilha."""
    vistos: list[str] = []
    for linha in linhas:
        if not isinstance(linha, dict):
            continue
        if linha.get("ferramenta") not in FERRAMENTAS_ESCRITA:
            continue
        alvo = linha.get("alvo")
        if alvo and alvo not in vistos:
            vistos.append(str(alvo))
    return vistos


def _secao_decisoes(dados: dict) -> list[str]:
    decisoes = dados.get("decisoes") or []
    linhas = ["## Decisões", ""]
    if not decisoes:
        linhas.append("(nenhuma decisão registrada)")
        return linhas
    for item in decisoes:
        if not isinstance(item, dict):
            continue
        o_que = item.get("o_que", "?")
        porque = item.get("porque", "?")
        linhas.append(f"- {o_que} — {porque}")
    return linhas


def _secao_diffs(dados: dict) -> list[str]:
    diffs = dados.get("diffs_pendentes") or []
    linhas = ["## Diffs por apresentar", ""]
    if not diffs:
        linhas.append("(nenhum diff pendente)")
        return linhas
    for item in diffs:
        linhas.append(f"- {item}")
    return linhas


def _secao_pendencias(dados: dict) -> list[str]:
    pendencias = dados.get("pendencias") or []
    linhas = ["## Pendências abertas", ""]
    if not pendencias:
        linhas.append("(nenhuma pendência aberta)")
        return linhas
    for item in pendencias:
        linhas.append(f"- {item}")
    return linhas


def _secao_avisos_trilha(dados_trilha: dict) -> list[str]:
    avisos = dados_trilha.get("_avisos") or []
    if not avisos:
        return []
    linhas = ["## Avisos da trilha", ""]
    for aviso in avisos:
        linhas.append(f"- {aviso}")
    return linhas


def de_ciclo(raiz: Path) -> str:
    """Relatório em Markdown do ciclo inteiro.

    Contém: objetivo, fase atual, fases concluídas, decisões com justificativa,
    contagem de ações por nível (livre/rastreado/travado) somada da trilha, os
    arquivos distintos tocados por ações de escrita e os diffs/pendências abertos.
    Sem estado, devolve só a frase avisando que o motor nunca ligou neste projeto.
    Sem trilha (ausente ou vazia), a seção de ações diz isso em vez de mostrar
    números inventados.
    """
    try:
        dados = _carregar_estado_seguro(raiz)
        if not dados:
            return MOTOR_NUNCA_LIGOU

        ciclo = dados.get("ciclo") or {}
        linhas = [
            "# Relatório de ciclo",
            "",
            f"**Objetivo:** {ciclo.get('objetivo', '(nenhum)')}",
            f"**Fase atual:** {dados.get('fase', '?')}",
            f"**Fases concluídas:** "
            f"{', '.join(dados.get('fases_concluidas') or []) or '(nenhuma)'}",
            "",
        ]
        linhas += _secao_decisoes(dados)
        linhas.append("")

        dados_trilha = _carregar_trilha_segura(raiz)
        linhas_trilha = dados_trilha.get("linhas") or []

        linhas.append("## Ações por nível")
        linhas.append("")
        if not linhas_trilha:
            linhas.append(SEM_ACAO_NA_TRILHA)
        else:
            contagem = _contagem_por_nivel(linhas_trilha)
            for nivel in NIVEIS:
                linhas.append(f"- {nivel}: {contagem[nivel]}")
            linhas.append("")
            linhas.append("## Arquivos tocados")
            linhas.append("")
            arquivos = _arquivos_tocados(linhas_trilha)
            if arquivos:
                for arquivo in arquivos:
                    linhas.append(f"- {arquivo}")
            else:
                linhas.append("(nenhum arquivo de escrita registrado)")
        linhas.append("")

        linhas += _secao_diffs(dados)
        linhas.append("")
        linhas += _secao_pendencias(dados)

        avisos = _secao_avisos_trilha(dados_trilha)
        if avisos:
            linhas.append("")
            linhas += avisos

        return "\n".join(linhas)
    except Exception:  # noqa: BLE001 — rede de segurança final, nunca levanta
        return FALHA_AO_MONTAR


def de_fase(raiz: Path, fase: str) -> str:
    """Relatório em Markdown de uma fase específica.

    Contém uma linha por ação da trilha daquela fase (quando, ferramenta, alvo,
    nível), mais os diffs pendentes e pendências do estado atual (não filtrados
    por fase — são do ciclo inteiro). Fase sem nenhuma ação registrada diz isso
    em vez de mostrar uma lista vazia sem explicação.
    """
    try:
        fase_normalizada = str(fase or "").strip().upper()
        dados = _carregar_estado_seguro(raiz) or {}
        dados_trilha = _carregar_trilha_segura(raiz)
        linhas_da_fase = [
            item
            for item in (dados_trilha.get("linhas") or [])
            if isinstance(item, dict)
            and str(item.get("fase", "")).upper() == fase_normalizada
        ]

        titulo = fase_normalizada or "(fase não informada)"
        linhas = [f"# Relatório da fase {titulo}", "", "## Ações", ""]
        if not linhas_da_fase:
            linhas.append(f"Nenhuma ação registrada na fase {titulo}.")
        else:
            for item in linhas_da_fase:
                quando = item.get("quando", "?")
                ferramenta = item.get("ferramenta", "?")
                alvo = item.get("alvo", "?")
                nivel = item.get("risco", "?")
                linhas.append(f"- {quando} · {ferramenta} · {alvo} · {nivel}")
        linhas.append("")

        linhas += _secao_diffs(dados)
        linhas.append("")
        linhas += _secao_pendencias(dados)

        avisos = _secao_avisos_trilha(dados_trilha)
        if avisos:
            linhas.append("")
            linhas += avisos

        return "\n".join(linhas)
    except Exception:  # noqa: BLE001 — rede de segurança final, nunca levanta
        return FALHA_AO_MONTAR
