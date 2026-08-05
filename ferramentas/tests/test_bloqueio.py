"""Testes da regra de bloqueio (C3) e da persistência da descoberta no estado.

Convenção da suíte: cada docstring nomeia **a mutação que derrubaria o teste**. Aqui
isso é o próprio critério de aceite do ciclo — as três mutações `_b1_muda_lacunas_ativas
-> False`, `_b2_universal -> False` e `_b3_impede_aceite -> False` têm de derrubar, cada
uma, ao menos um teste que a nomeia. Por isso existem três testes com um predicado
isolado cada: um teste que só olhasse `bloqueantes_abertas` no catálogo real passaria
com dois dos três predicados mortos, porque as lacunas universais disparam B2 e B3 ao
mesmo tempo.

O que este arquivo prova, além disso: que confiança do modelo e peso da lacuna **não**
são critério de bloqueio, e que lacuna assumível sai como decisão aberta com a pergunta
inteira — nunca como valor preenchido.
"""
from __future__ import annotations

import json

import pytest

from ferramentas import descoberta, estado
from ferramentas.elicitacao import (
    CATALOGO,
    PARTES_DO_ACEITE,
    BloqueioInvalido,
    Contexto,
    DecisaoAberta,
    Intencao,
    Lacuna,
    LacunaDesconhecida,
    Origem,
    ParteDoAceite,
    Plataforma,
    Predicado,
    assumiveis_abertas,
    avaliar_lacuna,
    bloqueantes_abertas,
    lacunas_do_pedido,
    universo_completo,
    validar_bloqueio,
)
from ferramentas.elicitacao.bloqueio import (
    _b1_muda_lacunas_ativas,
    _b2_universal,
    _b3_impede_aceite,
)

POR_ID: dict[str, Lacuna] = {lacuna.id: lacuna for lacuna in CATALOGO}

#: Catálogo sintético de duas lacunas para isolar B1. `tem_cobranca` não é universal
#: (B2 falso), não fornece pedaço de aceite (B3 falso) e tem peso 3 — o mais baixo que
#: o catálogo aceita como "vale pouco". Só o que sobra é B1: responder "LOJA_PAGAMENTOS"
#: faz `pag_estorno_sintetica` passar a existir, e responder "não cobra nada" não.
_GATILHO = Lacuna(
    id="tem_cobranca_sintetica",
    pergunta="Isto cobra dinheiro de alguém, ou não toca em pagamento?",
    porque="Existe só para provar que uma resposta pode abrir outras perguntas.",
    peso=3,
    universal=False,
    plataformas=frozenset({Plataforma.WEB}),
    opcoes=("LOJA_PAGAMENTOS", "nao toca em pagamento"),
)
_DESTRAVADA = Lacuna(
    id="pag_estorno_sintetica",
    pergunta="Como se devolve o dinheiro quando a cobrança sai errada?",
    porque="Existe só para ser a pergunta que aparece quando a de cima é respondida.",
    peso=6,
    universal=False,
    contextos=frozenset({Contexto.LOJA_PAGAMENTOS}),
)
_UNIVERSO_SINTETICO = (_GATILHO, _DESTRAVADA)


# --- (1) As três mutações do aceite, uma por predicado -------------------


