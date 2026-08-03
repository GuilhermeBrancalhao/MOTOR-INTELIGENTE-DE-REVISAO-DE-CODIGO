import pytest

from laco_agente import ChamarFerramenta, Observacao, RespostaFinal, Resultado, executar
from orcamento import Motivo, Orcamento


def modelo_de(*acoes):
    """Modelo fake: devolve a sequencia programada e conta quantas vezes foi
    chamado. Sem isso nao da para provar que o guardiao roda ANTES da chamada."""
    seq = list(acoes)
    chamadas = {"n": 0}

    def modelo(historico):
        chamadas["n"] += 1
        return seq.pop(0) if seq else RespostaFinal("fim")

    modelo.chamadas = chamadas
    return modelo


FERRAMENTAS = {"estoque": lambda produto: Observacao(f"12 unidades de {produto}")}


def test_objetivo_atingido_em_tres_passos():
    m = modelo_de(
        ChamarFerramenta("estoque", {"produto": "X"}),
        RespostaFinal("12 unidades"),
    )
    r = executar(m, FERRAMENTAS, Orcamento.criar(10, 1000, 30.0))
    assert r.motivo is Motivo.OBJETIVO_ATINGIDO
    assert r.saida == "12 unidades"


def test_orcamento_zerado_impede_a_chamada_ao_modelo():
    """A prova por contagem de que o guardiao roda antes, nao depois.

    Se alguem inverter a ordem (chamar o modelo e so entao verificar), este teste
    falha: `chamadas` passaria a ser 1. Esperado zero.
    """
    m = modelo_de(RespostaFinal("nao deveria chegar aqui"))
    orcamento_gasto = Orcamento.criar(10, 1000, 30.0).consumir(passos=10)
    r = executar(m, FERRAMENTAS, orcamento_gasto)
    assert r.motivo is Motivo.ORCAMENTO_EXCEDIDO
    assert m.chamadas["n"] == 0


def test_resultado_incompleto_nunca_carrega_saida():
    r = executar(
        modelo_de(RespostaFinal("x")),
        FERRAMENTAS,
        Orcamento.criar(10, 1000, 30.0).consumir(passos=10),
    )
    assert r.saida is None
    with pytest.raises(ValueError):
        Resultado(Motivo.ORCAMENTO_EXCEDIDO, (), "saida indevida")


def test_erro_de_ferramenta_vira_observacao_e_o_laco_continua():
    """Erro recuperavel nao aborta: volta como observacao e o modelo decide."""
    def quebra(**_):
        raise RuntimeError("timeout de rede")

    m = modelo_de(
        ChamarFerramenta("frágil", {}),
        RespostaFinal("recuperei"),
    )
    r = executar(m, {"frágil": quebra}, Orcamento.criar(10, 1000, 30.0))
    assert r.motivo is Motivo.OBJETIVO_ATINGIDO
    assert r.passos[0].observacao.erro is True
    assert len(r.passos) == 2


def test_resposta_fora_do_contrato_encerra_sem_despachar_ferramenta():
    despachou = {"sim": False}

    def registra(**_):
        despachou["sim"] = True
        return Observacao("ok")

    r = executar(modelo_de("isto nao e uma acao"), {"x": registra}, Orcamento.criar(10, 1000, 30.0))
    assert r.motivo is Motivo.ERRO_NAO_RECUPERAVEL
    assert despachou["sim"] is False


def test_ferramenta_inexistente_e_erro_nao_recuperavel():
    r = executar(
        modelo_de(ChamarFerramenta("nao_existe", {})),
        FERRAMENTAS,
        Orcamento.criar(10, 1000, 30.0),
    )
    assert r.motivo is Motivo.ERRO_NAO_RECUPERAVEL
