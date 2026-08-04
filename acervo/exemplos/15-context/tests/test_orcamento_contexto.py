import pytest

from orcamento_contexto import (
    Categoria,
    ItemDeContexto,
    Orcamento,
    OrcamentoExcedidoPelaInstrucao,
    OrcamentoInvalido,
    montar_janela,
    proximo_da_margem,
)


def item(id_, categoria, tokens):
    return ItemDeContexto(id_, categoria, tokens)


def test_margem_zero_e_rejeitada():
    with pytest.raises(OrcamentoInvalido):
        Orcamento(limite_total=1000, margem_compactacao=0)


def test_tudo_cabe_sem_descarte():
    orc = Orcamento(1000, margem_compactacao=100)
    candidatos = (
        item("i1", Categoria.INSTRUCAO_SISTEMA, 200),
        item("h1", Categoria.HISTORICO_RECENTE, 300),
    )
    janela = montar_janela(candidatos, orc)
    assert janela.descartes == ()
    assert janela.tokens_usados == 500


def test_descarte_remove_menor_prioridade_primeiro():
    """C2: a mutação alvo é descartar por ordem de chegada em vez de
    prioridade — este teste falha se isso acontecer."""
    orc = Orcamento(limite_total=500, margem_compactacao=50)
    candidatos = (
        item("doc", Categoria.DOCUMENTO_RECUPERADO, 200),  # prioridade 2
        item("hist", Categoria.HISTORICO_RECENTE, 200),     # prioridade 1
        item("instr", Categoria.INSTRUCAO_SISTEMA, 200),    # prioridade 0
    )
    janela = montar_janela(candidatos, orc)
    # 600 tokens de candidatos, limite 500 -> precisa descartar 200
    ids_restantes = {i.id for i in janela.itens}
    assert "instr" in ids_restantes
    assert "doc" not in ids_restantes  # menor prioridade descartada primeiro
    assert "hist" in ids_restantes


def test_todo_descarte_gera_registro():
    """C3: nenhum item some sem Descarte correspondente."""
    orc = Orcamento(limite_total=300, margem_compactacao=50)
    candidatos = (
        item("instr", Categoria.INSTRUCAO_SISTEMA, 100),
        item("doc1", Categoria.DOCUMENTO_RECUPERADO, 150),
        item("doc2", Categoria.DOCUMENTO_RECUPERADO, 150),
    )
    janela = montar_janela(candidatos, orc)
    assert len(janela.descartes) == 1
    assert janela.descartes[0].motivo != ""


def test_instrucao_nunca_e_descartada_para_caber_outros_itens():
    """C6: instrução de prioridade máxima sobrevive mesmo sob pressão alta."""
    orc = Orcamento(limite_total=250, margem_compactacao=50)
    candidatos = (
        item("instr", Categoria.INSTRUCAO_SISTEMA, 200),
        item("hist", Categoria.HISTORICO_RECENTE, 200),
    )
    janela = montar_janela(candidatos, orc)
    assert any(i.id == "instr" for i in janela.itens)
    assert janela.tokens_usados <= 250


def test_instrucao_sozinha_maior_que_orcamento_e_recusada_explicitamente():
    """C6: recusa explícita, não descarte parcial da própria instrução."""
    orc = Orcamento(limite_total=100, margem_compactacao=10)
    candidatos = (item("instr", Categoria.INSTRUCAO_SISTEMA, 150),)
    with pytest.raises(OrcamentoExcedidoPelaInstrucao):
        montar_janela(candidatos, orc)


def test_proximo_da_margem_detecta_o_ponto_certo():
    orc = Orcamento(limite_total=1000, margem_compactacao=100)
    assert proximo_da_margem(consumo_atual=850, orcamento=orc) is False
    assert proximo_da_margem(consumo_atual=920, orcamento=orc) is True
