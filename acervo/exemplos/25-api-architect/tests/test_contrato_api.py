import pytest

from contrato_api import (
    ContratoDeEndpoint,
    MudancaQuebraContrato,
    OrcamentoDeLatenciaAusente,
    VersaoDeContrato,
    declarar_endpoint_sincrono,
    formatar_erro,
    status_do_trabalho,
    traduzir_para_resposta,
)


def contrato():
    return ContratoDeEndpoint(nome="consulta-resultado", versao_atual=VersaoDeContrato(1, 0))


def test_campo_com_tipo_diferente_na_mesma_versao_e_rejeitado():
    """T1/T5: a mutação alvo é aceitar redeclaração de tipo diferente sem exceção."""
    c = contrato()
    c.declarar_campo("status", "str")
    with pytest.raises(MudancaQuebraContrato):
        c.declarar_campo("status", "int")


def test_campo_com_mesmo_tipo_pode_ser_redeclarado():
    c = contrato()
    c.declarar_campo("status", "str")
    c.declarar_campo("status", "str")  # nao levanta
    assert c.campos_expostos["status"] == "str"


def test_traducao_nunca_expoe_campo_nao_permitido():
    """T2: a mutação alvo é copiar o registro interno inteiro para a resposta."""
    registro_interno = {
        "id": "r1",
        "conteudo": "resultado",
        "versao_do_registro": 4,
        "chave_idempotencia": "pedido-42",
    }
    resposta = traduzir_para_resposta(registro_interno, campos_permitidos={"id", "conteudo"})
    assert resposta == {"id": "r1", "conteudo": "resultado"}
    assert "versao_do_registro" not in resposta
    assert "chave_idempotencia" not in resposta


def test_erro_de_diferentes_origens_tem_mesmo_formato():
    """T3: a mutação alvo é retornar um formato de erro diferente por origem."""
    erro_a = formatar_erro("VALIDACAO_FALHOU", "campo obrigatorio ausente")
    erro_b = formatar_erro("CONFLITO_DE_VERSAO", "versao esperada nao confere", {"versao": 3})
    assert type(erro_a) is type(erro_b)
    assert set(vars(erro_a)) == set(vars(erro_b))


def test_status_de_trabalho_e_recurso_consultavel_em_qualquer_estado():
    """T4: confirma estrutura consistente independente do estado."""
    r1 = status_do_trabalho("t1", "ENFILEIRADO")
    r2 = status_do_trabalho("t2", "FALHOU_PERMANENTEMENTE")
    assert r1.url_consulta == "/trabalhos/t1"
    assert r2.url_consulta == "/trabalhos/t2"
    assert set(vars(r1)) == set(vars(r2))


def test_endpoint_sincrono_sem_orcamento_de_latencia_e_rejeitado():
    """T6: a mutação alvo é aceitar limite_ms=None sem exceção."""
    with pytest.raises(OrcamentoDeLatenciaAusente):
        declarar_endpoint_sincrono("consulta-rapida", limite_ms=None)


def test_endpoint_sincrono_com_orcamento_e_aceito():
    orcamento = declarar_endpoint_sincrono("consulta-rapida", limite_ms=300)
    assert orcamento.limite_ms == 300
