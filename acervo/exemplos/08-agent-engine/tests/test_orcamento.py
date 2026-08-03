import pytest

from orcamento import Dimensao, Guardiao, Orcamento, OrcamentoInvalido

CHEIO = Orcamento.criar(passos=10, tokens=1000, tempo_s=30.0)


def test_orcamento_com_dimensao_zerada_nao_inicia():
    with pytest.raises(OrcamentoInvalido):
        Orcamento.criar(passos=0, tokens=1000, tempo_s=30.0)


@pytest.mark.parametrize(
    "kwargs, esperada",
    [
        (dict(passos=10), Dimensao.PASSOS),
        (dict(tokens=1000), Dimensao.TOKENS),
        (dict(tempo_s=30.0), Dimensao.TEMPO),
    ],
)
def test_cada_dimensao_estoura_sozinha(kwargs, esperada):
    """Prova que as tres sao independentes: zerar uma, com as outras duas
    intactas, encerra. Um teste unico que zerasse as tres juntas nao provaria
    que cada uma e verificada -- passaria mesmo se so uma fosse."""
    assert CHEIO.consumir(**kwargs).estourou() is esperada


def test_orcamento_cheio_nao_estourou():
    assert CHEIO.estourou() is None


def test_consumir_nao_muta_o_anterior():
    """A trilha guarda o orcamento de cada passo; mutar destruiria o historico."""
    depois = CHEIO.consumir(passos=1, tokens=10, tempo_s=1.0)
    assert CHEIO.passos == 10 and CHEIO.tokens == 1000
    assert depois.passos == 9 and depois.tokens == 990


def test_guardiao_barra_antes_de_qualquer_acao_quando_ja_estourado():
    g = Guardiao(CHEIO.consumir(passos=10))
    assert g.pode_seguir() is False


def test_ferramenta_lenta_estoura_tempo_sem_estourar_passos():
    """O contraexemplo que justifica a dimensao de tempo: um unico passo, poucos
    tokens, e o orcamento de tempo de parede acabou."""
    g = Guardiao(CHEIO)
    g.registrar_passo(tokens=5, tempo_s=40.0)
    assert g.orcamento.passos == 9        # sobra passo
    assert g.orcamento.tokens == 995      # sobra token
    assert g.pode_seguir() is False       # mas o tempo acabou
    assert g.orcamento.estourou() is Dimensao.TEMPO
