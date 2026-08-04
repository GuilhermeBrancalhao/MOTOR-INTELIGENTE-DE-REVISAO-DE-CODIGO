import pytest

from painel_ia import (
    EstadoCarregamento,
    PromocaoNaoAutorizada,
    RequisicaoDeIA,
    RequisicaoJaFinalizada,
    adaptar_resposta_do_provedor,
    promover_para_global,
    resolver_exibicao,
)


def requisicao_carregando():
    r = RequisicaoDeIA(id="req-1")
    r.iniciar()
    return r


def test_nenhum_resultado_exibido_enquanto_carregando():
    """F1: a mutação alvo é retornar algo diferente de None durante CARREGANDO."""
    r = requisicao_carregando()
    assert resolver_exibicao(r, cache_anterior=None) is None


def test_fragmentos_acumulam_incrementalmente():
    """F2: a mutação alvo é armazenar só o texto final, perdendo o progresso incremental."""
    r = requisicao_carregando()
    r.receber_fragmento("Ola")
    assert r.texto_parcial() == "Ola"
    r.receber_fragmento(", mundo")
    assert r.texto_parcial() == "Ola, mundo"


def test_receber_fragmento_fora_de_carregando_falha():
    r = RequisicaoDeIA(id="req-1")  # ainda OCIOSO
    with pytest.raises(RequisicaoJaFinalizada):
        r.receber_fragmento("x")


def test_falha_sem_cache_nao_produz_fallback_enganoso():
    """F3: a mutação alvo é inventar um resultado quando não há cache para fallback."""
    r = requisicao_carregando()
    r.falhar("provedor indisponivel")
    assert resolver_exibicao(r, cache_anterior=None) is None


def test_falha_com_cache_retorna_fallback_marcado():
    """F3: a mutação alvo é omitir e_fallback=True, tornando o fallback indistinguível."""
    r = requisicao_carregando()
    r.falhar("provedor indisponivel")
    resultado = resolver_exibicao(r, cache_anterior="resposta anterior")
    assert resultado.texto == "resposta anterior"
    assert resultado.e_fallback is True


def test_promocao_sem_autorizacao_e_rejeitada():
    """F4: a mutação alvo é permitir promoção implícita a estado global."""
    r = requisicao_carregando()
    r.receber_fragmento("dado sensivel do componente")
    r.concluir()
    estado_global = {}
    with pytest.raises(PromocaoNaoAutorizada):
        promover_para_global(r, estado_global, chave="resultado", autorizado=False)
    assert estado_global == {}


def test_promocao_autorizada_funciona():
    r = requisicao_carregando()
    r.receber_fragmento("resultado compartilhavel")
    r.concluir()
    estado_global = {}
    promover_para_global(r, estado_global, chave="resultado", autorizado=True)
    assert estado_global["resultado"] == "resultado compartilhavel"


def test_fragmento_apos_cancelamento_e_descartado():
    """F5: a mutação alvo é continuar acumulando fragmento depois de cancelar()."""
    r = requisicao_carregando()
    r.receber_fragmento("antes")
    r.cancelar()
    r.receber_fragmento("depois")  # nao levanta, apenas ignora
    assert r.texto_parcial() == "antes"


def test_cancelamento_impede_conclusao_subsequente():
    """F5: a mutação alvo é permitir concluir() ou falhar() reverter um CANCELADO."""
    r = requisicao_carregando()
    r.cancelar()
    r.concluir()
    assert r.estado == EstadoCarregamento.CANCELADO
    r.falhar("motivo qualquer")
    assert r.estado == EstadoCarregamento.CANCELADO


def test_adaptador_traduz_resposta_bruta_antes_da_ui():
    """F6: a mutação alvo é expor o dicionário bruto do provedor diretamente à UI."""
    bruta = {"choices": [{"delta": {"content": "texto do modelo"}}]}
    adaptador = lambda b: b["choices"][0]["delta"]["content"]
    resultado = adaptar_resposta_do_provedor(bruta, adaptador)
    assert resultado == "texto do modelo"
    assert isinstance(resultado, str)
