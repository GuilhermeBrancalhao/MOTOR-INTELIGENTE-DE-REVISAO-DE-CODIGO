import pytest

from indicador_de_qualidade import (
    GateDeQualidade,
    HistoricoDeQualidade,
    ItemDeDivida,
    ItemDeDividaIncompleto,
    LimiarNaoAtingido,
    Medicao,
    detectar_regressao,
)


def medicao(data="2026-08-04", totais=10, com_prova=6, cobertura_linha=0.95):
    return Medicao(data, totais, com_prova, cobertura_linha)


def test_gate_ignora_cobertura_de_linha_alta_com_mutacao_baixa():
    """H1: a mutação alvo é o gate considerar cobertura_de_linha na decisão."""
    gate = GateDeQualidade(limiar_minimo=0.8)
    m = medicao(com_prova=6, cobertura_linha=0.95)  # taxa de mutacao = 0.6, abaixo do limiar
    with pytest.raises(LimiarNaoAtingido):
        gate.verificar(m)


def test_gate_bloqueia_taxa_abaixo_do_limiar():
    gate = GateDeQualidade(limiar_minimo=0.8)
    m = medicao(com_prova=5)
    with pytest.raises(LimiarNaoAtingido):
        gate.verificar(m)


def test_gate_com_excecao_permite_passagem():
    gate = GateDeQualidade(limiar_minimo=0.8)
    m = medicao(com_prova=5)
    gate.verificar(m, excecao_registrada=True)  # nao levanta


def test_gate_aceita_taxa_acima_do_limiar():
    gate = GateDeQualidade(limiar_minimo=0.8)
    m = medicao(com_prova=9)
    gate.verificar(m)  # nao levanta


def test_item_de_divida_incompleto_e_rejeitado():
    """H3: a mutação alvo é aceitar ItemDeDivida com campo vazio."""
    with pytest.raises(ItemDeDividaIncompleto):
        ItemDeDivida(descricao="refatorar modulo X", motivo_adiamento="prazo", data_registro="2026-08-04", custo_estimado="")


def test_regressao_exige_pelo_menos_duas_medicoes():
    """H4: a mutação alvo é julgar tendência com uma única medição."""
    historico = HistoricoDeQualidade()
    historico.registrar(medicao())
    assert detectar_regressao(historico) is None


def test_regressao_detectada_entre_duas_medicoes():
    """H5: a mutação alvo é não reportar regressão quando a taxa cai."""
    historico = HistoricoDeQualidade()
    historico.registrar(medicao(data="2026-08-01", com_prova=9))
    historico.registrar(medicao(data="2026-08-04", com_prova=6))
    regressao = detectar_regressao(historico)
    assert regressao is not None
    assert regressao.taxa_anterior == 0.9
    assert regressao.taxa_atual == 0.6


def test_sem_regressao_quando_taxa_mantem_ou_sobe():
    historico = HistoricoDeQualidade()
    historico.registrar(medicao(data="2026-08-01", com_prova=6))
    historico.registrar(medicao(data="2026-08-04", com_prova=9))
    assert detectar_regressao(historico) is None


def test_medicao_expoe_submetricas_nomeadas():
    """H6: confirma que Medicao carrega campos separados, não um score único."""
    m = medicao()
    campos = {f.name for f in m.__dataclass_fields__.values()}
    assert {"regras_totais", "regras_com_prova_de_mutacao", "cobertura_de_linha"} <= campos
