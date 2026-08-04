import pytest

from governanca_ia import (
    AprovacaoAusente,
    CasoDeUso,
    CasoDeUsoNaoClassificado,
    DecisaoAutomatizada,
    DonoResponsavelAusente,
    NivelDeRisco,
    RegistroDeCasosDeUso,
    RevisaoHumanaAusente,
    RevisaoPeriodica,
)


def caso(nome="credito", risco=NivelDeRisco.ALTO, dono="time-risco"):
    return CasoDeUso(nome=nome, nivel_de_risco=risco, dono_responsavel=dono)


def test_caso_de_uso_sem_dono_e_rejeitado():
    """G1: a mutação alvo é aceitar CasoDeUso sem dono_responsavel."""
    registro = RegistroDeCasosDeUso()
    with pytest.raises(DonoResponsavelAusente):
        registro.registrar_caso(caso(dono=""))


def test_verificar_producao_para_caso_nao_classificado_e_rejeitado():
    """G2: a mutação alvo é permitir verificação de produção sem registro prévio."""
    registro = RegistroDeCasosDeUso()
    with pytest.raises(CasoDeUsoNaoClassificado):
        registro.verificar_pronto_para_producao("caso-inexistente")


def test_decisao_de_alto_risco_sem_revisao_humana_e_rejeitada():
    """G3: a mutação alvo é aceitar decisão de risco ALTO sem revisão humana."""
    registro = RegistroDeCasosDeUso()
    registro.registrar_caso(caso(risco=NivelDeRisco.ALTO))
    decisao = DecisaoAutomatizada(
        caso_de_uso="credito", entrada={"renda": 5000}, modelo_usado="modelo-x",
        decisao="negado", revisada_por_humano=False,
    )
    with pytest.raises(RevisaoHumanaAusente):
        registro.registrar_decisao(decisao)


def test_decisao_de_baixo_risco_nao_exige_revisao_humana():
    registro = RegistroDeCasosDeUso()
    registro.registrar_caso(caso(nome="recomendacao", risco=NivelDeRisco.BAIXO))
    decisao = DecisaoAutomatizada(
        caso_de_uso="recomendacao", entrada={"historico": []}, modelo_usado="modelo-x",
        decisao="produto-A", revisada_por_humano=False,
    )
    registro.registrar_decisao(decisao)  # nao levanta
    assert len(registro.trilha_de_auditoria) == 1


def test_toda_decisao_registrada_fica_na_trilha_de_auditoria():
    """G4: confirma que a decisão aceita preserva contexto completo no histórico."""
    registro = RegistroDeCasosDeUso()
    registro.registrar_caso(caso(risco=NivelDeRisco.ALTO))
    decisao = DecisaoAutomatizada(
        caso_de_uso="credito", entrada={"renda": 8000}, modelo_usado="modelo-y",
        decisao="aprovado", revisada_por_humano=True,
    )
    registro.registrar_decisao(decisao)
    assert registro.trilha_de_auditoria[0].modelo_usado == "modelo-y"
    assert registro.trilha_de_auditoria[0].entrada == {"renda": 8000}


def test_producao_sem_aprovacao_explicita_e_rejeitada():
    """G5: a mutação alvo é permitir produção sem aprovação explícita registrada."""
    registro = RegistroDeCasosDeUso()
    registro.registrar_caso(caso())
    with pytest.raises(AprovacaoAusente):
        registro.verificar_pronto_para_producao("credito")


def test_producao_com_aprovacao_e_permitida():
    registro = RegistroDeCasosDeUso()
    registro.registrar_caso(caso())
    registro.aprovar_para_producao("credito", aprovado=True)
    registro.verificar_pronto_para_producao("credito")  # nao levanta


def test_revisao_periodica_acumula_historico():
    """G6: a mutação alvo é a segunda revisão substituir a primeira em vez de acumular."""
    registro = RegistroDeCasosDeUso()
    registro.registrar_caso(caso())
    registro.revisar_periodicamente(
        RevisaoPeriodica("credito", "2026-08-04", NivelDeRisco.ALTO, "time-risco")
    )
    registro.revisar_periodicamente(
        RevisaoPeriodica("credito", "2026-09-04", NivelDeRisco.ALTO, "time-risco")
    )
    assert len(registro.historico_de_revisoes) == 2
    assert registro.historico_de_revisoes[0].data == "2026-08-04"
    assert registro.historico_de_revisoes[1].data == "2026-09-04"
