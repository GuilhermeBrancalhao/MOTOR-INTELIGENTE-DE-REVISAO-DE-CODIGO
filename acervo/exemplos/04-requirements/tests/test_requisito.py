import pytest

from requisito import Conjunto, CriterioDeAceite, IdentificadorReciclado, Origem, Requisito


def criterio(desc="valor confere"):
    return CriterioDeAceite(desc, verificar=lambda ctx: True)


def test_requisito_de_origem_nao_humana_exige_lacuna_id():
    """Q3: rastro para trás obrigatório, exceto quando a origem já é humana."""
    with pytest.raises(ValueError, match="lacuna_id"):
        Requisito("R1", "enunciado", criterio(), Origem.INFERIDA, lacuna_id=None)


def test_requisito_decidido_por_humano_dispensa_lacuna_id():
    r = Requisito("R1", "enunciado", criterio(), Origem.DECIDIDA_POR_HUMANO, lacuna_id=None)
    assert r.lacuna_id is None


def test_identificador_retirado_nunca_e_reutilizado():
    """Q4: a mutação alvo é permitir re-adicionar um id aposentado. Se
    `adicionar` parar de checar `aposentados`, este teste falha."""
    c = Conjunto()
    c.adicionar(Requisito("R1", "x", criterio(), Origem.DECIDIDA_POR_HUMANO, None))
    c.retirar("R1")
    with pytest.raises(IdentificadorReciclado):
        c.adicionar(Requisito("R1", "outro enunciado", criterio(), Origem.DECIDIDA_POR_HUMANO, None))


def test_conjunto_com_pendencia_aberta_nao_e_completo():
    """Q2: pendência aberta bloqueia completude, mesmo com todo requisito
    tendo rastro para frente."""
    c = Conjunto()
    r = Requisito("R1", "x", criterio(), Origem.DECIDIDA_POR_HUMANO, None, verificacao_id="V1")
    c.adicionar(r)
    c.registrar_pendencia("L7", peso=5)
    assert c.completo() is False


def test_conjunto_com_requisito_sem_verificacao_nao_e_completo():
    """Q3: rastro para frente ausente também bloqueia completude, mesmo sem
    nenhuma pendência declarada — as duas condições são independentes."""
    c = Conjunto()
    c.adicionar(Requisito("R1", "x", criterio(), Origem.DECIDIDA_POR_HUMANO, None, verificacao_id=None))
    assert c.pendencias == []
    assert c.completo() is False


def test_conjunto_sem_pendencia_e_com_todo_rastro_e_completo():
    c = Conjunto()
    c.adicionar(Requisito("R1", "x", criterio(), Origem.DECIDIDA_POR_HUMANO, None, verificacao_id="V1"))
    assert c.completo() is True


def test_sem_rastro_para_frente_lista_exatamente_os_pendentes():
    c = Conjunto()
    c.adicionar(Requisito("R1", "x", criterio(), Origem.DECIDIDA_POR_HUMANO, None, verificacao_id="V1"))
    c.adicionar(Requisito("R2", "y", criterio(), Origem.DECIDIDA_POR_HUMANO, None, verificacao_id=None))
    pendentes = c.sem_rastro_para_frente()
    assert [r.id for r in pendentes] == ["R2"]


def test_mudanca_sem_razao_e_rejeitada():
    """Q7: razão vazia não é razão."""
    c = Conjunto()
    with pytest.raises(ValueError, match="Q7"):
        c.registrar_mudanca("R1", "")


def test_mudanca_com_razao_fica_registrada():
    c = Conjunto()
    c.registrar_mudanca("R1", "cliente mudou o critério de aprovação em reunião de 02/08")
    assert c.mudancas == [("R1", "cliente mudou o critério de aprovação em reunião de 02/08")]
