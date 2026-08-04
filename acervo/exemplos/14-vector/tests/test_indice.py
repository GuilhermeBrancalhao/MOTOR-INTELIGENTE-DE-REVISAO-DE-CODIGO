import pytest

from indice import Consulta, ConsultaIncompleta, IndiceVetorial, Metrica, Vetor, VersaoIncompativel, comparar


def vetor(id_, valores=(1.0, 0.0), versao="modelo-v1", particao="p1"):
    return Vetor(id_, valores, versao, particao)


def test_comparar_versoes_diferentes_e_rejeitado():
    """V1, a invariante central."""
    a = vetor("a", versao="modelo-v1")
    b = vetor("b", versao="modelo-v2")
    with pytest.raises(VersaoIncompativel):
        comparar(a, b, Metrica.COSSENO)


def test_comparar_mesma_versao_funciona():
    a = vetor("a", valores=(1.0, 0.0))
    b = vetor("b", valores=(1.0, 0.0))
    assert comparar(a, b, Metrica.COSSENO) == pytest.approx(1.0)


def test_consulta_sem_metrica_e_rejeitada():
    with pytest.raises(ConsultaIncompleta):
        Consulta((1.0, 0.0), None, "p1", "modelo-v1")


def test_consulta_sem_particao_e_rejeitada():
    with pytest.raises(ConsultaIncompleta):
        Consulta((1.0, 0.0), Metrica.COSSENO, None, "modelo-v1")


def test_busca_nunca_cruza_particao():
    """V3: a mutação alvo é remover o filtro de particao em buscar()."""
    idx = IndiceVetorial()
    idx.indexar(vetor("a", valores=(1.0, 0.0), particao="p1"))
    idx.indexar(vetor("b", valores=(1.0, 0.0), particao="p2"))
    consulta = Consulta((1.0, 0.0), Metrica.COSSENO, "p1", "modelo-v1")
    resultado = idx.buscar(consulta)
    assert [r.id_documento for r in resultado] == ["a"]


def test_busca_nunca_cruza_versao_de_modelo():
    idx = IndiceVetorial()
    idx.indexar(vetor("a", versao="modelo-v1"))
    idx.indexar(vetor("b", versao="modelo-v2"))
    consulta = Consulta((1.0, 0.0), Metrica.COSSENO, "p1", "modelo-v1")
    resultado = idx.buscar(consulta)
    assert [r.id_documento for r in resultado] == ["a"]


def test_documento_excluido_nunca_aparece_no_resultado():
    """V6: exclusão lógica, independente de remoção física — o vetor
    continua em idx.vetores, mas nunca aparece no resultado."""
    idx = IndiceVetorial()
    idx.indexar(vetor("a", valores=(1.0, 0.0)))
    idx.excluir("a")
    consulta = Consulta((1.0, 0.0), Metrica.COSSENO, "p1", "modelo-v1")
    resultado = idx.buscar(consulta)
    assert resultado == ()
    assert any(v.id_documento == "a" for v in idx.vetores)  # fisicamente presente


def test_resultado_ordenado_por_proximidade():
    idx = IndiceVetorial()
    idx.indexar(vetor("longe", valores=(0.0, 1.0)))
    idx.indexar(vetor("perto", valores=(1.0, 0.0)))
    consulta = Consulta((1.0, 0.0), Metrica.COSSENO, "p1", "modelo-v1")
    resultado = idx.buscar(consulta)
    assert resultado[0].id_documento == "perto"
