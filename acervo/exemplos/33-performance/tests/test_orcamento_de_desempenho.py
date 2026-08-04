import pytest

from orcamento_de_desempenho import (
    EstrategiaDeSobrecargaAusente,
    MargemDeVariabilidadeAusente,
    MedicaoDeCarga,
    MedicaoSobCargaInsuficiente,
    Otimizacao,
    OtimizacaoNaoValidada,
    PoliticaDeSobrecarga,
    SLO,
    SLOAusente,
    declarar_operacao_pronta,
    detectar_regressao_de_performance,
    validar_otimizacao,
    verificar_slo,
)


def slo(operacao="consulta", p95=200.0, p99=500.0, ia=False):
    return SLO(operacao, p95, p99, envolve_chamada_de_ia=ia)


def politica():
    return PoliticaDeSobrecarga(limite_concorrente=50, estrategia="rejeitar")


def medicao(operacao="consulta", concorrencia=20, amostras=None):
    amostras = amostras or tuple(range(50, 50 + concorrencia))
    return MedicaoDeCarga(operacao, concorrencia, amostras)


def test_operacao_sem_slo_e_rejeitada():
    """J1: a mutação alvo é aceitar operação sem SLO declarado."""
    with pytest.raises(SLOAusente):
        declarar_operacao_pronta("consulta", None, politica())


def test_operacao_sem_estrategia_de_sobrecarga_e_rejeitada():
    """J4: a mutação alvo é aceitar operação sem política de sobrecarga."""
    with pytest.raises(EstrategiaDeSobrecargaAusente):
        declarar_operacao_pronta("consulta", slo(), None)


def test_medicao_com_concorrencia_baixa_e_rejeitada():
    """J2: a mutação alvo é aceitar medição sob carga artificialmente baixa."""
    m = medicao(concorrencia=2, amostras=(50.0, 60.0))
    with pytest.raises(MedicaoSobCargaInsuficiente):
        verificar_slo(slo(), m, concorrencia_minima=10)


def test_regressao_de_performance_detectada():
    """J3: a mutação alvo é não reportar regressão quando p95 piora."""
    anterior = medicao(amostras=tuple(range(50, 120)))  # p95 baixo
    atual = medicao(amostras=tuple(range(200, 270)))  # p95 alto
    regressao = detectar_regressao_de_performance(anterior, atual)
    assert regressao is not None
    assert regressao.p95_atual > regressao.p95_anterior


def test_sem_regressao_quando_p95_melhora():
    anterior = medicao(amostras=tuple(range(200, 270)))
    atual = medicao(amostras=tuple(range(50, 120)))
    assert detectar_regressao_de_performance(anterior, atual) is None


def test_otimizacao_nao_validada_e_rejeitada():
    """J5: a mutação alvo é aceitar otimização sem melhoria mensurável de p95."""
    antes = medicao(amostras=tuple(range(50, 120)))
    depois = medicao(amostras=tuple(range(50, 120)))  # identico, sem melhoria
    with pytest.raises(OtimizacaoNaoValidada):
        validar_otimizacao(Otimizacao("cache de consulta", antes, depois))


def test_otimizacao_validada_e_aceita():
    antes = medicao(amostras=tuple(range(200, 270)))
    depois = medicao(amostras=tuple(range(50, 120)))
    validar_otimizacao(Otimizacao("cache de consulta", antes, depois))  # nao levanta


def test_slo_de_ia_sem_margem_e_rejeitado():
    """J6: a mutação alvo é aceitar SLO de IA sem margem entre p95 e p99."""
    with pytest.raises(MargemDeVariabilidadeAusente):
        SLO("resumo-por-ia", p95_ms=2000.0, p99_ms=2000.0, envolve_chamada_de_ia=True)


def test_slo_de_ia_com_margem_e_aceito():
    s = SLO("resumo-por-ia", p95_ms=2000.0, p99_ms=8000.0, envolve_chamada_de_ia=True)
    assert s.p99_ms > s.p95_ms
