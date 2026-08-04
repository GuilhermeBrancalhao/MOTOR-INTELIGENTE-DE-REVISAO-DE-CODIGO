import pytest

from catalogo_de_templates import (
    ConteudoDeDominioDetectado,
    ConteudoGeradoDeTemplate,
    DepreciacaoSemMotivo,
    Template,
    TemplateIncompleto,
    VariavelAusente,
    VersaoDeTemplateIncompativel,
    renderizar,
    verificar_compatibilidade,
)


def template(nome="carta-de-boas-vindas", versao="1.0", corpo="Ola {nome_do_usuario}, bem-vindo."):
    return Template(
        nome=nome, versao=versao, corpo=corpo,
        variaveis_obrigatorias=frozenset({"nome_do_usuario"}), escopo_declarado="email transacional simples",
    )


def test_template_incompleto_e_rejeitado():
    """AB1/AB6: a mutação alvo é aceitar Template sem versão ou escopo."""
    with pytest.raises(TemplateIncompleto):
        Template(nome="x", versao="", corpo="y", variaveis_obrigatorias=frozenset(), escopo_declarado="z")


def test_depreciacao_sem_motivo_e_rejeitada():
    """AB5: a mutação alvo é aceitar depreciado=True sem motivo."""
    with pytest.raises(DepreciacaoSemMotivo):
        Template(
            nome="antigo", versao="1.0", corpo="x", variaveis_obrigatorias=frozenset(),
            escopo_declarado="y", depreciado=True, motivo_de_depreciacao=None,
        )


def test_template_com_conteudo_de_dominio_e_rejeitado():
    """AB4: a mutação alvo é aceitar corpo com termo de domínio proibido."""
    with pytest.raises(ConteudoDeDominioDetectado):
        Template(
            nome="x", versao="1.0", corpo="Relatorio de Conciliacao Sicoob",
            variaveis_obrigatorias=frozenset(), escopo_declarado="y",
        )


def test_renderizar_sem_variavel_obrigatoria_e_rejeitado():
    """AB3: a mutação alvo é renderizar com placeholder vazio em vez de rejeitar."""
    with pytest.raises(VariavelAusente):
        renderizar(template(), valores={})


def test_renderizar_com_variaveis_completas_funciona():
    resultado = renderizar(template(), valores={"nome_do_usuario": "Maria"})
    assert resultado == "Ola Maria, bem-vindo."


def test_verificar_compatibilidade_detecta_versao_diferente():
    """AB2: a mutação alvo é aceitar conteúdo de versão antiga como compatível."""
    t = template(versao="2.0")
    conteudo = ConteudoGeradoDeTemplate(template_nome="carta-de-boas-vindas", template_versao="1.0", conteudo="...")
    with pytest.raises(VersaoDeTemplateIncompativel):
        verificar_compatibilidade(conteudo, t)


def test_verificar_compatibilidade_aceita_mesma_versao():
    t = template(versao="1.0")
    conteudo = ConteudoGeradoDeTemplate(template_nome="carta-de-boas-vindas", template_versao="1.0", conteudo="...")
    verificar_compatibilidade(conteudo, t)  # nao levanta
