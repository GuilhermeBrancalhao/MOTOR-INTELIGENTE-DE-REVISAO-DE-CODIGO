import pytest

from roadmap import (
    AutoridadeNaoDeclarada,
    CriterioDePriorizacao,
    CriterioDePriorizacaoAusente,
    DataComprometidaIndevida,
    DecisaoQueExigeAutoridade,
    DependenciaEntreCiclos,
    DependenciaEntreCiclosIncompleta,
    ItemDeRoadmap,
    ItemForaDeEscopo,
    MotivoForaDeEscopoAusente,
    Roadmap,
    RevisaoDeRoadmap,
    RevisaoDeRoadmapIncompleta,
    registrar_revisao_de_roadmap,
)


def criterio(item="painel-de-custo", valor="alto", risco="baixo", dependencia="nenhuma"):
    return CriterioDePriorizacao(item, valor, risco, dependencia)


def test_criterio_de_priorizacao_incompleto_e_rejeitado():
    """AA1: a mutação alvo é aceitar critério com valor, risco ou dependência vazio."""
    with pytest.raises(CriterioDePriorizacaoAusente):
        CriterioDePriorizacao(item="x", valor="", risco="baixo", dependencia="nenhuma")


def test_item_direcional_com_data_comprometida_e_rejeitado():
    """AA5: a mutação alvo é aceitar item direcional com data comprometida."""
    with pytest.raises(DataComprometidaIndevida):
        ItemDeRoadmap(
            nome="painel-de-custo", criterio=criterio(), horizonte="DIRECIONAL_LONGO_PRAZO",
            data_comprometida="2027-01-01",
        )


def test_item_comprometido_com_data_e_aceito():
    item = ItemDeRoadmap(
        nome="painel-de-custo", criterio=criterio(), horizonte="COMPROMETIDO_CURTO_PRAZO",
        data_comprometida="2026-09-01",
    )
    assert item.data_comprometida == "2026-09-01"


def test_item_fora_de_escopo_sem_motivo_e_rejeitado():
    """AA2: a mutação alvo é aceitar ItemForaDeEscopo sem motivo."""
    roadmap = Roadmap()
    with pytest.raises(MotivoForaDeEscopoAusente):
        roadmap.registrar_fora_de_escopo(ItemForaDeEscopo(nome="x", motivo=""))


def test_decisao_sem_autoridade_declarada_e_rejeitada():
    """AA3: a mutação alvo é aceitar DecisaoQueExigeAutoridade sem autoridade nomeada."""
    roadmap = Roadmap()
    with pytest.raises(AutoridadeNaoDeclarada):
        roadmap.sinalizar_decisao_de_autoridade(
            DecisaoQueExigeAutoridade(nome="x", motivo="fora do escopo do processo", autoridade_necessaria="")
        )


def test_revisao_com_atraso_sem_motivo_e_rejeitada():
    """AA4: a mutação alvo é aceitar revisão com item atrasado e sem motivo."""
    historico = []
    with pytest.raises(RevisaoDeRoadmapIncompleta):
        registrar_revisao_de_roadmap(
            historico,
            RevisaoDeRoadmap(data="2026-08-04", itens_entregues=(), itens_atrasados=("x",)),
        )
    assert historico == []


def test_revisao_sem_atraso_nao_exige_motivo():
    historico = []
    registrar_revisao_de_roadmap(
        historico,
        RevisaoDeRoadmap(data="2026-08-04", itens_entregues=("x",), itens_atrasados=()),
    )
    assert len(historico) == 1


def test_dependencia_entre_ciclos_incompleta_e_rejeitada():
    """AA6: a mutação alvo é aceitar DependenciaEntreCiclos com campo vazio."""
    with pytest.raises(DependenciaEntreCiclosIncompleta):
        DependenciaEntreCiclos(item_dependente="x", item_do_qual_depende="", ciclo_de_origem="2026-Q3")
