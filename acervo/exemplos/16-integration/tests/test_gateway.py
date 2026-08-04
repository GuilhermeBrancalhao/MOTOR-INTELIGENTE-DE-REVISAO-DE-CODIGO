import pytest

from gateway import (
    CircuitBreaker,
    CircuitoAberto,
    Gateway,
    PoliticaDeRetry,
    VersaoContrato,
    VersaoIncompativel,
)


def gateway(limiar=3, versao_minima=VersaoContrato(2, 0)):
    return Gateway(versao_minima, CircuitBreaker(limiar_abertura=limiar, tempo_espera_s=30.0))


def resposta_ok(versao=VersaoContrato(2, 3)):
    return {"dados": {"ok": True}, "versao": versao}


def test_politica_de_retry_sem_timeout_e_rejeitada():
    with pytest.raises(ValueError):
        PoliticaDeRetry(timeout_s=0, max_tentativas=3, backoff_inicial_s=1.0)


def test_chamada_com_versao_compativel_funciona():
    gw = gateway()
    r = gw.chamar("pedido-123", lambda: resposta_ok())
    assert r["dados"]["ok"] is True


def test_versao_incompativel_e_rejeitada():
    """I1: major diferente é sempre incompatível, mesmo com minor maior."""
    gw = gateway(versao_minima=VersaoContrato(2, 0))
    with pytest.raises(VersaoIncompativel):
        gw.chamar("pedido-1", lambda: resposta_ok(versao=VersaoContrato(3, 0)))


def test_chamada_repetida_com_mesma_chave_nao_duplica_efeito():
    """I2: a mutação alvo é gerar chave nova a cada chamada — este teste
    falha se isso acontecer, porque a segunda chamada teria que executar
    de novo em vez de usar o cache."""
    contador = {"chamadas": 0}

    def executar():
        contador["chamadas"] += 1
        return resposta_ok()

    gw = gateway()
    gw.chamar("pedido-123", executar)
    gw.chamar("pedido-123", executar)  # mesma chave
    assert contador["chamadas"] == 1


def test_circuito_abre_apos_limiar_de_falhas_consecutivas():
    """I4: apos o limiar, chamadas falham imediatamente sem tentar."""
    gw = gateway(limiar=2)

    def falha():
        raise ConnectionError("timeout simulado")

    for i in range(2):
        with pytest.raises(ConnectionError):
            gw.chamar(f"tentativa-{i}", falha)

    assert gw.circuito.estado.value == "ABERTO"
    with pytest.raises(CircuitoAberto):
        gw.chamar("tentativa-nova", lambda: resposta_ok())  # nem chega a tentar


def test_sucesso_reseta_contagem_de_falhas():
    gw = gateway(limiar=3)

    def falha():
        raise ConnectionError("timeout")

    with pytest.raises(ConnectionError):
        gw.chamar("t1", falha)
    assert gw.circuito.falhas_consecutivas == 1

    gw.chamar("t2", lambda: resposta_ok())
    assert gw.circuito.falhas_consecutivas == 0
