import pytest

from planejamento import (
    AndamentoDaTarefa,
    CriterioNaoAtingido,
    DependenciaForaDeOrdem,
    EscopoNaoNegociado,
    EstimativaSemIncerteza,
    MotivoDoBloqueioAusente,
    PlanoDeCiclo,
    RevisaoDePlano,
    RevisaoIncompleta,
    Tarefa,
    ordenar_por_dependencia,
    registrar_revisao,
)


def tarefa(nome, depende_de=frozenset(), min_dias=1.0, max_dias=3.0):
    return Tarefa(
        nome=nome, depende_de=depende_de, criterio_de_pronto="testes passam e revisado",
        estimativa_min_dias=min_dias, estimativa_max_dias=max_dias,
    )


def test_ordenacao_respeita_dependencia_real():
    tarefas = {
        "b": tarefa("b", depende_de=frozenset({"a"})),
        "a": tarefa("a"),
        "c": tarefa("c", depende_de=frozenset({"b"})),
    }
    ordem = ordenar_por_dependencia(tarefas)
    assert ordem.index("a") < ordem.index("b") < ordem.index("c")


def test_ciclo_de_dependencia_e_detectado():
    """Z1: a mutação alvo é produzir uma ordem inválida em vez de detectar o ciclo."""
    tarefas = {
        "a": tarefa("a", depende_de=frozenset({"b"})),
        "b": tarefa("b", depende_de=frozenset({"a"})),
    }
    with pytest.raises(DependenciaForaDeOrdem):
        ordenar_por_dependencia(tarefas)


def test_estimativa_sem_incerteza_e_rejeitada():
    """Z2: a mutação alvo é aceitar estimativa_min_dias igual a estimativa_max_dias."""
    plano = PlanoDeCiclo(escopo_negociado="entregar exportacao de relatorio")
    with pytest.raises(EstimativaSemIncerteza):
        plano.adicionar_tarefa(tarefa("x", min_dias=2.0, max_dias=2.0))


def test_plano_sem_escopo_negociado_e_rejeitado():
    """Z3: a mutação alvo é aceitar PlanoDeCiclo sem escopo declarado."""
    with pytest.raises(EscopoNaoNegociado):
        PlanoDeCiclo(escopo_negociado="")


def test_revisao_de_plano_sem_motivo_e_rejeitada():
    """Z4: a mutação alvo é aceitar RevisaoDePlano sem motivo."""
    historico = []
    with pytest.raises(RevisaoIncompleta):
        registrar_revisao(historico, RevisaoDePlano(motivo="", tarefas_afetadas=(), data="2026-08-04"))
    assert historico == []


def test_bloqueio_sem_motivo_e_rejeitado():
    """Z5: a mutação alvo é aceitar bloqueio sem motivo explícito."""
    andamento = AndamentoDaTarefa(tarefa="migrar-banco")
    with pytest.raises(MotivoDoBloqueioAusente):
        andamento.bloquear("")


def test_conclusao_sem_atingir_criterio_e_rejeitada():
    """Z6: a mutação alvo é aceitar conclusão sem confirmar o critério de pronto."""
    andamento = AndamentoDaTarefa(tarefa="migrar-banco")
    with pytest.raises(CriterioNaoAtingido):
        andamento.concluir(criterio_atingido=False)


def test_bloqueio_distingue_de_nao_iniciada():
    from planejamento import EstadoDaTarefa

    andamento = AndamentoDaTarefa(tarefa="migrar-banco")
    assert andamento.estado == EstadoDaTarefa.NAO_INICIADA
    andamento.bloquear("aguardando aprovacao de acesso, solicitada em 2026-08-01")
    assert andamento.estado == EstadoDaTarefa.BLOQUEADA
    assert andamento.motivo_do_bloqueio is not None
