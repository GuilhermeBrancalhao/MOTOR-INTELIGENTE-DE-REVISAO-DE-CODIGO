import pytest

from selecao_de_modelo import (
    CandidatoDeModelo,
    CustoPorTarefa,
    FallbackAusente,
    ModeloNaoAvaliado,
    PlanoDeTarefa,
    RegistroDeTroca,
    ResultadoDeAvaliacao,
    comparar_custo_por_tarefa,
    registrar_troca,
    validar_plano,
)


def avaliacao(modelo="modelo-x", aprovados=92, total=100, data="2026-08-04"):
    return ResultadoDeAvaliacao(modelo, aprovados, total, data)


def test_modelo_nao_avaliado_nao_pode_ser_aprovado():
    """M2: a mutação alvo é retornar False silenciosamente em vez de levantar exceção."""
    c = CandidatoDeModelo(nome="modelo-x", atende_requisito=True, avaliacao=None)
    with pytest.raises(ModeloNaoAvaliado):
        c.aprovado()


def test_modelo_avaliado_abaixo_do_limiar_e_reprovado():
    c = CandidatoDeModelo(
        nome="modelo-x", atende_requisito=True, avaliacao=avaliacao(aprovados=80, total=100)
    )
    assert c.aprovado(limiar_aprovacao=0.9) is False


def test_modelo_avaliado_acima_do_limiar_e_aprovado():
    c = CandidatoDeModelo(
        nome="modelo-x", atende_requisito=True, avaliacao=avaliacao(aprovados=95, total=100)
    )
    assert c.aprovado(limiar_aprovacao=0.9) is True


def test_modelo_que_nao_atende_requisito_e_reprovado_mesmo_com_boa_avaliacao():
    """M1: a mutação alvo é aprovar um candidato sem checar atende_requisito."""
    c = CandidatoDeModelo(
        nome="modelo-poderoso", atende_requisito=False, avaliacao=avaliacao(aprovados=100, total=100)
    )
    assert c.aprovado() is False


def test_plano_sem_fallback_e_rejeitado():
    """M3: a mutação alvo é aceitar PlanoDeTarefa sem modelo_fallback."""
    plano = PlanoDeTarefa(tarefa="resumo", modelo_principal="modelo-x", modelo_fallback=None)
    with pytest.raises(FallbackAusente):
        validar_plano(plano)


def test_plano_com_fallback_e_aceito():
    plano = PlanoDeTarefa(tarefa="resumo", modelo_principal="modelo-x", modelo_fallback="modelo-y")
    validar_plano(plano)  # nao levanta


def test_comparacao_de_custo_favorece_menor_custo_total_nao_menor_preco_unitario():
    """M4: modelo A tem preco unitario menor mas custo total maior; a comparação
    deve favorecer B mesmo com preco unitario maior."""
    a = CustoPorTarefa(
        modelo="modelo-A",
        tokens_entrada=1000,
        tokens_saida=2000,
        tentativas=3,  # precisou de 3 tentativas
        preco_por_1k_entrada=0.001,
        preco_por_1k_saida=0.002,
    )
    b = CustoPorTarefa(
        modelo="modelo-B",
        tokens_entrada=1000,
        tokens_saida=1000,
        tentativas=1,  # resolveu de primeira
        preco_por_1k_entrada=0.005,
        preco_por_1k_saida=0.008,
    )
    assert a.total() > b.total()  # confirma o cenario antes de testar a funcao
    assert comparar_custo_por_tarefa(a, b) == "modelo-B"


def test_toda_troca_fica_registrada_no_historico():
    """M6: confirma que a troca registrada carrega data, motivo e avaliacao completos."""
    historico = []
    troca = RegistroDeTroca(
        tarefa="resumo",
        modelo_anterior="modelo-x",
        modelo_novo="modelo-y",
        motivo="modelo-x descontinuado pelo fornecedor",
        data="2026-08-04",
        resultado_avaliacao=avaliacao(modelo="modelo-y"),
    )
    registrar_troca(historico, troca)
    assert len(historico) == 1
    assert historico[0].motivo == "modelo-x descontinuado pelo fornecedor"
    assert historico[0].resultado_avaliacao.modelo == "modelo-y"