def test_b1_lacuna_que_abre_outras_perguntas_bloqueia_sozinha():
    """Derrubaria este teste: `_b1_muda_lacunas_ativas` devolver `False` sempre.

    É a mutação B1 do aceite deste ciclo, e o teste está montado para que **só** B1
    possa salvá-lo: `tem_cobranca_sintetica` não é universal, não fornece pedaço nenhum
    do critério de aceite e tem peso 3. Se ela deixar de bloquear, a entrevista segue
    por um ramo escolhido no escuro — e a pergunta de estorno, que só existe se a
    resposta for "cobra", nunca é feita nem listada.

    Também derrubaria: medir a mudança sobre as lacunas já ativas em vez do universo
    completo. Com `LOJA_PAGAMENTOS` ainda não confirmado, `pag_estorno_sintetica` não
    está ativa — e é justamente a que a resposta faria aparecer.
    """
    assert not _b2_universal(_GATILHO), "o teste perde o sentido se ela virar universal"
    assert not _b3_impede_aceite(_GATILHO), "o teste perde o sentido se ela entrar no aceite"

    assert _b1_muda_lacunas_ativas(
        _GATILHO, plataformas=[Plataforma.WEB], universo=_UNIVERSO_SINTETICO
    )

    veredito = avaliar_lacuna(
        _GATILHO, plataformas=[Plataforma.WEB], universo=_UNIVERSO_SINTETICO
    )
    assert veredito.bloqueante
    assert veredito.predicados == (Predicado.B1_MUDA_LACUNAS,)

    travadas = {
        decisao.id
        for decisao in bloqueantes_abertas(
            [_GATILHO], plataformas=[Plataforma.WEB], universo=_UNIVERSO_SINTETICO
        )
    }
    assert travadas == {"tem_cobranca_sintetica"}


def test_b1_no_catalogo_real_so_dispara_para_onde_roda():
    """Derrubaria este teste: `_b1_muda_lacunas_ativas` devolver `False` sempre — ou `True` sempre.

    A mesma mutação B1, agora contra o catálogo publicado, e com a metade que impede o
    conserto preguiçoso: `onde_roda` é a única lacuna do catálogo cuja resposta muda
    quais outras existem (está escrito no `porque` dela), e nenhuma outra pode disparar
    B1. Um predicado que devolvesse `True` sempre passaria na primeira asserção e cairia
    na segunda, que é o ponto — bloquear tudo é o interrogatório de novo.
    """
    assert _b1_muda_lacunas_ativas(POR_ID["onde_roda"])

    for identificador in ("problema", "sucesso", "web_autenticacao", "mobile_loja"):
        assert not _b1_muda_lacunas_ativas(
            POR_ID[identificador], plataformas=[Plataforma.WEB, Plataforma.MOBILE]
        ), f"{identificador} não muda o conjunto de lacunas e não pode disparar B1"


def test_b2_lacuna_universal_bloqueia_mesmo_com_peso_baixo():
    """Derrubaria este teste: `_b2_universal` devolver `False` sempre.

    É a mutação B2 do aceite. `fora_de_escopo` é universal e vale 7 — abaixo de várias
    condicionais que não bloqueiam —, e `usuario` é universal sem pedaço de aceite. Nas
    duas, B1 é falso e B3 é falso, então só B2 as sustenta: se ele morrer, o motor passa
    a planejar sem saber para quem o software é e sem o que ficou de fora, que são as
    duas ausências que nenhum caso torna aceitável.
    """
    for identificador in ("usuario", "fora_de_escopo"):
        lacuna = POR_ID[identificador]
        assert not _b1_muda_lacunas_ativas(lacuna)
        assert not _b3_impede_aceite(lacuna)
        assert _b2_universal(lacuna)

        veredito = avaliar_lacuna(lacuna)
        assert veredito.predicados == (Predicado.B2_UNIVERSAL,), identificador
        assert veredito.bloqueante


