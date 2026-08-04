import pytest

from documentacao import (
    ADR,
    ADRImutavel,
    ADRIncompleto,
    Documento,
    DocumentoDesatualizado,
    DocumentoNaoVersionado,
    EdicaoManualDeConteudoGerado,
    FonteDeVerdadeAusente,
    PublicoAlvoInvalido,
    RegistroDeADRs,
    VerificacaoDeVigencia,
    editar_documento,
    verificar_vigencia,
)


def adr(numero=1, titulo="usar fila assincrona", supersede=None):
    return ADR(
        numero=numero,
        titulo=titulo,
        contexto="processamento sincrono excedia timeout de requisicao",
        decisao="modelar trabalho como fila assincrona com estado consultavel",
        consequencia="cliente consulta status em vez de esperar bloqueado",
        supersede=supersede,
    )


def test_adr_incompleto_e_rejeitado():
    """W1: a mutação alvo é aceitar ADR com campo vazio."""
    with pytest.raises(ADRIncompleto):
        ADR(numero=1, titulo="x", contexto="", decisao="y", consequencia="z")


def test_adr_ja_registrado_nao_pode_ser_reescrito():
    """W2: a mutação alvo é permitir sobrescrever ADR existente diretamente."""
    registro = RegistroDeADRs()
    registro.registrar(adr(numero=1))
    with pytest.raises(ADRImutavel):
        registro.registrar(adr(numero=1, titulo="outra decisao"))


def test_substituir_adr_marca_anterior_como_superado_sem_apagar():
    registro = RegistroDeADRs()
    registro.registrar(adr(numero=1, titulo="fila assincrona simples"))
    registro.substituir(adr(numero=2, titulo="fila com prioridade", supersede=1))
    assert registro.adrs[1].status == "SUPERADO"
    assert registro.adrs[1].titulo == "fila assincrona simples"  # nao apagado
    assert registro.adrs[2].status == "ACEITO"


def test_documento_nao_versionado_e_rejeitado():
    """W3: a mutação alvo é aceitar documento fora do controle de versão."""
    with pytest.raises(DocumentoNaoVersionado):
        Documento(titulo="guia", versionado_junto_do_codigo=False, publico_alvo="USUARIO")


def test_documento_gerado_sem_fonte_de_verdade_e_rejeitado():
    """W5: a mutação alvo é aceitar documento gerado sem fonte de verdade."""
    with pytest.raises(FonteDeVerdadeAusente):
        Documento(
            titulo="referencia de api",
            versionado_junto_do_codigo=True,
            publico_alvo="MANTENEDOR",
            gerado_automaticamente=True,
            fonte_de_verdade=None,
        )


def test_verificacao_de_vigencia_detecta_documento_desatualizado():
    """W4: a mutação alvo é não levantar exceção quando a afirmação não é mais verdadeira."""
    v = VerificacaoDeVigencia(
        documento="guia-de-instalacao",
        afirmacao="requer Python 3.9",
        ainda_verdadeiro_no_codigo=False,
    )
    with pytest.raises(DocumentoDesatualizado):
        verificar_vigencia(v)


def test_edicao_manual_de_documento_gerado_e_rejeitada():
    """W5: a mutação alvo é permitir edição direta sobre documento gerado."""
    doc = Documento(
        titulo="referencia de api",
        versionado_junto_do_codigo=True,
        publico_alvo="MANTENEDOR",
        gerado_automaticamente=True,
        fonte_de_verdade="contrato_api.yml",
    )
    with pytest.raises(EdicaoManualDeConteudoGerado):
        editar_documento(doc, "novo conteudo manual")


def test_publico_alvo_invalido_e_rejeitado():
    """W6: a mutação alvo é aceitar um terceiro valor que misture os dois públicos."""
    with pytest.raises(PublicoAlvoInvalido):
        Documento(titulo="guia", versionado_junto_do_codigo=True, publico_alvo="AMBOS")
