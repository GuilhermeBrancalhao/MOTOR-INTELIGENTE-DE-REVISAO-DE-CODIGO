import pytest

from inventario import DecisaoDePortfolio, DependenciaIncompleta, Inventario, Sistema


def sistema(id_, fornecedor="ProvedorX", categoria="rag", custo=1000.0):
    return Sistema(id_, fornecedor, "modelo-a", "fonte-b", categoria, custo)


def test_sistema_sem_fornecedor_e_rejeitado():
    with pytest.raises(DependenciaIncompleta):
        Sistema("s1", "", "modelo-a", "fonte-b", "rag", 100.0)


def test_decisao_sem_consequencia_e_rejeitada():
    """E2: nenhuma decisão de portfólio existe sem justificativa nomeada."""
    with pytest.raises(ValueError, match="E2"):
        DecisaoDePortfolio(("s1",), "", "aceitar")


def test_custo_agregado_soma_todos_os_sistemas_do_mesmo_fornecedor():
    """E3: a mutação alvo é trocar soma por maior valor isolado — este
    teste falha se isso acontecer, porque o total esperado é a soma."""
    inv = Inventario()
    inv.registrar(sistema("s1", custo=1000.0))
    inv.registrar(sistema("s2", custo=1500.0))
    inv.registrar(sistema("s3", fornecedor="ProvedorY", custo=5000.0))
    totais = inv.custo_total_agregado()
    assert totais["ProvedorX"] == 2500.0
    assert totais["ProvedorY"] == 5000.0


def test_concentracao_dispara_apenas_no_terceiro_sistema_do_mesmo_fornecedor():
    inv = Inventario()
    inv.registrar(sistema("s1"))
    assert inv.concentracao_por_fornecedor() == {}
    inv.registrar(sistema("s2"))
    assert inv.concentracao_por_fornecedor() == {}
    inv.registrar(sistema("s3"))
    assert set(inv.concentracao_por_fornecedor()["ProvedorX"]) == {"s1", "s2", "s3"}


def test_dois_sistemas_de_categorias_diferentes_nao_sao_duplicacao():
    inv = Inventario()
    inv.registrar(sistema("s1", categoria="rag"))
    inv.registrar(sistema("s2", categoria="classificacao"))
    assert inv.duplicacoes() == ()


def test_dois_sistemas_de_mesma_categoria_sao_duplicacao():
    """E5: achado de portfólio, não culpa de projeto — o teste só confirma
    a detecção estrutural, não atribui responsabilidade."""
    inv = Inventario()
    inv.registrar(sistema("s1", categoria="rag"))
    inv.registrar(sistema("s2", categoria="rag"))
    assert inv.duplicacoes() == (("s1", "s2"),)


def test_registrar_decisao_com_consequencia_valida_funciona():
    inv = Inventario()
    inv.decidir(("s1", "s2", "s3"), "concentracao de fornecedor com 3 sistemas", "aceitar")
    assert len(inv.decisoes) == 1
    assert inv.decisoes[0].consequencia == "concentracao de fornecedor com 3 sistemas"