def test_b3_lacuna_sem_a_qual_nao_se_escreve_aceite_bloqueia():
    """Derrubaria este teste: `_b3_impede_aceite` devolver `False` sempre.

    É a mutação B3 do aceite. `perf_medicao_atual` e `perf_meta` são condicionais (B2
    falso), sem opções (B1 falso) e são a linha de base e o limiar de um pedido de
    otimização: sem elas não existe critério falsificável nenhum — "ficou mais rápido"
    não reprova ninguém. Se B3 morrer, as duas somem da lista de bloqueantes e o plano
    de otimização é aprovado sem número, que é o defeito que o motor `otimizar-performance`
    inteiro existe para impedir.
    """
    universo = universo_completo(Intencao.OTIMIZAR)
    abertas = lacunas_do_pedido("Está lento, dá timeout.", [Plataforma.WEB], [])

    travadas = {
        decisao.id
        for decisao in bloqueantes_abertas(
            abertas, plataformas=[Plataforma.WEB], universo=universo
        )
    }
    assert {"perf_medicao_atual", "perf_meta"} <= travadas

    por_id = {lacuna.id: lacuna for lacuna in abertas}
    for identificador in ("perf_medicao_atual", "perf_meta"):
        lacuna = por_id[identificador]
        assert not _b1_muda_lacunas_ativas(lacuna, universo=universo)
        assert not _b2_universal(lacuna)
        assert _b3_impede_aceite(lacuna)
        assert avaliar_lacuna(lacuna, universo=universo).predicados == (
            Predicado.B3_IMPEDE_ACEITE,
        ), identificador


def test_b3_deixa_de_bloquear_quando_outra_resposta_ja_deu_o_mesmo_pedaco():
    """Derrubaria este teste: B3 virar lista fixa de ids obrigatórios.

    O que B3 pergunta é se **falta** um pedaço do critério, e não se aquela pergunta
    está numa lista. `sucesso` e `perf_meta` fornecem o mesmo pedaço — o limiar —, e com
    o limiar já respondido a segunda deixa de travar o plano: continua valendo a pena
    perguntar, e é por isso que ela permanece como decisão aberta, mas o aceite já se
    escreve. Sem esta propriedade, responder a entrevista nunca destravaria o gate do
    C4 por completo.
    """
    perf_meta = {lacuna.id: lacuna for lacuna in lacunas_do_pedido("", [], [], intencao=Intencao.OTIMIZAR)}[
        "perf_meta"
    ]
    assert _b3_impede_aceite(perf_meta)
    assert not _b3_impede_aceite(perf_meta, respondidas=["sucesso"])
    assert _b3_impede_aceite(perf_meta, respondidas=["problema"]), (
        "`problema` é SUJEITO, não LIMIAR: responder um pedaço não cobre o outro"
    )


# --- (2) Os dois critérios que a regra proíbe ----------------------------


def test_peso_nao_e_criterio_de_bloqueio():
    """Derrubaria este teste: trocar os predicados por `lacuna.peso >= limiar`.

    Esta é a confusão que transforma o gate em "pergunte tudo acima de 7". A prova é
    exaustiva de propósito: **nenhum** dos dez limiares possíveis reproduz a partição
    que os predicados produzem. Se um dia reproduzir, ou os predicados viraram peso
    disfarçado, ou o catálogo perdeu a variedade que torna a regra necessária.
    """
    universo = universo_completo(Intencao.EVOLUIR)
    abertas = lacunas_do_pedido(
        "", [Plataforma.WEB], [], intencao=Intencao.EVOLUIR
    )
    decisoes = {
        decisao.id: decisao
        for decisao in bloqueantes_abertas(abertas, plataformas=[Plataforma.WEB], universo=universo)
    }
    travadas = set(decisoes)
    por_id = {lacuna.id: lacuna for lacuna in abertas}

    for limiar in range(1, 11):
        por_peso = {i for i, lacuna in por_id.items() if lacuna.peso >= limiar}
        assert por_peso != travadas, (
            f"a partição por peso >= {limiar} coincidiu com a dos predicados: "
            "o gate virou limiar de peso disfarçado"
        )

    pesada_e_assumivel = [
        lacuna.id for lacuna in por_id.values() if lacuna.peso >= 9 and lacuna.id not in travadas
    ]
    leve_e_bloqueante = [
        lacuna.id for lacuna in por_id.values() if lacuna.peso <= 7 and lacuna.id in travadas
    ]
    assert pesada_e_assumivel, "esperava lacuna de peso alto que não bloqueia"
    assert leve_e_bloqueante, "esperava lacuna de peso baixo que bloqueia"


