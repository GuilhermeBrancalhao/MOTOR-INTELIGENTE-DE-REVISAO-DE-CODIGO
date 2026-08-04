"""Backlog de longo prazo: critério explícito, escopo registrado, autoridade sinalizada.

As regras AA1-AA6 formalizadas: `CriterioDePriorizacao.__post_init__` exige
valor/risco/dependência (AA1); `Roadmap.registrar_fora_de_escopo` exige motivo
(AA2); `Roadmap.sinalizar_decisao_de_autoridade` exige autoridade declarada
(AA3); `registrar_revisao_de_roadmap` exige motivo para atraso (AA4);
`ItemDeRoadmap.__post_init__` rejeita data comprometida em item direcional
(AA5); `DependenciaEntreCiclos.__post_init__` exige os três campos (AA6).
"""

from __future__ import annotations

from dataclasses import dataclass, field


class CriterioDePriorizacaoAusente(Exception):
    """AA1: critério de priorização sem valor, risco ou dependência declarados."""


class DataComprometidaIndevida(Exception):
    """AA5: item direcional de longo prazo com data comprometida."""


class MotivoForaDeEscopoAusente(Exception):
    """AA2: item fora de escopo registrado sem motivo."""


class AutoridadeNaoDeclarada(Exception):
    """AA3: decisão sinalizada sem autoridade necessária nomeada."""


class RevisaoDeRoadmapIncompleta(Exception):
    """AA4: revisão com item atrasado sem motivo declarado."""


class DependenciaEntreCiclosIncompleta(Exception):
    """AA6: dependência entre ciclos com campo ausente."""


@dataclass(frozen=True)
class CriterioDePriorizacao:
    item: str
    valor: str
    risco: str
    dependencia: str

    def __post_init__(self) -> None:
        if not all([self.valor, self.risco, self.dependencia]):
            raise CriterioDePriorizacaoAusente(
                f"criterio de priorizacao de '{self.item}' incompleto (AA1)"
            )


@dataclass(frozen=True)
class ItemDeRoadmap:
    nome: str
    criterio: CriterioDePriorizacao
    horizonte: str  # "COMPROMETIDO_CURTO_PRAZO" | "DIRECIONAL_LONGO_PRAZO"
    data_comprometida: str | None = None

    def __post_init__(self) -> None:
        if self.horizonte == "DIRECIONAL_LONGO_PRAZO" and self.data_comprometida is not None:
            raise DataComprometidaIndevida(
                f"item '{self.nome}' e direcional de longo prazo mas tem data comprometida (AA5)"
            )


@dataclass(frozen=True)
class ItemForaDeEscopo:
    nome: str
    motivo: str


@dataclass(frozen=True)
class DecisaoQueExigeAutoridade:
    nome: str
    motivo: str
    autoridade_necessaria: str


@dataclass(frozen=True)
class DependenciaEntreCiclos:
    item_dependente: str
    item_do_qual_depende: str
    ciclo_de_origem: str

    def __post_init__(self) -> None:
        if not all([self.item_dependente, self.item_do_qual_depende, self.ciclo_de_origem]):
            raise DependenciaEntreCiclosIncompleta("dependencia entre ciclos incompleta (AA6)")


@dataclass
class Roadmap:
    itens: dict = field(default_factory=dict)
    fora_de_escopo: dict = field(default_factory=dict)
    decisoes_pendentes_de_autoridade: dict = field(default_factory=dict)

    def adicionar_item(self, item: ItemDeRoadmap) -> None:
        self.itens[item.nome] = item

    def registrar_fora_de_escopo(self, item: ItemForaDeEscopo) -> None:
        if not item.motivo:
            raise MotivoForaDeEscopoAusente(f"item '{item.nome}' fora de escopo sem motivo (AA2)")
        self.fora_de_escopo[item.nome] = item

    def sinalizar_decisao_de_autoridade(self, decisao: DecisaoQueExigeAutoridade) -> None:
        if not decisao.autoridade_necessaria:
            raise AutoridadeNaoDeclarada(
                f"decisao '{decisao.nome}' sem autoridade necessaria declarada (AA3)"
            )
        self.decisoes_pendentes_de_autoridade[decisao.nome] = decisao


@dataclass(frozen=True)
class RevisaoDeRoadmap:
    data: str
    itens_entregues: tuple
    itens_atrasados: tuple
    motivo_dos_atrasos: str = ""


def registrar_revisao_de_roadmap(historico: list, revisao: RevisaoDeRoadmap) -> None:
    if revisao.itens_atrasados and not revisao.motivo_dos_atrasos:
        raise RevisaoDeRoadmapIncompleta("revisao com item atrasado sem motivo declarado (AA4)")
    historico.append(revisao)
