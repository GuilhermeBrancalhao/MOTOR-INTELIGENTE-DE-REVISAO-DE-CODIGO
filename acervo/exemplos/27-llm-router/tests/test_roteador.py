import pytest

from roteador import CandidatoNaoAprovado, Roteador, SinalDeSaude


def roteador(aprovados=None):
    return Roteador(candidatos_aprovados=aprovados or {"modelo-principal", "modelo-fallback"})


def sinal(total, falhas, latencia=100.0):
    return SinalDeSaude(total_chamadas=total, falhas=falhas, latencia_media_ms=latencia)


def test_roteamento_para_candidato_nao_aprovado_e_rejeitado():
    """L1: a mutação alvo é aceitar candidato fora da lista aprovada."""
    r = roteador(aprovados={"modelo-principal"})
    with pytest.raises(CandidatoNaoAprovado):
        r.rotear("resumo", "modelo-principal", "modelo-nao-aprovado", sinal(10, 0))


def test_principal_saudavel_e_escolhido():
    r = roteador()
    d = r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(10, 0))
    assert d.candidato_escolhido == "modelo-principal"
    assert d.motivo == "principal_saudavel"


def test_falha_unica_isolada_nao_aciona_fallback():
    """L4: a mutação alvo é tratar uma falha isolada como degradação suficiente."""
    r = roteador()
    d = r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(1, 1))
    assert d.candidato_escolhido == "modelo-principal"


def test_degradacao_sustentada_aciona_fallback():
    """L2: a mutação alvo é manter roteamento no principal apesar de degradacao sustentada."""
    r = roteador()
    d = r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(20, 15))
    assert d.candidato_escolhido == "modelo-fallback"
    assert d.motivo == "fallback_por_degradacao"


def test_recuperacao_exige_janela_de_estabilidade():
    """L5: a mutação alvo é voltar ao principal no primeiro sinal saudável isolado."""
    r = roteador()
    r.janela_estabilidade = 3
    r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(20, 15))  # dispara fallback

    d1 = r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(20, 0))
    assert d1.candidato_escolhido == "modelo-fallback"
    assert d1.motivo == "ainda_em_janela_de_estabilidade"

    d2 = r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(20, 0))
    assert d2.candidato_escolhido == "modelo-fallback"

    d3 = r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(20, 0))
    assert d3.candidato_escolhido == "modelo-principal"
    assert d3.motivo == "recuperado_apos_janela_de_estabilidade"


def test_toda_decisao_fica_registrada_no_historico():
    """L3: a mutação alvo é não registrar alguma decisão no histórico."""
    r = roteador()
    r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(10, 0))
    r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(20, 15))
    assert len(r.historico) == 2
    assert r.historico[0].motivo == "principal_saudavel"
    assert r.historico[1].motivo == "fallback_por_degradacao"


def test_estado_atual_e_consultavel():
    """L6: confirma que estado_de reflete o candidato ativo sem chamada adicional."""
    r = roteador()
    assert r.estado_de("resumo") is None
    r.rotear("resumo", "modelo-principal", "modelo-fallback", sinal(20, 15))
    assert r.estado_de("resumo") == "modelo-fallback"