def test_confianca_nao_entra_na_decisao_de_bloqueio():
    """Derrubaria este teste: ler `Palpite.confianca` dentro de `bloqueio.py`.

    No caso medido pelo acervo, a inferência de confiança BAIXA era a certa e as de
    ALTA/MÉDIA erraram — confiança é resultado, não critério. A prova é dupla: o
    **código executável** do módulo não menciona confiança em lugar nenhum (a varredura
    é por `ast`, com os docstrings removidos, porque a documentação precisa falar da
    proibição para explicá-la), e dois estados idênticos a menos das confianças dos
    palpites produzem exatamente a mesma lista de bloqueantes.
    """
    import ast
    from pathlib import Path

    from ferramentas.elicitacao import bloqueio

    arvore = ast.parse(Path(bloqueio.__file__).read_text(encoding="utf-8"))
    for no in ast.walk(arvore):
        corpo_do_no = getattr(no, "body", None)
        if isinstance(no, (ast.Module, ast.ClassDef, ast.FunctionDef)) and ast.get_docstring(no):
            no.body = corpo_do_no[1:]
    codigo = ast.unparse(arvore).lower().replace("ç", "c")

    assert "lacunas_ativas" in codigo, "a varredura não está vendo o código do módulo"
    assert "confianc" not in codigo, (
        "o código de bloqueio.py menciona confiança: confiança ordena a conversa de "
        "confirmação, não decide o que trava o plano"
    )

    def _com_confianca(rotulo: str) -> dict:
        return {
            descoberta.CHAVE: {
                "versao": descoberta.VERSAO_BLOCO,
                "pedido": "Está lento, dá timeout no navegador.",
                "intencao": "OTIMIZAR",
                "plataformas": ["WEB"],
                "contextos": [],
                "respostas": {},
                "palpites_pendentes": [
                    {"valor": "WEB", "evidencia": "no navegador", "confianca": rotulo}
                ],
                "registrado_em": "2026-08-05T10:00:00",
                "atualizado_em": "2026-08-05T10:00:00",
            }
        }

    alta = descoberta.avaliar(_com_confianca("ALTA"))
    baixa = descoberta.avaliar(_com_confianca("BAIXA"))
    assert [d.id for d in alta.bloqueantes] == [d.id for d in baixa.bloqueantes]
    assert [d.predicados for d in alta.abertas] == [d.predicados for d in baixa.abertas]


# --- (3) Assumível é decisão aberta, nunca valor preenchido --------------


def test_assumivel_sai_como_pergunta_inteira_e_nunca_como_valor():
    """Derrubaria este teste: dar um campo de valor (ou um padrão) à `DecisaoAberta`.

    Assumível quer dizer "o motor segue sem perguntar", e não "o motor decide no lugar
    de alguém e não conta". A classe não tem campo de valor — nem `None`, nem `""`, nem
    "a definir" —, porque campo vazio é preenchido por alguém em algum momento e a
    suposição passa a viajar com a autoridade de uma resposta. O que sai é a pergunta
    literal do catálogo e o motivo dela.
    """
    campos = {campo for campo in DecisaoAberta.__dataclass_fields__}
    assert campos == {"id", "pergunta", "porque", "peso", "universal", "predicados"}

    universo = universo_completo(Intencao.OTIMIZAR)
    abertas = lacunas_do_pedido("Está lento, dá timeout.", [Plataforma.WEB], [])
    por_id = {lacuna.id: lacuna for lacuna in abertas}

    assumiveis = assumiveis_abertas(abertas, plataformas=[Plataforma.WEB], universo=universo)
    assert assumiveis, "esperava ao menos uma lacuna assumível"

    for decisao in assumiveis:
        original = por_id[decisao.id]
        assert decisao.pergunta == original.pergunta, "a pergunta saiu truncada ou trocada"
        assert decisao.porque == original.porque
        assert not decisao.bloqueante and decisao.predicados == ()
        serializada = decisao.como_dicionario()
        assert "valor" not in serializada
        assert not any(
            chave in serializada for chave in ("resposta", "padrao", "assumido", "default")
        )
        assert serializada["pergunta"] == original.pergunta


