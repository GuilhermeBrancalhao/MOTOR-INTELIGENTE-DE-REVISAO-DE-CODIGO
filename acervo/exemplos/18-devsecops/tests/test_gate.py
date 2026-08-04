from gate import Controle, GateDeSeguranca, Waiver


def gate_com(*controles):
    return GateDeSeguranca(list(controles))


def test_controle_automatizado_que_passa_e_aprovado():
    g = gate_com(Controle("isolamento-dado", "prompt injection", "check-isolamento"))
    r = g.avaliar(resultados={"check-isolamento": True}, waivers=[], data_atual="2026-08-04")
    assert r.aprovado is True
    assert r.falhas_bloqueantes == []
    assert r.lacunas == []


def test_controle_sem_verificacao_e_reportado_como_lacuna():
    """D1/D6: a mutação alvo é o gate tratar ausência de verificação automatizada
    como aprovação. Este teste falha se isso acontecer."""
    g = gate_com(Controle("shell-nunca-livre", "execucao insegura", None))
    r = g.avaliar(resultados={}, waivers=[], data_atual="2026-08-04")
    assert r.aprovado is True  # lacuna não é falha bloqueante
    assert len(r.lacunas) == 1
    assert r.lacunas[0].controle == "shell-nunca-livre"


def test_falha_sem_waiver_bloqueia():
    """D2: a mutação alvo é o gate permitir a mudança prosseguir mesmo sem waiver."""
    g = gate_com(Controle("lista-destinos", "exfiltracao", "check-destinos"))
    r = g.avaliar(resultados={"check-destinos": False}, waivers=[], data_atual="2026-08-04")
    assert r.aprovado is False
    assert r.falhas_bloqueantes[0].controle == "lista-destinos"
    assert r.falhas_bloqueantes[0].vetor_de_risco == "exfiltracao"


def test_waiver_ativo_permite_prosseguir_com_excecao_registrada():
    g = gate_com(Controle("lista-destinos", "exfiltracao", "check-destinos"))
    waiver = Waiver("lista-destinos", "aguardando revisao, ticket SEC-142", "2026-08-11")
    r = g.avaliar(
        resultados={"check-destinos": False}, waivers=[waiver], data_atual="2026-08-04"
    )
    assert r.aprovado is True
    assert r.falhas_bloqueantes == []
    assert r.excecoes[0].controle == "lista-destinos"
    assert r.excecoes[0].motivo == "aguardando revisao, ticket SEC-142"


def test_waiver_expirado_nao_impede_bloqueio():
    """D3: a mutação alvo é o gate continuar honrando o waiver após a expiração."""
    g = gate_com(Controle("lista-destinos", "exfiltracao", "check-destinos"))
    waiver = Waiver("lista-destinos", "aguardando revisao, ticket SEC-142", "2026-08-01")
    r = g.avaliar(
        resultados={"check-destinos": False}, waivers=[waiver], data_atual="2026-08-04"
    )
    assert r.aprovado is False
    assert r.falhas_bloqueantes[0].controle == "lista-destinos"
    assert r.excecoes == []


def test_waiver_de_outro_controle_nao_cobre_falha():
    g = gate_com(
        Controle("lista-destinos", "exfiltracao", "check-destinos"),
        Controle("isolamento-dado", "prompt injection", "check-isolamento"),
    )
    waiver = Waiver("isolamento-dado", "motivo qualquer", "2026-12-31")
    r = g.avaliar(
        resultados={"check-destinos": False, "check-isolamento": True},
        waivers=[waiver],
        data_atual="2026-08-04",
    )
    assert r.aprovado is False
    assert r.falhas_bloqueantes[0].controle == "lista-destinos"
