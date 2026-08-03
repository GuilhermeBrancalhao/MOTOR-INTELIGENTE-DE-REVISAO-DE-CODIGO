"""Fluxo ponta-a-ponta: ancora fecha o dia -> movimento sem titulo exato tenta
casamento aproximado -> confianca decide se escreve -> guarda impede
duplicata -> trilha registra. Anda pelo caminho inteiro do volume, na ordem em
que ele acontece na operacao real.
"""
from datetime import date, datetime

import pytest

from ancora import Movimento as MovimentoBanco, achar_ancora
from casamento import Movimento as MovimentoCasamento, TituloAberto, casar, similaridade
from confianca import Confianca, Evidencia, classificar
from guarda import ChaveMovimento, GuardaDuplicidade
from trilha import Trilha


def test_fluxo_completo_de_conciliacao_com_escrita():
    saldos_banco = {date(2026, 8, 3): 1080.0}
    ancora = achar_ancora(
        1000.0, date(2026, 8, 1), [MovimentoBanco(date(2026, 8, 3), 80.0)], saldos_banco
    )
    assert ancora is not None

    titulos = [TituloAberto("T1", "PROVEDOR INTERNET FIBRA", 80.0)]
    movimento = MovimentoCasamento("PROVEDOR INTERNET FIBRA", -80.0)
    titulo = casar(movimento, titulos)
    assert titulo is not None

    evidencia = Evidencia(
        match_exato_valor=True,
        similaridade_nome=similaridade(movimento.descricao, titulo.contraparte),
    )
    assert classificar(evidencia) is Confianca.ALTA

    guarda = GuardaDuplicidade()
    chave = ChaveMovimento(date(2026, 8, 3), movimento.valor, titulo.contraparte)
    assert guarda.ja_registrado(chave) is False

    trilha = Trilha()
    guarda.registrar(chave)
    trilha.registrar(f"{titulo.id}:{chave.data}", "usuario1", datetime(2026, 8, 3, 12, 0), "BAIXA")

    # reprocessar o mesmo dia (retry) tem de ser barrado nas duas camadas
    assert guarda.ja_registrado(chave) is True
    with pytest.raises(ValueError):
        trilha.registrar(f"{titulo.id}:{chave.data}", "usuario1", datetime(2026, 8, 3, 12, 5), "BAIXA")


def test_fluxo_nao_escreve_quando_confianca_e_baixa():
    """Sem match de valor e sem nome parecido, o motor nunca chega a chamar
    guarda/trilha -- fica pendencia humana."""
    titulos = [TituloAberto("T1", "FORNECEDOR DESCONHECIDO", 900.0)]
    movimento = MovimentoCasamento("ORIGEM SEM IDENTIFICACAO", -80.0)
    titulo = casar(movimento, titulos)
    assert titulo is None