def test_estado_gravado_nao_contem_valor_assumido(tmp_path):
    """Derrubaria este teste: gravar as assumíveis com um valor adotado pelo motor.

    A mesma regra, agora onde ela pode vazar sem ninguém ver: o arquivo. O
    `estado.json` inteiro é lido como texto e não pode conter `PADRAO_ASSUMIDO` em
    lugar nenhum, e as lacunas não respondidas não podem aparecer no mapa de respostas.
    """
    estado.novo_ciclo(tmp_path, "otimizar a exportação", "2026-08-05T10:00:00")
    descoberta.registrar(
        tmp_path, "Está lento, dá timeout no navegador.", agora="2026-08-05T10:01:00"
    )
    descoberta.responder(tmp_path, "problema", "a exportação trava o fechamento")

    bruto = estado.caminho(tmp_path).read_text(encoding="utf-8")
    assert str(Origem.PADRAO_ASSUMIDO) not in bruto

    avaliacao = descoberta.avaliar_do_disco(tmp_path)
    gravadas = set(json.loads(bruto)[descoberta.CHAVE]["respostas"])
    assert gravadas == {"problema"}
    for decisao in avaliacao.assumiveis:
        assert decisao.id not in gravadas
        assert decisao.pergunta in avaliacao.resumo()


def test_origem_padrao_assumido_e_recusada_e_nao_grava(tmp_path):
    """Derrubaria este teste: aceitar `Origem.PADRAO_ASSUMIDO` como origem de resposta.

    `PADRAO_ASSUMIDO` existe nomeado em `deteccao.py` para poder ser proibido, e este é
    o ponto onde a proibição vira código. A segunda metade do teste é a que importa: a
    recusa não pode gravar metade — o estado tem de ficar byte-idêntico.
    """
    from ferramentas.elicitacao import PadraoAssumidoProibido

    estado.novo_ciclo(tmp_path, "otimizar", "2026-08-05T10:00:00")
    descoberta.registrar(tmp_path, "Está lento, dá timeout.", agora="2026-08-05T10:01:00")
    antes = estado.caminho(tmp_path).read_bytes()

    with pytest.raises(PadraoAssumidoProibido):
        descoberta.responder(
            tmp_path, "problema", "algo qualquer", origem=Origem.PADRAO_ASSUMIDO
        )

    assert estado.caminho(tmp_path).read_bytes() == antes


# --- (4) Persistência: chave própria, `atualizar`, retrocompatível -------


def test_registrar_preserva_o_resto_do_estado(tmp_path):
    """Derrubaria este teste: montar um estado novo em vez de acrescentar a chave.

    A descoberta mora ao lado de `pendencias`, e não no lugar dela. Um mutador que
    devolvesse um dicionário novo apagaria ciclo, cartões, decisões e diffs pendentes —
    e o sumiço não daria erro nenhum, que é o modo de falhar que `estado.atualizar`
    existe para não ter.
    """
    dados = estado.novo_ciclo(tmp_path, "objetivo do ciclo", "2026-08-05T10:00:00")
    estado.registrar_diff(tmp_path, "ferramentas/algo.py")
    antes = estado.carregar(tmp_path)

    descoberta.registrar(
        tmp_path, "Está lento, dá timeout no navegador.", agora="2026-08-05T10:01:00"
    )
    depois = estado.carregar(tmp_path)

    assert descoberta.CHAVE in depois
    for chave in ("versao", "ativo", "ciclo", "fase", "cartoes", "decisoes", "pendencias",
                  "diffs_pendentes", "historico"):
        assert depois[chave] == antes[chave], f"{chave} foi alterado ao registrar a descoberta"
    assert depois["ciclo"]["objetivo"] == dados["ciclo"]["objetivo"]


