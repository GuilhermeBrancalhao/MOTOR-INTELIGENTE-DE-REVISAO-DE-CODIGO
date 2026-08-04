import pytest

from fronteira import (
    MotivoRejeicao,
    SemEfeito,
    aplicar_efeito,
    atravessar_fronteira,
    montar_contexto,
)

CAMPOS = frozenset({"status"})
VALORES = frozenset({"aprovado", "recusado"})
AUTORIZADOS = frozenset({"status"})


def test_contexto_e_deterministico_para_a_mesma_entrada():
    """N6: mesmo dado de entrada produz o mesmo contexto, byte a byte."""
    a = montar_contexto({"pedido": "123", "valor": "50"})
    b = montar_contexto({"valor": "50", "pedido": "123"})  # ordem diferente na entrada
    assert a.texto() == b.texto()


def test_resposta_bem_formada_valida_e_autorizada_atravessa():
    resp, motivo = atravessar_fronteira("status=aprovado", CAMPOS, VALORES, AUTORIZADOS)
    assert motivo is None
    assert resp.campo == "status" and resp.valor == "aprovado"


def test_forma_invalida_rejeita_antes_de_checar_dominio():
    """A ordem importa: forma primeiro. Um texto sem '=' nunca chega perto
    de validar_dominio ou validar_autorizacao."""
    resp, motivo = atravessar_fronteira("isto nao e campo=valor=extra", CAMPOS, VALORES, AUTORIZADOS)
    assert resp is None
    assert motivo is MotivoRejeicao.FORMA


def test_campo_desconhecido_e_falha_de_forma_nao_de_dominio():
    resp, motivo = atravessar_fronteira("campo_fantasma=x", CAMPOS, VALORES, AUTORIZADOS)
    assert motivo is MotivoRejeicao.FORMA


def test_valor_fora_do_dominio_rejeita_mesmo_com_forma_valida():
    resp, motivo = atravessar_fronteira("status=talvez", CAMPOS, VALORES, AUTORIZADOS)
    assert resp is None
    assert motivo is MotivoRejeicao.DOMINIO


def test_campo_nao_autorizado_rejeita_mesmo_com_forma_e_dominio_validos():
    """A mutação alvo: se alguém trocar a ordem para autorização antes de
    domínio, um valor fora do domínio mas de campo autorizado passaria pela
    checagem errada primeiro sem que este teste, isolado, revelasse — por
    isso o teste de domínio acima e este precisam existir separadamente."""
    resp, motivo = atravessar_fronteira("status=aprovado", CAMPOS, VALORES, frozenset())
    assert resp is None
    assert motivo is MotivoRejeicao.AUTORIZACAO


def test_resposta_rejeitada_nunca_produz_efeito():
    """N4 em teste: a única forma de aplicar_efeito não levantar é receber
    uma RespostaValidada de verdade — não um dict, não um texto bruto."""
    with pytest.raises(SemEfeito):
        aplicar_efeito(None, MotivoRejeicao.DOMINIO)


def test_resposta_valida_produz_o_efeito_esperado():
    resp, _ = atravessar_fronteira("status=aprovado", CAMPOS, VALORES, AUTORIZADOS)
    assert aplicar_efeito(resp, None) == "aplicado: status=aprovado"
