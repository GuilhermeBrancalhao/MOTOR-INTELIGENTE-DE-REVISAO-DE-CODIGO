import pytest

from objetivo import Autoridade, AutoridadeInsuficiente, ObjetivoDeNegocio, Processo, Stakeholder

DECIDE = Stakeholder("Ana", Autoridade.DECIDE)
CONSULTADO = Stakeholder("Bruno", Autoridade.CONSULTADO)
DECIDE_2 = Stakeholder("Carla", Autoridade.DECIDE)


def objetivo(criterio="reduzir tempo de resposta de 4h para 30min no trimestre"):
    return ObjetivoDeNegocio("melhorar suporte", criterio)


def test_objetivo_sem_criterio_nao_e_falsificavel():
    assert ObjetivoDeNegocio("melhorar algo", "").eh_falsificavel() is False


def test_objetivo_com_criterio_e_falsificavel():
    assert objetivo().eh_falsificavel() is True


def test_validar_objetivo_sem_criterio_falha():
    """B2: nenhum objetivo entra validado sem passar no teste."""
    p = Processo()
    with pytest.raises(ValueError, match="critério de falsificação"):
        p.validar(objetivo(criterio=""), DECIDE)


def test_consultado_nao_pode_validar_sozinho():
    """B3, a invariante central. A mutação alvo: trocar a checagem de
    `Autoridade.DECIDE` por 'qualquer stakeholder com objetivo proposto' —
    este teste falha se isso acontecer."""
    p = Processo()
    with pytest.raises(AutoridadeInsuficiente):
        p.validar(objetivo(), CONSULTADO)


def test_decide_valida_objetivo_com_sucesso():
    p = Processo()
    p.validar(objetivo(), DECIDE)
    assert len(p.validados) == 1
    assert p.discordancias_abertas() == ()


def test_dois_decide_com_objetivos_diferentes_gera_discordancia_registrada():
    """B4: o sistema nunca escolhe um lado — registra e para."""
    p = Processo()
    p.validar(objetivo("reduzir tempo"), DECIDE)
    p.validar(objetivo("reduzir custo"), DECIDE_2)
    abertas = p.discordancias_abertas()
    assert len(abertas) == 1
    assert abertas[0].resolvida is False


def test_dois_decide_com_o_mesmo_objetivo_nao_gera_discordancia():
    """Concordância entre dois DECIDE não é discordância — só objetivo
    incompatível dispara o registro."""
    p = Processo()
    obj = objetivo()
    p.validar(obj, DECIDE)
    p.validar(obj, DECIDE_2)
    assert p.discordancias_abertas() == ()


def test_stakeholder_carrega_exatamente_uma_autoridade():
    """B1: o tipo já garante isso — não há como um Stakeholder ter duas
    classificações, o campo é singular por construção."""
    s = Stakeholder("Dora", Autoridade.INFORMADO)
    assert s.autoridade is Autoridade.INFORMADO