def test_estado_antigo_sem_a_chave_nao_quebra(tmp_path):
    """Derrubaria este teste: exigir a chave `descoberta` na leitura.

    `estado.VERSAO` continua 1 e não há migração escrita — logo o estado gravado antes
    deste ciclo tem de carregar, ler e avaliar sem levantar. E não pode responder "sem
    bloqueante": não saber e estar livre são coisas diferentes, e o predicado que libera
    portão falha fechado.
    """
    estado.novo_ciclo(tmp_path, "ciclo anterior a este recurso", "2026-08-05T10:00:00")
    dados = estado.carregar(tmp_path)
    assert descoberta.CHAVE not in dados

    assert descoberta.ler(tmp_path) is None
    avaliacao = descoberta.avaliar(dados)
    assert avaliacao.registrada is False
    assert avaliacao.abertas == () and avaliacao.bloqueantes == ()
    assert avaliacao.liberado_para_planejar is False
    assert "não registrada" in avaliacao.resumo()

    # E o estado antigo aceita ganhar a chave nova sem perder nada.
    descoberta.registrar(tmp_path, "Está lento, dá timeout.", agora="2026-08-05T10:01:00")
    assert descoberta.avaliar_do_disco(tmp_path).registrada is True


def test_responder_reavalia_sem_perder_o_resto(tmp_path):
    """Derrubaria este teste: recalcular a descoberta do zero a cada resposta.

    Responder uma lacuna tem de mudar o veredito das outras — é o que B3 faz — sem
    perder as respostas anteriores, os palpites pendentes nem os eixos já confirmados. É
    a propriedade que o gate do C4 usa para destravar a transição depois da entrevista.
    """
    estado.novo_ciclo(tmp_path, "otimizar", "2026-08-05T10:00:00")
    descoberta.registrar(
        tmp_path, "Está lento, dá timeout no navegador.", agora="2026-08-05T10:01:00"
    )
    inicial = descoberta.avaliar_do_disco(tmp_path)
    assert inicial.intencao is Intencao.OTIMIZAR
    assert {d.id for d in inicial.bloqueantes} >= {"problema", "sucesso", "perf_medicao_atual"}

    descoberta.responder(tmp_path, "problema", "o fechamento mensal atrasa 3 horas")
    descoberta.responder(tmp_path, "sucesso", "cair de 3h para 20 minutos")
    depois = descoberta.avaliar_do_disco(tmp_path)

    assert set(depois.respondidas) == {"problema", "sucesso"}
    assert "problema" not in {d.id for d in depois.abertas}
    assert len(depois.bloqueantes) < len(inicial.bloqueantes)
    # `perf_meta` fornecia o mesmo pedaço que `sucesso`: deixou de travar e continua aberta.
    assert "perf_meta" not in {d.id for d in depois.bloqueantes}
    assert "perf_meta" in {d.id for d in depois.assumiveis}
    assert depois.palpites_pendentes == inicial.palpites_pendentes


def test_responder_onde_roda_destrava_o_bloco_da_plataforma(tmp_path):
    """Derrubaria este teste: a persistência aplicar a resposta por uma regra própria.

    A gravação usa a **mesma** `aplicar_resposta` que B1 usa para prever o efeito. Se as
    duas divergirem, o gate trava por uma mudança que a gravação não faz — e a pessoa
    responde `onde_roda` e continua bloqueada, sem entender por quê.
    """
    estado.novo_ciclo(tmp_path, "criar", "2026-08-05T10:00:00")
    descoberta.registrar(
        tmp_path, "Quero um sistema novo, do zero, para a recepção.", agora="2026-08-05T10:01:00"
    )
    antes = descoberta.avaliar_do_disco(tmp_path)
    assert antes.plataformas == ()
    assert "mobile_offline" not in {d.id for d in antes.abertas}

    descoberta.responder(tmp_path, "onde_roda", "MOBILE")
    depois = descoberta.avaliar_do_disco(tmp_path)

    assert depois.plataformas == (Plataforma.MOBILE,)
    assert "mobile_offline" in {d.id for d in depois.abertas}
    assert "onde_roda" not in {d.id for d in depois.abertas}


