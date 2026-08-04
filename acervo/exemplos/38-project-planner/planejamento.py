"""Planejamento: dependência real, estimativa com incerteza, escopo negociado, conclusão verificável.

As regras Z1-Z6 formalizadas: `ordenar_por_dependencia` detecta ciclo (Z1);
`PlanoDeCiclo.adicionar_tarefa` exige faixa real de estimativa (Z2);
`PlanoDeCiclo.__post_init__` exige escopo negociado (Z3); `registrar_revisao`
exige motivo (Z4); `AndamentoDaTarefa.bloquear` exige motivo (Z5);
`AndamentoDaTarefa.concluir` exige critério atingido (Z6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class CriterioDeProntoAusente(Exception):
    """Z6: tarefa adicionada ao plano sem critério de pronto declarado."""


class EstimativaSemIncerteza(Exception):
    """Z2: estimativa sem faixa real de incerteza (mínimo igual ao máximo, ou invertida)."""


class DependenciaForaDeOrdem(Exception):
    """Z1: ciclo de dependência detectado entre tarefas."""


class EscopoNaoNegociado(Exception):
    """Z3: plano de ciclo sem escopo negociado registrado."""


class RevisaoIncompleta(Exception):
    """Z4: revisão de plano sem motivo declarado."""


class MotivoDoBloqueioAusente(Exception):
    """Z5: bloqueio de tarefa sem motivo explícito."""


class CriterioNaoAtingido(Exception):
    """Z6: tentativa de concluir tarefa sem confirmar critério de pronto."""


@dataclass(frozen=True)
class Tarefa:
    nome: str
    depende_de: frozenset
    criterio_de_pronto: str
    estimativa_min_dias: float
    estimativa_max_dias: float


@dataclass
class PlanoDeCiclo:
    escopo_negociado: str
    tarefas: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.escopo_negociado:
            raise EscopoNaoNegociado("plano de ciclo sem escopo negociado registrado (Z3)")

    def adicionar_tarefa(self, tarefa: Tarefa) -> None:
        if not tarefa.criterio_de_pronto:
            raise CriterioDeProntoAusente(f"tarefa '{tarefa.nome}' sem criterio de pronto (Z6)")
        if tarefa.estimativa_min_dias >= tarefa.estimativa_max_dias:
            raise EstimativaSemIncerteza(
                f"tarefa '{tarefa.nome}' sem faixa real de incerteza (Z2)"
            )
        self.tarefas[tarefa.nome] = tarefa


def ordenar_por_dependencia(tarefas: dict) -> list:
    ordenadas = []
    visitadas = set()
    visitando = set()

    def visitar(nome):
        if nome in visitadas:
            return
        if nome in visitando:
            raise DependenciaForaDeOrdem(f"ciclo de dependencia envolvendo '{nome}' (Z1)")
        visitando.add(nome)
        for dep in tarefas[nome].depende_de:
            visitar(dep)
        visitando.discard(nome)
        visitadas.add(nome)
        ordenadas.append(nome)

    for nome in tarefas:
        visitar(nome)
    return ordenadas


@dataclass(frozen=True)
class RevisaoDePlano:
    motivo: str
    tarefas_afetadas: tuple
    data: str


def registrar_revisao(historico: list, revisao: RevisaoDePlano) -> None:
    if not revisao.motivo:
        raise RevisaoIncompleta("revisao de plano sem motivo declarado (Z4)")
    historico.append(revisao)


class EstadoDaTarefa(str, Enum):
    NAO_INICIADA = "NAO_INICIADA"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    BLOQUEADA = "BLOQUEADA"
    CONCLUIDA = "CONCLUIDA"


@dataclass
class AndamentoDaTarefa:
    tarefa: str
    estado: EstadoDaTarefa = EstadoDaTarefa.NAO_INICIADA
    motivo_do_bloqueio: str | None = None

    def bloquear(self, motivo: str) -> None:
        if not motivo:
            raise MotivoDoBloqueioAusente(f"bloqueio de '{self.tarefa}' exige motivo (Z5)")
        self.estado = EstadoDaTarefa.BLOQUEADA
        self.motivo_do_bloqueio = motivo

    def concluir(self, criterio_atingido: bool) -> None:
        if not criterio_atingido:
            raise CriterioNaoAtingido(
                f"tarefa '{self.tarefa}' nao pode concluir sem atingir criterio de pronto (Z6)"
            )
        self.estado = EstadoDaTarefa.CONCLUIDA
