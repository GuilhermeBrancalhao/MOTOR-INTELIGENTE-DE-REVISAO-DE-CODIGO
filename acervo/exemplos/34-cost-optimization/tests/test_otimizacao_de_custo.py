import pytest

from otimizacao_de_custo import (
    CustoDeTarefa,
    EscopoAusente,
    HistoricoDeCusto,
    OrcamentoDeEscopo,
    OtimizacaoDeCusto,
    OtimizacaoDeCustoNaoValidada,
    PeriodoDeCusto,
    TarefaAusente,
    detectar_tendencia_de_custo,
    validar_otimizacao_de_custo,
    verificar_orcamento,
)


def custo(tarefa="resumo-relatorio", escopo="time-produto", valor=1.5, data="2026-08-04"):
    return CustoDeTarefa(tarefa, escopo, valor, data)


def test_custo_sem_tarefa_e_rejeitado():
    """U1: a mutação alvo é aceitar CustoDeTarefa sem identificar a tarefa."""
    with pytest.raises(TarefaAusente):
        CustoDeTarefa(tarefa="", escopo="time-produto", valor=1.0, data="2026-08-04")


def test_custo_sem_escopo_e_rejeitado():
    """U2: a mutação alvo é aceitar CustoDeTarefa sem escopo atribuído."""
    with pytest.raises(EscopoAusente):
        CustoDeTarefa(tarefa="resumo", escopo="", valor=1.0, data="2026-08-04")


def test_orcamento_estado_ok_alerta_estourado():
    """U3: confirma os três estados distintos sob níveis crescentes de gasto."""
    orcamento = OrcamentoDeEscopo(escopo="time-produto", limite=100.0, limiar_de_alerta=0.8)
    assert verificar_orcamento(orcamento, gasto_atual=50.0) == "OK"
    assert verificar_orcamento(orcamento, gasto_atual=85.0) == "ALERTA"
    assert verificar_orcamento(orcamento, gasto_atual=100.0) == "ESTOURADO"


def test_tendencia_exige_duas_medicoes():
    """U4: a mutação alvo é julgar tendência com um único período registrado."""
    historico = HistoricoDeCusto()
    historico.registrar(PeriodoDeCusto("2026-07", "time-produto", 200.0))
    assert detectar_tendencia_de_custo(historico) is None


def test_tendencia_detectada_entre_dois_periodos():
    historico = HistoricoDeCusto()
    historico.registrar(PeriodoDeCusto("2026-07", "time-produto", 200.0))
    historico.registrar(PeriodoDeCusto("2026-08", "time-produto", 260.0))
    tendencia = detectar_tendencia_de_custo(historico)
    assert tendencia is not None
    assert tendencia.variacao == 60.0


def test_otimizacao_de_custo_nao_validada_e_rejeitada():
    """U5: a mutação alvo é aceitar mudança sem redução real de gasto medido."""
    with pytest.raises(OtimizacaoDeCustoNaoValidada):
        validar_otimizacao_de_custo(
            OtimizacaoDeCusto("trocar de modelo", custo_antes=100.0, custo_depois=100.0)
        )


def test_otimizacao_de_custo_validada_e_aceita():
    validar_otimizacao_de_custo(
        OtimizacaoDeCusto("trocar de modelo", custo_antes=100.0, custo_depois=70.0)
    )  # nao levanta


def test_total_por_escopo_agrega_apenas_o_escopo_correto():
    from otimizacao_de_custo import RegistroDeCusto

    registro = RegistroDeCusto()
    registro.registrar(custo(escopo="time-A", valor=10.0))
    registro.registrar(custo(escopo="time-A", valor=5.0))
    registro.registrar(custo(escopo="time-B", valor=99.0))
    assert registro.total_por_escopo("time-A") == 15.0