def test_responder_id_fora_do_conjunto_levanta_e_nao_grava(tmp_path):
    """Derrubaria este teste: gravar resposta de id que não está ativo.

    É o mesmo contrato de `entrevista.responder`: id desconhecido guardaria a resposta
    num balde que ninguém lê, a lacuna verdadeira continuaria aberta, e a pessoa
    lembraria de ter respondido. `web_autenticacao` só existe depois de a plataforma WEB
    ser confirmada — antes disso, responder é erro, não adiantamento.
    """
    estado.novo_ciclo(tmp_path, "criar", "2026-08-05T10:00:00")
    descoberta.registrar(tmp_path, "Quero um sistema novo, do zero.", agora="2026-08-05T10:01:00")
    antes = estado.caminho(tmp_path).read_bytes()

    for identificador in ("web_autenticacao", "nao_existe", ""):
        with pytest.raises(LacunaDesconhecida):
            descoberta.responder(tmp_path, identificador, "qualquer coisa")

    assert estado.caminho(tmp_path).read_bytes() == antes


def test_bloco_de_versao_desconhecida_falha_fechado(tmp_path):
    """Derrubaria este teste: ler o bloco de qualquer versão como se fosse a atual.

    Um bloco gravado por uma versão futura, lido por esta, produziria uma avaliação
    plausível sobre campos que mudaram de significado — e o resultado dela **libera**
    uma transição de fase. Predicado que abre portão falha fechado.
    """
    estado.novo_ciclo(tmp_path, "criar", "2026-08-05T10:00:00")
    descoberta.registrar(tmp_path, "Quero um sistema novo, do zero.", agora="2026-08-05T10:01:00")

    def _envelhecer(dados: dict | None) -> dict | None:
        dados[descoberta.CHAVE]["versao"] = descoberta.VERSAO_BLOCO + 1
        return dados

    estado.atualizar(tmp_path, _envelhecer)
    with pytest.raises(descoberta.DescobertaInvalida):
        descoberta.avaliar_do_disco(tmp_path)


def test_confirmar_e_recusar_palpite(tmp_path):
    """Derrubaria este teste: confirmar e recusar virarem a mesma coisa.

    Confirmado, o palpite aplica o eixo e destrava um bloco. Recusado, ele sai da
    pendência e **não** deixa rastro de valor assumido em lugar nenhum — nem nos eixos,
    nem nas respostas. Ignorar não é nenhuma das duas: o palpite continua pendente.
    """
    estado.novo_ciclo(tmp_path, "criar", "2026-08-05T10:00:00")
    descoberta.registrar(
        tmp_path,
        "Quero um sistema novo, do zero, com pagamento no celular.",
        agora="2026-08-05T10:01:00",
    )
    inicial = descoberta.avaliar_do_disco(tmp_path)
    valores = {palpite.valor for palpite in inicial.palpites_pendentes}
    assert {"MOBILE", "LOJA_PAGAMENTOS"} <= valores

    descoberta.confirmar(tmp_path, "MOBILE")
    descoberta.recusar(tmp_path, "LOJA_PAGAMENTOS")
    depois = descoberta.avaliar_do_disco(tmp_path)

    assert depois.plataformas == (Plataforma.MOBILE,)
    assert depois.contextos == ()
    assert {p.valor for p in depois.palpites_pendentes} == valores - {"MOBILE", "LOJA_PAGAMENTOS"}
    assert "mobile_loja" in {d.id for d in depois.abertas}
    assert "pag_estorno" not in {d.id for d in depois.abertas}


