import pytest

from grafo import Estado, Grafo, GrafoInvalido, No, Politica


def leque():
    """A -> B1,B2,B3 -> C (fan-out seguido de fan-in)."""
    return Grafo({
        "A": No("A"),
        "B1": No("B1", ("A",)),
        "B2": No("B2", ("A",)),
        "B3": No("B3", ("A",)),
        "C": No("C", ("B1", "B2", "B3")),
    })


def test_ciclo_direto_e_rejeitado_na_submissao():
    with pytest.raises(GrafoInvalido, match="ciclo"):
        Grafo({"A": No("A", ("B",)), "B": No("B", ("A",))})


def test_ciclo_indireto_por_tres_nos_tambem_e_rejeitado():
    """Ciclo A->B->C->A e mais facil de introduzir por acidente que o direto, e
    um detector que so olhasse pares nao pegaria."""
    with pytest.raises(GrafoInvalido, match="ciclo"):
        Grafo({"A": No("A", ("C",)), "B": No("B", ("A",)), "C": No("C", ("B",))})


def test_dependencia_inexistente_e_rejeitada():
    with pytest.raises(GrafoInvalido, match="nao existe"):
        Grafo({"A": No("A", ("fantasma",))})


def test_grafo_ciclico_nao_executa_nenhum_no():
    """A rejeicao acontece inteiramente no planejamento: nenhum estado chega a ser
    criado, entao nao ha como um no ter rodado."""
    try:
        Grafo({"A": No("A", ("B",)), "B": No("B", ("A",))})
    except GrafoInvalido as e:
        assert "ciclo" in str(e)
    else:  # pragma: no cover
        pytest.fail("grafo ciclico deveria ter sido rejeitado")


def test_fan_out_libera_os_tres_paralelos_de_uma_vez():
    g = leque()
    g.marcar("A", Estado.SUCESSO)
    assert g.prontos() == ("B1", "B2", "B3")


def test_fan_in_com_uma_dependencia_falha_nunca_libera():
    """A mutacao alvo: trocar `all` por `any` em `prontos()`. Com dois sucessos e
    uma falha, o `any` liberaria C para agregar dado parcial; o `all` nao."""
    g = leque()
    g.marcar("A", Estado.SUCESSO)
    g.marcar("B1", Estado.SUCESSO)
    g.marcar("B2", Estado.SUCESSO)
    g.marcar("B3", Estado.FALHA_DEFINITIVA)
    assert "C" not in g.prontos()
    assert g.estados["C"] is Estado.ABORTADO


def test_fan_in_com_dependencia_apenas_pendente_tambem_nao_libera():
    g = leque()
    g.marcar("A", Estado.SUCESSO)
    g.marcar("B1", Estado.SUCESSO)
    g.marcar("B2", Estado.SUCESSO)
    assert "C" not in g.prontos()


def test_ramo_independente_sobrevive_a_falha_de_outro_ramo():
    """Falha parcial: o ramo D nao depende de B, entao continua elegivel."""
    g = Grafo({
        "A": No("A"),
        "B": No("B", ("A",)),
        "C": No("C", ("B",)),
        "D": No("D", ("A",)),
    })
    g.marcar("A", Estado.SUCESSO)
    g.marcar("B", Estado.FALHA_DEFINITIVA)
    assert g.estados["C"] is Estado.ABORTADO
    assert "D" in g.prontos()


def test_resultado_e_granular_por_no_sem_agregado():
    g = leque()
    g.marcar("A", Estado.SUCESSO)
    g.marcar("B1", Estado.FALHA_DEFINITIVA)
    r = g.resultado()
    assert set(r) == {"A", "B1", "B2", "B3", "C"}
    assert not any(k in r for k in ("sucesso", "ok", "falhou"))


def test_ordem_topologica_respeita_dependencia():
    ordem = leque().ordem_topologica()
    assert ordem.index("A") < ordem.index("B1") < ordem.index("C")
