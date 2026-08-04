import pytest

from catalogo_de_diagramas import (
    Catalogo,
    DiagramaDesatualizado,
    EntradaDeCatalogo,
    EntradaSemProsa,
    EscopoNaoDeclarado,
    NecessidadeNaoCatalogada,
    TipoDeDiagrama,
    TipoDeDiagramaIncompleto,
    TipoNaoCatalogado,
    VerificacaoDeVigenciaDoDiagrama,
    escolher_tipo_por_necessidade,
    verificar_vigencia_do_diagrama,
)


def tipo_sequencia():
    return TipoDeDiagrama(
        nome="sequenceDiagram",
        proposito="mostra ordem temporal de mensagens entre participantes",
        quando_usar="quando a pergunta e 'o que acontece, passo a passo'",
    )


def test_tipo_de_diagrama_incompleto_e_rejeitado():
    """X1: a mutação alvo é aceitar TipoDeDiagrama sem proposito ou quando_usar."""
    with pytest.raises(TipoDeDiagramaIncompleto):
        TipoDeDiagrama(nome="flowchart", proposito="", quando_usar="algo")


def test_tipo_nao_catalogado_e_rejeitado():
    """X3: a mutação alvo é aceitar um nome de tipo fora do conjunto reconhecido."""
    with pytest.raises(TipoNaoCatalogado):
        TipoDeDiagrama(nome="ganttDiagram", proposito="cronograma", quando_usar="planejamento")


def test_entrada_sem_prosa_explicativa_e_rejeitada():
    """X2: a mutação alvo é aceitar entrada sem prosa explicativa."""
    catalogo = Catalogo()
    with pytest.raises(EntradaSemProsa):
        catalogo.registrar(
            EntradaDeCatalogo(
                titulo="fluxo de login",
                tipo=tipo_sequencia(),
                prosa_explicativa="",
                fora_de_escopo="nao mostra tratamento de erro de rede",
            )
        )


def test_entrada_sem_escopo_declarado_e_rejeitada():
    """X6: a mutação alvo é aceitar entrada sem declarar o que não mostra."""
    catalogo = Catalogo()
    with pytest.raises(EscopoNaoDeclarado):
        catalogo.registrar(
            EntradaDeCatalogo(
                titulo="fluxo de login",
                tipo=tipo_sequencia(),
                prosa_explicativa="mostra a ordem de verificacao de credencial",
                fora_de_escopo="",
            )
        )


def test_escolher_tipo_por_necessidade_mapeia_corretamente():
    tipos = {
        "stateDiagram-v2": TipoDeDiagrama(
            nome="stateDiagram-v2", proposito="ciclo de vida", quando_usar="transicao de estado"
        )
    }
    tipo = escolher_tipo_por_necessidade("transicao de estado de uma entidade", tipos)
    assert tipo.nome == "stateDiagram-v2"


def test_necessidade_nao_catalogada_e_rejeitada():
    """X5: a mutação alvo é aceitar uma necessidade sem tipo correspondente."""
    with pytest.raises(NecessidadeNaoCatalogada):
        escolher_tipo_por_necessidade("mostrar cronograma de projeto", {})


def test_vigencia_detecta_diagrama_desatualizado():
    """X4: a mutação alvo é não levantar exceção quando o diagrama diverge do sistema."""
    v = VerificacaoDeVigenciaDoDiagrama(titulo="arquitetura-v1", ainda_reflete_o_sistema=False)
    with pytest.raises(DiagramaDesatualizado):
        verificar_vigencia_do_diagrama(v)
