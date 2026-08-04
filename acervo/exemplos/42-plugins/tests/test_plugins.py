import pytest

from plugins import (
    CapacidadeNaoDeclarada,
    ContratoDeExtensao,
    ContratoIncompativel,
    DeclaracaoDePlugin,
    EstadoDoHost,
    PluginNaoEncontrado,
    QuebraDeContratoSemMajorBump,
    RegistroImplicito,
    VersaoDeContrato,
    acessar_capacidade,
    ativar_plugin,
    evoluir_contrato,
    executar_hook_isolado,
)


def test_ativar_plugin_com_contrato_incompativel_e_rejeitado():
    """Mutação alvo: aceitar ativação com major do contrato alvo divergente do host (AD1)."""
    contrato_do_host = ContratoDeExtensao(versao=VersaoDeContrato(1, 0))
    declaracao = DeclaracaoDePlugin(
        nome="ExportadorPDF",
        versao_do_contrato_alvo=VersaoDeContrato(2, 0),
        ponto_de_entrada="exportador_pdf:main",
    )

    with pytest.raises(ContratoIncompativel):
        ativar_plugin(contrato_do_host, declaracao)


def test_ativar_plugin_com_contrato_compativel_funciona():
    """Mutação alvo: rejeitar ativação quando major do contrato alvo já coincide (AD1)."""
    contrato_do_host = ContratoDeExtensao(versao=VersaoDeContrato(1, 3))
    declaracao = DeclaracaoDePlugin(
        nome="ExportadorPDF",
        versao_do_contrato_alvo=VersaoDeContrato(1, 0),
        ponto_de_entrada="exportador_pdf:main",
    )

    ativar_plugin(contrato_do_host, declaracao)


def test_declaracao_sem_ponto_de_entrada_e_rejeitada():
    """Mutação alvo: aceitar DeclaracaoDePlugin sem ponto_de_entrada (AD4)."""
    with pytest.raises(RegistroImplicito):
        DeclaracaoDePlugin(nome="ExportadorPDF", versao_do_contrato_alvo=VersaoDeContrato(1, 0))


def test_acessar_capacidade_nao_declarada_e_rejeitado():
    """Mutação alvo: permitir acesso a capacidade fora de capacidades_solicitadas (AD3)."""
    declaracao = DeclaracaoDePlugin(
        nome="ExportadorPDF",
        versao_do_contrato_alvo=VersaoDeContrato(1, 0),
        ponto_de_entrada="exportador_pdf:main",
        capacidades_solicitadas=frozenset({"leitura"}),
    )

    with pytest.raises(CapacidadeNaoDeclarada):
        acessar_capacidade(declaracao, "rede")


def test_acessar_capacidade_declarada_funciona():
    """Mutação alvo: rejeitar acesso a capacidade que de fato foi declarada (AD3)."""
    declaracao = DeclaracaoDePlugin(
        nome="ExportadorPDF",
        versao_do_contrato_alvo=VersaoDeContrato(1, 0),
        ponto_de_entrada="exportador_pdf:main",
        capacidades_solicitadas=frozenset({"leitura", "rede"}),
    )

    acessar_capacidade(declaracao, "rede")


def test_hook_que_lanca_excecao_e_isolado_do_host():
    """Mutação alvo: deixar exceção de hook de plugin propagar ao chamador (AD2)."""
    def hook_com_defeito():
        raise ValueError("falha interna do plugin")

    resultado = executar_hook_isolado("ExportadorPDF", hook_com_defeito)

    assert resultado.sucesso is False
    assert "falha interna do plugin" in resultado.erro


def test_hook_que_funciona_normalmente_retorna_resultado_de_sucesso():
    """Mutação alvo: envolver hook que funciona corretamente em falha espúria (AD2)."""
    def hook_ok(x):
        return x * 2

    resultado = executar_hook_isolado("ExportadorPDF", hook_ok, 21)

    assert resultado.sucesso is True
    assert resultado.valor == 42


def test_desativacao_remove_plugin_e_seus_recursos():
    """Mutação alvo: deixar recurso associado ao plugin sobreviver à desativação (AD5)."""
    host = EstadoDoHost()
    declaracao = DeclaracaoDePlugin(
        nome="ExportadorPDF",
        versao_do_contrato_alvo=VersaoDeContrato(1, 0),
        ponto_de_entrada="exportador_pdf:main",
    )
    host.ativar(declaracao, recursos=["handle_de_arquivo_temporario"])

    host.desativar("ExportadorPDF")

    assert "ExportadorPDF" not in host.plugins_ativos
    assert "ExportadorPDF" not in host.recursos_por_plugin


def test_desativar_plugin_nao_ativo_e_rejeitado():
    """Mutação alvo: aceitar desativação silenciosa de plugin que nunca foi ativado."""
    host = EstadoDoHost()

    with pytest.raises(PluginNaoEncontrado):
        host.desativar("Fantasma")


def test_evolucao_de_contrato_que_quebra_sem_bump_de_major_e_rejeitada():
    """Mutação alvo: aceitar evolução de contrato que quebra hook sem bump de major (AD6)."""
    atual = ContratoDeExtensao(versao=VersaoDeContrato(1, 4))
    novo = ContratoDeExtensao(versao=VersaoDeContrato(1, 5))

    with pytest.raises(QuebraDeContratoSemMajorBump):
        evoluir_contrato(atual, novo, quebra_hook=True)


def test_evolucao_de_contrato_compativel_sem_bump_de_major_e_aceita():
    """Mutação alvo: rejeitar evolução compatível que só incrementa minor (AD6)."""
    atual = ContratoDeExtensao(versao=VersaoDeContrato(1, 4))
    novo = ContratoDeExtensao(versao=VersaoDeContrato(1, 5))

    evoluir_contrato(atual, novo, quebra_hook=False)


def test_evolucao_de_contrato_que_quebra_com_bump_de_major_e_aceita():
    """Mutação alvo: rejeitar evolução que quebra mesmo com major corretamente incrementado (AD6)."""
    atual = ContratoDeExtensao(versao=VersaoDeContrato(1, 4))
    novo = ContratoDeExtensao(versao=VersaoDeContrato(2, 0))

    evoluir_contrato(atual, novo, quebra_hook=True)
