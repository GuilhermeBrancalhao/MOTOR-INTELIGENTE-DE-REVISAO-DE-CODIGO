import pytest

from limiar import (
    Avaliador,
    CanalFalso,
    Categoria,
    CustoDecomposto,
    Limiar,
    Sinal,
    TipoEtapa,
    somar_tokens,
    tempo_por_tipo,
)

LIMIARES = {
    Categoria.MOTIVO_ENCERRAMENTO: Limiar(
        Categoria.MOTIVO_ENCERRAMENTO, 0.20, base_observacao="p95 observado em 30 dias"
    )
}


def avaliador(disponivel=True):
    return Avaliador(dict(LIMIARES), CanalFalso(disponivel=disponivel))


def sinal(valor):
    return Sinal(Categoria.MOTIVO_ENCERRAMENTO, valor, origem="08-AGENT-ENGINE")


def test_abaixo_do_limiar_nao_alerta():
    r = avaliador().avaliar(sinal(0.10))
    assert r.alertou is False and r.notificado is False


def test_cruzar_o_limiar_dispara_notificacao_de_fato():
    """A mutacao alvo: trocar a chamada de notificacao por um registro em log.
    Este teste falha se isso acontecer, porque verifica a entrega no canal, nao
    a ausencia de excecao."""
    a = avaliador()
    r = a.avaliar(sinal(0.35))
    assert r.alertou is True and r.notificado is True
    assert len(a.canal.entregues) == 1


def test_canal_indisponivel_nao_passa_por_notificado():
    """O cenario mais perigoso: sinal detectado corretamente e ninguem avisado.
    O resultado precisa distinguir 'alertou' de 'notificou'."""
    a = avaliador(disponivel=False)
    r = a.avaliar(sinal(0.35))
    assert r.alertou is True
    assert r.notificado is False
    assert a.alertas_reversos  # a falha do canal virou sinal, nao silencio


def test_heartbeat_falho_gera_alerta_reverso():
    a = avaliador(disponivel=False)
    assert a.verificar_canal() is False
    assert "heartbeat" in a.alertas_reversos[0]


def test_limiar_sem_proveniencia_e_rejeitado():
    """Numero redondo escolhido antes de existir dado e o modo de falha classico."""
    with pytest.raises(ValueError, match="proveniencia"):
        Limiar(Categoria.INTERVENCAO_HUMANA, 10.0, base_observacao="  ")


def test_etapa_deterministica_nao_pode_declarar_tokens():
    with pytest.raises(ValueError, match="nao consome tokens"):
        CustoDecomposto("e1", TipoEtapa.DETERMINISTICO, 1.0, tokens=5)


def test_none_de_tokens_e_nao_aplicavel_nunca_zero():
    """Se `None` virasse zero na soma, a etapa deterministica entraria na media de
    tokens e pareceria artificialmente eficiente."""
    custos = [
        CustoDecomposto("ia", TipoEtapa.IA, 2.0, tokens=800),
        CustoDecomposto("det", TipoEtapa.DETERMINISTICO, 0.5),
    ]
    assert somar_tokens(custos) == 800


def test_decomposicao_separa_os_dois_tipos_de_etapa():
    custos = [
        CustoDecomposto("ia", TipoEtapa.IA, 2.0, tokens=800),
        CustoDecomposto("det", TipoEtapa.DETERMINISTICO, 0.5),
    ]
    por_tipo = tempo_por_tipo(custos)
    assert por_tipo[TipoEtapa.IA] == 2.0
    assert por_tipo[TipoEtapa.DETERMINISTICO] == 0.5
