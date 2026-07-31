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

**Só o ciclo corrente entra.** `estado.novo_ciclo` zera o estado mas não a trilha
(que é append-only por contrato), então sem filtro o relatório do ciclo 2 contava as
ações do ciclo 1 — número errado, não só verboso. Cada linha da trilha carrega hoje
o `ciclo` que a gerou (`hooks/engine_trilha.py`) e o relatório fica com as do ciclo
atual, dizendo quantas ignorou.

**Teto duro de saída.** Um relatório é lido DENTRO do contexto do modelo. Uma trilha
de 50 mil linhas virava 3,1 MB impressos e 23 s de montagem; o custo não é estético,
é o contexto inteiro do turno. Nenhum relatório passa de `TETO_LINHAS` linhas: ao
exceder, a listagem de ações é cortada e o relatório diz quantas ficaram de fora.
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

#: Teto duro de linhas de QUALQUER relatório. Ver o docstring do módulo.
TETO_LINHAS = 300


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


def _id_do_ciclo(dados: dict | None) -> str:
    """Id do ciclo corrente, ou string vazia quando não há estado/ciclo legível."""
    if not isinstance(dados, dict):
        return ""
    ciclo = dados.get("ciclo")
    if not isinstance(ciclo, dict):
        return ""
    return str(ciclo.get("id") or "")


def _do_ciclo_corrente(linhas: list, id_ciclo: str) -> tuple[list[dict], int]:
    """Filtra as linhas da trilha pelo ciclo corrente.

    Devolve `(linhas do ciclo, quantas foram ignoradas por não terem id de ciclo)`.

    Uma linha SEM `ciclo` é anterior a esta correção. Quando a trilha inteira é
    assim (nenhuma linha carimbada), não há como separar ciclo nenhum e descartar
    tudo faria o relatório dizer "nenhuma ação" sobre uma trilha cheia — pior que o
    problema original. Nesse caso ela é contada inteira. Assim que aparece ao menos
    uma linha carimbada, a trilha é posterior à correção: aí vale o filtro estrito,
    e as linhas sem id são ignoradas e reportadas.
    """
    objetos = [linha for linha in linhas if isinstance(linha, dict)]
    if not id_ciclo:
        return objetos, 0
    if not any(item.get("ciclo") for item in objetos):
        return objetos, 0
    do_ciclo = [item for item in objetos if str(item.get("ciclo") or "") == id_ciclo]
    ignoradas = sum(1 for item in objetos if not item.get("ciclo"))
    return do_ciclo, ignoradas


def _nota_de_ignoradas(ignoradas: int) -> list[str]:
    if ignoradas <= 0:
        return []
    return [
        f"_({ignoradas} ação(ões) sem id de ciclo — trilha anterior à separação por "
        f"ciclo — foram ignoradas neste relatório.)_"
    ]


def _cortar_no_teto(cabecalho: list[str], itens: list[str], rodape: list[str]) -> list[str]:
    """Monta o relatório mantendo o total dentro de `TETO_LINHAS`.

    Só a listagem de ações (`itens`) é cortada — cabeçalho e rodapé carregam o que o
    leitor precisa para entender o corte (objetivo, fase, pendências). Se nem assim
    couber, `_garantir_teto` faz o corte final.
    """
    orcamento = TETO_LINHAS - len(cabecalho) - len(rodape)
    if len(itens) <= orcamento:
        return cabecalho + itens + rodape
    manter = max(orcamento - 1, 0)
    omitidas = len(itens) - manter
    nota = f"... {omitidas} ação(ões) omitida(s) (teto de {TETO_LINHAS} linhas do relatório)."
    return cabecalho + itens[:manter] + [nota] + rodape