def test_mutacao_sem_bloco_levanta_e_nao_grava(tmp_path):
    """Derrubaria este teste: criar o bloco de descoberta na primeira resposta.

    Criar o bloco aqui exigiria inventar o pedido e a intenção — e intenção inventada
    escolhe *quais perguntas existem*, que é o erro mais caro deste motor. A recusa é
    explícita e nomeada.
    """
    estado.novo_ciclo(tmp_path, "criar", "2026-08-05T10:00:00")
    antes = estado.caminho(tmp_path).read_bytes()

    with pytest.raises(descoberta.DescobertaAusente):
        descoberta.responder(tmp_path, "problema", "qualquer coisa")
    with pytest.raises(descoberta.DescobertaAusente):
        descoberta.confirmar(tmp_path, "WEB")

    assert estado.caminho(tmp_path).read_bytes() == antes


def test_registrar_pedido_indeterminado_nao_grava(tmp_path):
    """Derrubaria este teste: adotar uma intenção padrão quando o texto não decide.

    A indeterminação sobe para quem consegue perguntar, e o estado fica intocado.
    Registrar com `MATERIALIZAR` por padrão produziria uma entrevista inteira sobre o
    trabalho errado, respondida até o fim antes de alguém notar.
    """
    from ferramentas.elicitacao import IntencaoIndeterminada

    estado.novo_ciclo(tmp_path, "ciclo", "2026-08-05T10:00:00")
    antes = estado.caminho(tmp_path).read_bytes()

    with pytest.raises(IntencaoIndeterminada):
        descoberta.registrar(tmp_path, "bom dia, tudo bem?", agora="2026-08-05T10:01:00")

    assert estado.caminho(tmp_path).read_bytes() == antes
    assert descoberta.ler(tmp_path) is None


# --- (5) O mapa do aceite se valida -------------------------------------


def test_validar_bloqueio_aprova_o_mapa_real():
    """Derrubaria este teste: qualquer id inexistente em `PARTES_DO_ACEITE`.

    Id digitado errado ali não levanta nada em execução: a linha nunca casa, B3 deixa de
    disparar por ela, e o plano passa no gate sem aceite possível. Como `validar_catalogo`
    e `validar_taxonomia`, o validador devolve o próprio dado.
    """
    assert validar_bloqueio() is PARTES_DO_ACEITE

    conhecidos = {lacuna.id for lacuna in CATALOGO}
    for lacunas in __import__(
        "ferramentas.elicitacao.taxonomia", fromlist=["LACUNAS_POR_INTENCAO"]
    ).LACUNAS_POR_INTENCAO.values():
        conhecidos.update(lacuna.id for lacuna in lacunas)
    assert set(PARTES_DO_ACEITE) <= conhecidos


def test_validar_bloqueio_reprova_id_inexistente_e_parte_orfa():
    """Derrubaria este teste: o validador só olhar o formato e não o conteúdo.

    Os dois defeitos que ele existe para pegar são silenciosos pelos dois lados: id que
    não casa faz B3 disparar de menos; parte de aceite que nenhuma lacuna fornece faz a
    enumeração crescer sem o critério mudar, sugerindo cobertura que não existe.
    """
    torto = dict(PARTES_DO_ACEITE)
    torto["lacuna_que_nunca_existiu"] = ParteDoAceite.LIMIAR
    with pytest.raises(BloqueioInvalido) as erro:
        validar_bloqueio(torto)
    assert "lacuna_que_nunca_existiu" in str(erro.value)

    sem_limiar = {i: p for i, p in PARTES_DO_ACEITE.items() if p is not ParteDoAceite.LIMIAR}
    with pytest.raises(BloqueioInvalido) as erro:
        validar_bloqueio(sem_limiar)
    assert "LIMIAR" in str(erro.value)
