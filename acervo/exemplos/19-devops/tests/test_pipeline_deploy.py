import dataclasses

import pytest

from pipeline_deploy import (
    Artefato,
    DeployCompletoRequerJustificativa,
    EstagioFalhou,
    EstagioForaDeOrdem,
    Estagio,
    GerenciadorDeploy,
    Pipeline,
    PipelineIncompleto,
    SemVersaoAnteriorParaReverter,
)


def artefato(commit="abc123"):
    return Artefato(hash=f"hash-{commit}", commit=commit)


def pipeline_completo(commit="abc123"):
    p = Pipeline(artefato(commit))
    p.executar_estagio(Estagio.BUILD, True)
    p.executar_estagio(Estagio.TESTE, True)
    p.executar_estagio(Estagio.SEGURANCA, True)
    p.executar_estagio(Estagio.STAGING, True)
    return p


def test_estagio_fora_de_ordem_e_rejeitado():
    """P5: a mutação alvo é aceitar um estágio fora da posição esperada."""
    p = Pipeline(artefato())
    with pytest.raises(EstagioForaDeOrdem):
        p.executar_estagio(Estagio.TESTE, True)  # BUILD deveria vir primeiro


def test_estagio_que_falha_bloqueia_seguinte():
    """P1/P5: a mutação alvo é permitir que TESTE rode apos BUILD falhar."""
    p = Pipeline(artefato())
    with pytest.raises(EstagioFalhou):
        p.executar_estagio(Estagio.BUILD, False)
    with pytest.raises(EstagioForaDeOrdem):
        p.executar_estagio(Estagio.TESTE, True)


def test_pipeline_incompleto_nao_pode_implantar():
    """P1: a mutação alvo é permitir deploy sem todos os estágios anteriores."""
    p = Pipeline(artefato())
    p.executar_estagio(Estagio.BUILD, True)
    gerenciador = GerenciadorDeploy()
    with pytest.raises(PipelineIncompleto):
        p.implantar_em_producao(gerenciador)


def test_deploy_completo_sem_justificativa_e_rejeitado():
    """P3: a mutação alvo é aceitar percentual=100 sem forcar_completo."""
    p = pipeline_completo()
    gerenciador = GerenciadorDeploy()
    with pytest.raises(DeployCompletoRequerJustificativa):
        p.implantar_em_producao(gerenciador, percentual=100)


def test_deploy_gradual_e_aceito_por_padrao():
    p = pipeline_completo()
    gerenciador = GerenciadorDeploy()
    registro = p.implantar_em_producao(gerenciador, percentual=25)
    assert registro.percentual == 25
    assert registro.e_rollback is False


def test_artefato_atual_rastreia_o_que_esta_em_producao():
    """P4: consulta o histórico apos múltiplos deploys."""
    gerenciador = GerenciadorDeploy()
    p1 = pipeline_completo("commit-1")
    p1.implantar_em_producao(gerenciador, percentual=25)

    p2 = pipeline_completo("commit-2")
    registro2 = p2.implantar_em_producao(gerenciador, percentual=25)

    assert gerenciador.artefato_atual() == registro2.artefato
    assert gerenciador.artefato_atual().commit == "commit-2"


def test_reverter_sem_versao_anterior_falha():
    """P2: a mutação alvo é permitir reverter sem histórico anterior."""
    gerenciador = GerenciadorDeploy()
    p = pipeline_completo()
    p.implantar_em_producao(gerenciador, percentual=25)
    with pytest.raises(SemVersaoAnteriorParaReverter):
        gerenciador.reverter()


def test_reverter_restaura_artefato_anterior():
    """P2: reversão promove o artefato do registro anterior, não reconstrói."""
    gerenciador = GerenciadorDeploy()
    p1 = Pipeline(artefato("commit-1"))
    for e in (Estagio.BUILD, Estagio.TESTE, Estagio.SEGURANCA, Estagio.STAGING):
        p1.executar_estagio(e, True)
    p1.implantar_em_producao(gerenciador, percentual=25)

    p2 = Pipeline(artefato("commit-2"))
    for e in (Estagio.BUILD, Estagio.TESTE, Estagio.SEGURANCA, Estagio.STAGING):
        p2.executar_estagio(e, True)
    p2.implantar_em_producao(gerenciador, percentual=25)

    registro = gerenciador.reverter()
    assert registro.artefato.commit == "commit-1"
    assert registro.e_rollback is True


def test_artefato_do_pipeline_e_imutavel():
    """P6: a mutação alvo é permitir reatribuir o artefato de um pipeline existente."""
    p = Pipeline(artefato("commit-1"))
    with pytest.raises(dataclasses.FrozenInstanceError):
        p.artefato = artefato("commit-2")