def _garantir_teto(linhas: list[str]) -> list[str]:
    """Rede final: nem um rodapé gigante (muitos diffs/pendências) passa do teto."""
    if len(linhas) <= TETO_LINHAS:
        return linhas
    omitidas = len(linhas) - (TETO_LINHAS - 1)
    return linhas[: TETO_LINHAS - 1] + [
        f"... relatório cortado no teto de {TETO_LINHAS} linhas ({omitidas} linhas omitidas)."
    ]


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
    """Alvos distintos das ações de escrita, na ordem em que apareceram na trilha.

    `dict` em vez de `list` para o "já vi este alvo?": a busca linear anterior
    (`alvo not in vistos`) era O(n²) e, numa trilha de 50 mil linhas, dominava os
    23 s de montagem do relatório. `dict` preserva a ordem de inserção desde o
    Python 3.7, então a ordem de aparição continua a mesma.
    """
    vistos: dict[str, None] = {}
    for linha in linhas:
        if not isinstance(linha, dict):
            continue
        if linha.get("ferramenta") not in FERRAMENTAS_ESCRITA:
            continue
        alvo = linha.get("alvo")
        if alvo:
            vistos.setdefault(trilha.redigir(str(alvo)), None)
    return list(vistos)


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
        cabecalho = [
            "# Relatório de ciclo",
            "",
            f"**Ciclo:** {ciclo.get('id', '(sem id)')}",
            f"**Objetivo:** {ciclo.get('objetivo', '(nenhum)')}",
            f"**Fase atual:** {dados.get('fase', '?')}",
            f"**Fases concluídas:** "
            f"{', '.join(dados.get('fases_concluidas') or []) or '(nenhuma)'}",
            "",
        ]
        cabecalho += _secao_decisoes(dados)
        cabecalho.append("")

        dados_trilha = _carregar_trilha_segura(raiz)
        linhas_trilha, ignoradas = _do_ciclo_corrente(
            dados_trilha.get("linhas") or [], _id_do_ciclo(dados)
        )

        cabecalho.append("## Ações por nível")
        cabecalho.append("")
        itens: list[str] = []
        if not linhas_trilha:
            cabecalho.append(SEM_ACAO_NA_TRILHA)
            cabecalho += _nota_de_ignoradas(ignoradas)
        else:
            contagem = _contagem_por_nivel(linhas_trilha)
            for nivel in NIVEIS:
                cabecalho.append(f"- {nivel}: {contagem[nivel]}")
            cabecalho += _nota_de_ignoradas(ignoradas)
            cabecalho.append("")
            cabecalho.append("## Arquivos tocados")
            cabecalho.append("")
            arquivos = _arquivos_tocados(linhas_trilha)
            if arquivos:
                itens = [f"- {arquivo}" for arquivo in arquivos]
            else:
                cabecalho.append("(nenhum arquivo de escrita registrado)")

        rodape = [""]
        rodape += _secao_diffs(dados)
        rodape.append("")
        rodape += _secao_pendencias(dados)

        avisos = _secao_avisos_trilha(dados_trilha)
        if avisos:
            rodape.append("")
            rodape += avisos

        return "\n".join(_garantir_teto(_cortar_no_teto(cabecalho, itens, rodape)))
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
        do_ciclo, ignoradas = _do_ciclo_corrente(
            dados_trilha.get("linhas") or [], _id_do_ciclo(dados)
        )
        linhas_da_fase = [
            item
            for item in do_ciclo
            if str(item.get("fase", "")).upper() == fase_normalizada
        ]

        titulo = fase_normalizada or "(fase não informada)"
        cabecalho = [f"# Relatório da fase {titulo}", "", "## Ações", ""]
        itens: list[str] = []
        if not linhas_da_fase:
            cabecalho.append(f"Nenhuma ação registrada na fase {titulo}.")
        else:
            for item in linhas_da_fase:
                quando = item.get("quando", "?")
                ferramenta = item.get("ferramenta", "?")
                # Defesa em profundidade: `registrar` já redige antes do disco, mas
                # uma trilha gravada antes desta correção ainda tem segredo em claro
                # no arquivo — e é este print que devolve o texto ao contexto.
                alvo = trilha.redigir(str(item.get("alvo", "?")))
                nivel = item.get("risco", "?")
                itens.append(f"- {quando} · {ferramenta} · {alvo} · {nivel}")
        cabecalho += _nota_de_ignoradas(ignoradas)

        rodape = [""]
        rodape += _secao_diffs(dados)
        rodape.append("")
        rodape += _secao_pendencias(dados)

        avisos = _secao_avisos_trilha(dados_trilha)
        if avisos:
            rodape.append("")
            rodape += avisos

        return "\n".join(_garantir_teto(_cortar_no_teto(cabecalho, itens, rodape)))
    except Exception:  # noqa: BLE001 — rede de segurança final, nunca levanta
        return FALHA_AO_MONTAR
