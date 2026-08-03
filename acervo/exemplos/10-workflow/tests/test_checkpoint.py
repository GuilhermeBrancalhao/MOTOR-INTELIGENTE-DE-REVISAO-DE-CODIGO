import pytest

from checkpoint import (
    Armazem,
    Checkpoint,
    CicloDeCorrecao,
    EstadoWorkflow,
    FalhaNaGravacao,
    TipoPasso,
    avancar,
    passo_a_retomar,
    validar_saida,
)


def ck(passo, **estado):
    return Checkpoint("wf-1", passo, dict(estado))


def test_avanco_normal_confirma_o_checkpoint():
    a = Armazem()
    avancar(a, ck("passo-2", extraido=True))
    assert a.ultimo_confirmado().passo_atual == "passo-2"


def test_falha_entre_gravar_e_confirmar_faz_a_retomada_reexecutar():
    """A garantia central, testada no ponto exato onde vive.

    Se alguem inverter a ordem para "avancar, depois confirmar", a retomada
    passaria a pular o passo -- que e o cenario perigoso. Aqui, com a ordem
    correta, a retomada volta ao passo anterior: custo de uma reexecucao,
    nunca o de avancar sobre passo que pode nao ter terminado.
    """
    a = Armazem()
    avancar(a, ck("passo-1", extraido=True))
    with pytest.raises(FalhaNaGravacao):
        avancar(a, ck("passo-2", classificado=True), falhar_antes_de_confirmar=True)
    assert passo_a_retomar(a, "passo-1") == "passo-1"


def test_gravacao_interrompida_nao_corrompe_o_checkpoint_anterior():
    """Escrever o novo antes de invalidar o anterior: sempre existe um completo."""
    a = Armazem()
    avancar(a, ck("passo-1", extraido=True))
    with pytest.raises(FalhaNaGravacao):
        avancar(a, ck("passo-2"), falhar_antes_de_confirmar=True)
    anterior = a.ultimo_confirmado()
    assert anterior.passo_atual == "passo-1"
    assert anterior.estado_acumulado == {"extraido": True}


def test_sem_checkpoint_a_retomada_comeca_do_inicio():
    assert passo_a_retomar(Armazem(), "passo-1") == "passo-1"


def test_retomada_nao_depende_de_memoria_do_processo():
    """O armazem sobrevive; quem gravou some. Se o estado necessario para retomar
    vivesse numa variavel do processo original, ele nao estaria aqui."""
    def processo_que_grava(a):
        contexto_local = {"categoria": "fiscal", "campos": 2}
        avancar(a, ck("passo-3", **contexto_local))

    a = Armazem()
    processo_que_grava(a)  # o escopo local morre ao retornar
    assert a.ultimo_confirmado().estado_acumulado == {"categoria": "fiscal", "campos": 2}


def test_passo_de_ia_com_saida_malformada_e_rejeitado():
    assert validar_saida(TipoPasso.IA, {"categoria": "x"}, {"categoria", "data"}) is False


def test_passo_deterministico_nao_passa_pela_validacao_de_formato():
    """A mesma saida incompleta que reprova no passo de IA e aceita no
    deterministico -- porque a garantia dele vem da natureza do passo."""
    incompleta = {"categoria": "x"}
    formato = {"categoria", "data"}
    assert validar_saida(TipoPasso.IA, incompleta, formato) is False
    assert validar_saida(TipoPasso.DETERMINISTICO, incompleta, formato) is True


def test_correcao_automatica_tem_limite_e_cai_para_pausa():
    c = CicloDeCorrecao(limite=2)
    assert c.tentar() is True
    assert c.tentar() is True
    assert c.tentar() is False
    assert c.estado_final() is EstadoWorkflow.PAUSADO
