import pytest

from curadoria import BaseDeConhecimento, Documento, EstadoCiclo, Origem, OrigemIncompleta


def origem(fonte="juridico", confianca=0.9):
    return Origem(fonte, "curador-1", confianca)


def test_origem_sem_fonte_e_rejeitada():
    with pytest.raises(OrigemIncompleta):
        Origem("", "curador-1", 0.9)


def test_documento_expirado_nunca_e_devolvido_por_consulta_valido():
    """K2, a garantia central. A mutação alvo: remover a checagem de estado
    em consultar_valido — este teste falha se isso acontecer."""
    base = BaseDeConhecimento()
    d = Documento("d1", "conteudo", origem())
    base.ingerir(d)
    base.expirar("d1")
    assert base.consultar_valido("d1") is None
    assert "d1" in base.documentos  # continua fisicamente presente


def test_documento_valido_e_devolvido_normalmente():
    base = BaseDeConhecimento()
    base.ingerir(Documento("d1", "conteudo", origem()))
    assert base.consultar_valido("d1") is not None


def test_dois_documentos_mesmo_fato_chave_geram_conflito_registrado():
    """K3: nunca resolvido sozinho — fica pendente até decisão explícita."""
    base = BaseDeConhecimento()
    base.ingerir(Documento("d1", "versao A", origem(confianca=0.9), fato_chave="politica-x"))
    base.ingerir(Documento("d2", "versao B", origem(confianca=0.6), fato_chave="politica-x"))
    assert len(base.conflitos) == 1
    assert base.conflitos[0].resolvido is False
    # nenhum dos dois foi descartado automaticamente
    assert base.consultar_valido("d1") is not None
    assert base.consultar_valido("d2") is not None


def test_documentos_com_fato_chave_diferente_nao_geram_conflito():
    base = BaseDeConhecimento()
    base.ingerir(Documento("d1", "x", origem(), fato_chave="fato-a"))
    base.ingerir(Documento("d2", "y", origem(), fato_chave="fato-b"))
    assert base.conflitos == []


def test_resolver_conflito_expira_o_documento_que_nao_prevalece():
    base = BaseDeConhecimento()
    base.ingerir(Documento("d1", "A", origem(confianca=0.9), fato_chave="x"))
    base.ingerir(Documento("d2", "B", origem(confianca=0.6), fato_chave="x"))
    base.resolver_conflito(0, prevalece="d1")
    assert base.consultar_valido("d1") is not None
    assert base.consultar_valido("d2") is None


def test_revalidar_so_funciona_a_partir_de_expirando():
    """K6: revalidação é sempre explícita e só parte do estado certo."""
    base = BaseDeConhecimento()
    base.ingerir(Documento("d1", "x", origem()))
    with pytest.raises(ValueError, match="EXPIRANDO"):
        base.revalidar("d1")  # está VALIDO, não EXPIRANDO
    base.marcar_expirando("d1")
    base.revalidar("d1")
    assert base.documentos["d1"].estado == EstadoCiclo.VALIDO


def test_expirando_sem_revalidacao_nao_volta_a_valido_sozinho():
    """Não existe transição implícita — sem chamar revalidar, o documento
    permanece EXPIRANDO até alguém agir ou até expirar()."""
    base = BaseDeConhecimento()
    base.ingerir(Documento("d1", "x", origem()))
    base.marcar_expirando("d1")
    assert base.documentos["d1"].estado == EstadoCiclo.EXPIRANDO
