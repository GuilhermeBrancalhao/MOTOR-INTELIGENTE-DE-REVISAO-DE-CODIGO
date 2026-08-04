import pytest

from infraestrutura import (
    AlvoDeDisponibilidade,
    MudancaForaDoAmbiente,
    PlanoDeInfraestrutura,
    Recurso,
    RecursoSemDono,
    SegredoInlineDetectado,
    validar_config_sem_segredo,
)


def recurso(nome="db-producao", ambiente="producao", dono="time-plataforma", redundante=True):
    return Recurso(nome=nome, tipo="banco-de-dados", ambiente=ambiente, dono=dono, redundante=redundante)


def test_recurso_sem_dono_e_rejeitado():
    """N3: a mutação alvo é aceitar Recurso construído sem dono."""
    with pytest.raises(RecursoSemDono):
        Recurso(nome="x", tipo="vm", ambiente="producao", dono="", redundante=True)


def test_segredo_inline_e_detectado():
    """N5: a mutação alvo é aceitar configuração com chave de segredo em texto plano."""
    with pytest.raises(SegredoInlineDetectado):
        validar_config_sem_segredo({"nome": "db", "senha": "abc123"})


def test_config_sem_segredo_passa():
    validar_config_sem_segredo({"nome": "db", "ambiente": "producao"})  # nao levanta


def test_redundancia_ausente_e_reportada_para_alvo_critico():
    """N2: a mutação alvo é não sinalizar recurso sem redundância quando o alvo exige."""
    r = recurso(redundante=False)
    plano = PlanoDeInfraestrutura([r])
    alvo = AlvoDeDisponibilidade("producao-critica", exige_redundancia=True)
    faltantes = plano.verificar_redundancia(alvo)
    assert faltantes == [r]


def test_redundancia_nao_exigida_para_alvo_sem_requisito():
    r = recurso(redundante=False)
    plano = PlanoDeInfraestrutura([r])
    alvo = AlvoDeDisponibilidade("staging-sem-sla", exige_redundancia=False)
    assert plano.verificar_redundancia(alvo) == []


def test_mudanca_fora_do_ambiente_e_rejeitada():
    """N4: a mutação alvo é aplicar mudança de staging a um alvo de producao."""
    plano = PlanoDeInfraestrutura([recurso(ambiente="producao")])
    mudanca_staging = recurso(ambiente="staging")
    with pytest.raises(MudancaForaDoAmbiente):
        plano.aplicar_mudanca(mudanca_staging, ambiente_alvo="producao")


def test_drift_detectado_quando_recurso_ausente_do_real():
    """N6: recurso declarado mas nao encontrado no estado real."""
    plano = PlanoDeInfraestrutura([recurso(nome="db-fantasma")])
    divergencias = plano.detectar_drift(estado_real={})
    assert len(divergencias) == 1
    assert divergencias[0].campo == "existencia"


def test_drift_detectado_quando_redundancia_diverge():
    """N6: redundancia declarada diverge do estado real observado."""
    plano = PlanoDeInfraestrutura([recurso(nome="db-x", redundante=True)])
    divergencias = plano.detectar_drift(estado_real={"db-x": {"redundante": False}})
    assert len(divergencias) == 1
    assert divergencias[0].campo == "redundante"
    assert divergencias[0].declarado is True
    assert divergencias[0].real is False


def test_sem_drift_quando_declarado_bate_com_real():
    plano = PlanoDeInfraestrutura([recurso(nome="db-x", redundante=True)])
    divergencias = plano.detectar_drift(estado_real={"db-x": {"redundante": True}})
    assert divergencias == []
