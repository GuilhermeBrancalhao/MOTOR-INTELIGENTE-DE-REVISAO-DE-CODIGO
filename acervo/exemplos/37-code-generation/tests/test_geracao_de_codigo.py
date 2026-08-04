import pytest

from geracao_de_codigo import (
    CodigoGerado,
    CodigoNaoMarcado,
    EdicaoManualDeCodigoGerado,
    EspecificacaoDeGeracao,
    EspecificacaoIncompleta,
    ResultadoDeValidacao,
    ResultadoDeValidacaoAusente,
    RevisaoHumanaAusente,
    ValidacaoFalhou,
    aceitar_codigo_gerado,
    editar_codigo_gerado,
    gerar,
)


def especificacao(nome="cliente-api", versao="1.0", escopo="gera stub de cliente REST"):
    return EspecificacaoDeGeracao(
        nome=nome, prompt_ou_fonte="gerar cliente a partir do contrato openapi.yml",
        versao=versao, escopo_declarado=escopo,
    )


def codigo_completo():
    return CodigoGerado(
        especificacao=especificacao(),
        conteudo="class ClienteAPI: ...",
        marcado_como_gerado=True,
        validacao=ResultadoDeValidacao(compilou=True, testes_passaram=True),
        revisado_por_humano=True,
    )


def test_especificacao_incompleta_e_rejeitada():
    """Y5/Y6: a mutação alvo é aceitar especificação sem versão ou escopo."""
    with pytest.raises(EspecificacaoIncompleta):
        EspecificacaoDeGeracao(nome="x", prompt_ou_fonte="y", versao="", escopo_declarado="z")


def test_codigo_nao_marcado_e_rejeitado():
    """Y2: a mutação alvo é aceitar código gerado sem a marcação correspondente."""
    codigo = CodigoGerado(
        especificacao=especificacao(), conteudo="...", marcado_como_gerado=False,
        validacao=ResultadoDeValidacao(True, True), revisado_por_humano=True,
    )
    with pytest.raises(CodigoNaoMarcado):
        aceitar_codigo_gerado(codigo)


def test_codigo_sem_validacao_e_rejeitado():
    """Y1: a mutação alvo é aceitar código sem nenhum resultado de validação."""
    codigo = CodigoGerado(
        especificacao=especificacao(), conteudo="...", marcado_como_gerado=True,
        validacao=None, revisado_por_humano=True,
    )
    with pytest.raises(ResultadoDeValidacaoAusente):
        aceitar_codigo_gerado(codigo)


def test_codigo_com_validacao_falha_e_rejeitado():
    """Y1: a mutação alvo é aceitar código cuja validação falhou."""
    codigo = CodigoGerado(
        especificacao=especificacao(), conteudo="...", marcado_como_gerado=True,
        validacao=ResultadoDeValidacao(compilou=True, testes_passaram=False),
        revisado_por_humano=True,
    )
    with pytest.raises(ValidacaoFalhou):
        aceitar_codigo_gerado(codigo)


def test_codigo_sem_revisao_humana_e_rejeitado():
    """Y4: a mutação alvo é aceitar código validado mas sem revisão humana."""
    codigo = CodigoGerado(
        especificacao=especificacao(), conteudo="...", marcado_como_gerado=True,
        validacao=ResultadoDeValidacao(True, True), revisado_por_humano=False,
    )
    with pytest.raises(RevisaoHumanaAusente):
        aceitar_codigo_gerado(codigo)


def test_codigo_completo_e_aceito():
    aceitar_codigo_gerado(codigo_completo())  # nao levanta


def test_edicao_manual_de_codigo_gerado_e_rejeitada():
    """Y2: a mutação alvo é permitir edição direta sobre código marcado como gerado."""
    with pytest.raises(EdicaoManualDeCodigoGerado):
        editar_codigo_gerado(codigo_completo(), "novo conteudo manual")


def test_geracao_e_deterministica_para_mesma_especificacao():
    """Y3: a mutação alvo é a mesma especificação produzir código diferente entre chamadas."""
    spec = especificacao()
    gerador_deterministico = lambda e: f"# gerado de {e.nome} v{e.versao}\nclass Stub: pass"
    resultado_1 = gerar(spec, gerador_deterministico)
    resultado_2 = gerar(spec, gerador_deterministico)
    assert resultado_1 == resultado_2
