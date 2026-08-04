import pytest

from fila_de_trabalhos import (
    CapacidadeInsuficiente,
    EstadoDoTrabalho,
    FilaDeTrabalhos,
    Trabalho,
    TransicaoInvalida,
)


def trabalho(id_="t1", chave="chave-1", max_tentativas=3):
    return Trabalho(id=id_, chave_idempotencia=chave, max_tentativas=max_tentativas)


def test_trabalho_com_mesma_chave_nao_duplica():
    """S4: a mutação alvo é enfileirar criar novo trabalho mesmo com chave já ativa."""
    fila = FilaDeTrabalhos()
    original = fila.enfileirar(trabalho(id_="t1", chave="pedido-42"))
    duplicata = fila.enfileirar(trabalho(id_="t2", chave="pedido-42"))
    assert duplicata is original
    assert len(fila.trabalhos) == 1


def test_retirar_proximo_transita_para_executando():
    fila = FilaDeTrabalhos()
    fila.enfileirar(trabalho())
    t = fila.retirar_proximo()
    assert t.estado == EstadoDoTrabalho.EXECUTANDO


def test_concluir_trabalho_fora_de_executando_falha():
    """S5: a mutação alvo é permitir concluir um trabalho que nunca foi retirado da fila."""
    fila = FilaDeTrabalhos()
    fila.enfileirar(trabalho())
    with pytest.raises(TransicaoInvalida):
        fila.marcar_concluido("t1", resultado={"ok": True})


def test_falha_com_tentativas_restantes_reenfileira():
    fila = FilaDeTrabalhos()
    fila.enfileirar(trabalho(max_tentativas=3))
    fila.retirar_proximo()
    fila.marcar_falha("t1")
    assert fila.consultar_estado("t1") == EstadoDoTrabalho.ENFILEIRADO
    assert fila.trabalhos["t1"].tentativas == 1


def test_falha_apos_esgotar_tentativas_vai_para_estado_terminal():
    """S6: a mutação alvo é continuar reenfileirando após esgotar max_tentativas."""
    fila = FilaDeTrabalhos()
    fila.enfileirar(trabalho(max_tentativas=2))
    for _ in range(2):
        fila.retirar_proximo()
        fila.marcar_falha("t1")
    assert fila.consultar_estado("t1") == EstadoDoTrabalho.FALHOU_PERMANENTEMENTE
    # permanece consultavel, nao removido
    assert "t1" in fila.trabalhos


def test_backpressure_rejeita_quando_limite_atingido():
    """S3: a mutação alvo é permitir retirar mais trabalhos do que o limite configurado."""
    fila = FilaDeTrabalhos(limite_concorrente=1)
    fila.enfileirar(trabalho(id_="t1", chave="c1"))
    fila.enfileirar(trabalho(id_="t2", chave="c2"))
    fila.retirar_proximo()  # t1 -> EXECUTANDO, limite atingido
    with pytest.raises(CapacidadeInsuficiente):
        fila.retirar_proximo()


def test_qualquer_chamada_pode_retirar_trabalho_sem_afinidade():
    """S2: duas retiradas simuladas como workers diferentes, sem estado compartilhado entre elas."""
    fila = FilaDeTrabalhos(limite_concorrente=5)
    fila.enfileirar(trabalho(id_="t1", chave="c1"))
    fila.enfileirar(trabalho(id_="t2", chave="c2"))

    trabalho_worker_a = fila.retirar_proximo()
    fila.marcar_falha(trabalho_worker_a.id)  # worker A falha e "morre"

    # worker B, sem nenhum conhecimento do worker A, retira o proximo disponivel
    trabalho_worker_b = fila.retirar_proximo()
    assert trabalho_worker_b is not None
    assert trabalho_worker_b.estado == EstadoDoTrabalho.EXECUTANDO


def test_consultar_estado_nao_bloqueia():
    """S1: confirma que o estado e consultavel imediatamente, mesmo ainda EXECUTANDO."""
    fila = FilaDeTrabalhos()
    fila.enfileirar(trabalho())
    fila.retirar_proximo()
    assert fila.consultar_estado("t1") == EstadoDoTrabalho.EXECUTANDO
