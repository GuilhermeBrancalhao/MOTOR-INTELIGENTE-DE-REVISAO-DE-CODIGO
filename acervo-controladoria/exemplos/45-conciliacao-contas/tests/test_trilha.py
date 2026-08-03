from datetime import datetime

import pytest

from trilha import Trilha


def test_registrar_marca_como_processado():
    trilha = Trilha()
    trilha.registrar("CHAVE-1", "usuario1", datetime(2026, 8, 3, 10, 0), "BAIXA")
    assert trilha.ja_processado("CHAVE-1") is True


def test_registrar_a_mesma_chave_de_novo_e_erro():
    """A trilha e a unica fonte de idempotencia -- registrar a mesma chave duas
    vezes tem de falhar alto, nao ignorar silenciosamente."""
    trilha = Trilha()
    trilha.registrar("CHAVE-1", "usuario1", datetime(2026, 8, 3, 10, 0), "BAIXA")
    with pytest.raises(ValueError):
        trilha.registrar("CHAVE-1", "usuario1", datetime(2026, 8, 3, 10, 5), "BAIXA")


def test_historico_preserva_ordem_de_insercao():
    trilha = Trilha()
    trilha.registrar("A", "u", datetime(2026, 8, 3, 9, 0), "CRIAR")
    trilha.registrar("B", "u", datetime(2026, 8, 3, 9, 5), "BAIXA")
    assert [r.chave for r in trilha.historico()] == ["A", "B"]


def test_indice_remoto_pode_perder_a_chave_mas_a_trilha_local_nao():
    """Simula o caso real: um sistema externo apaga a referencia apos a
    escrita. A trilha local continua respondendo corretamente mesmo que o
    indice remoto (aqui um dict simulando o indice) nao tenha mais nada."""
    trilha = Trilha()
    indice_remoto = {"CHAVE-1": "referencia"}
    trilha.registrar("CHAVE-1", "u", datetime(2026, 8, 3, 9, 0), "BAIXA")
    indice_remoto.clear()
    assert trilha.ja_processado("CHAVE-1") is True
    assert "CHAVE-1" not in indice_remoto
