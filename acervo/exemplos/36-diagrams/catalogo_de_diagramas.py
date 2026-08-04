"""Catálogo de diagramas: tipo reconhecido, prosa obrigatória, escolha por necessidade, vigência.

As regras X1-X6 formalizadas: `TipoDeDiagrama.__post_init__` exige
proposito/quando_usar (X1) e nome catalogado (X3); `Catalogo.registrar` exige
prosa_explicativa (X2) e fora_de_escopo (X6); `escolher_tipo_por_necessidade`
mapeia necessidade -> tipo (X5); `verificar_vigencia_do_diagrama` detecta
desatualização (X4).
"""

from __future__ import annotations

from dataclasses import dataclass, field

_TIPOS_RECONHECIDOS = {"C4Context", "sequenceDiagram", "stateDiagram-v2", "flowchart"}


class TipoDeDiagramaIncompleto(Exception):
    """X1: tipo de diagrama sem propósito ou orientação de quando usar."""


class TipoNaoCatalogado(Exception):
    """X3: nome de tipo fora do conjunto reconhecido pelo acervo."""


class EntradaSemProsa(Exception):
    """X2: entrada de catálogo sem prosa explicativa."""


class EscopoNaoDeclarado(Exception):
    """X6: entrada de catálogo sem declarar o que não mostra."""


class NecessidadeNaoCatalogada(Exception):
    """X5: necessidade de representação sem tipo correspondente no catálogo."""


class DiagramaDesatualizado(Exception):
    """X4: diagrama não reflete mais o sistema real."""


@dataclass(frozen=True)
class TipoDeDiagrama:
    nome: str
    proposito: str
    quando_usar: str

    def __post_init__(self) -> None:
        if not self.proposito or not self.quando_usar:
            raise TipoDeDiagramaIncompleto(f"tipo '{self.nome}' sem proposito ou quando_usar (X1)")
        if self.nome not in _TIPOS_RECONHECIDOS:
            raise TipoNaoCatalogado(f"tipo '{self.nome}' fora do conjunto reconhecido (X3)")


@dataclass(frozen=True)
class EntradaDeCatalogo:
    titulo: str
    tipo: TipoDeDiagrama
    prosa_explicativa: str
    fora_de_escopo: str


@dataclass
class Catalogo:
    entradas: dict = field(default_factory=dict)

    def registrar(self, entrada: EntradaDeCatalogo) -> None:
        if not entrada.prosa_explicativa:
            raise EntradaSemProsa(f"entrada '{entrada.titulo}' sem prosa explicativa (X2)")
        if not entrada.fora_de_escopo:
            raise EscopoNaoDeclarado(f"entrada '{entrada.titulo}' sem escopo declarado (X6)")
        self.entradas[entrada.titulo] = entrada


_MAPA_NECESSIDADE_PARA_TIPO = {
    "estrutura de sistema e dependencia externa": "C4Context",
    "interacao ao longo do tempo entre participantes": "sequenceDiagram",
    "transicao de estado de uma entidade": "stateDiagram-v2",
    "ramificacao de decisao condicional": "flowchart",
}


def escolher_tipo_por_necessidade(necessidade: str, tipos_disponiveis: dict) -> TipoDeDiagrama:
    nome_tipo = _MAPA_NECESSIDADE_PARA_TIPO.get(necessidade)
    if nome_tipo is None:
        raise NecessidadeNaoCatalogada(f"necessidade '{necessidade}' sem tipo catalogado (X5)")
    return tipos_disponiveis[nome_tipo]


@dataclass(frozen=True)
class VerificacaoDeVigenciaDoDiagrama:
    titulo: str
    ainda_reflete_o_sistema: bool


def verificar_vigencia_do_diagrama(verificacao: VerificacaoDeVigenciaDoDiagrama) -> None:
    if not verificacao.ainda_reflete_o_sistema:
        raise DiagramaDesatualizado(f"diagrama '{verificacao.titulo}' nao reflete mais o sistema (X4)")
