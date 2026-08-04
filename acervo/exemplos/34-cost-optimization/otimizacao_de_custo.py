"""Custo por tarefa, atribuído, orçado com alerta, tendência, otimização validada.

As regras U1-U6 formalizadas: `CustoDeTarefa.__post_init__` exige `tarefa` (U1)
e `escopo` (U2); `verificar_orcamento` retorna três estados com limiar de
alerta antes do limite (U3); `detectar_tendencia_de_custo` exige dois períodos
(U4); `validar_otimizacao_de_custo` exige redução real medida (U5); nenhuma
constante de preço existe no módulo (U6).
"""

from __future__ import annotations

from dataclasses import dataclass, field


class TarefaAusente(Exception):
    """U1: custo registrado sem identificar a tarefa que o gerou."""


class EscopoAusente(Exception):
    """U2: custo registrado sem escopo (equipe, produto, ambiente) atribuído."""


class LimiarDeAlertaInvalido(Exception):
    """Limiar de alerta fora do intervalo (0, 1)."""


class OtimizacaoDeCustoNaoValidada(Exception):
    """U5: mudança proposta como economia sem redução real de gasto medido."""


@dataclass(frozen=True)
class CustoDeTarefa:
    tarefa: str
    escopo: str
    valor: float
    data: str

    def __post_init__(self) -> None:
        if not self.tarefa:
            raise TarefaAusente("custo registrado sem identificar a tarefa que o gerou (U1)")
        if not self.escopo:
            raise EscopoAusente(f"custo da tarefa '{self.tarefa}' sem escopo atribuido (U2)")


@dataclass(frozen=True)
class OrcamentoDeEscopo:
    escopo: str
    limite: float
    limiar_de_alerta: float = 0.8

    def __post_init__(self) -> None:
        if not (0 < self.limiar_de_alerta < 1):
            raise LimiarDeAlertaInvalido(
                f"limiar_de_alerta {self.limiar_de_alerta} fora do intervalo (0, 1)"
            )


def verificar_orcamento(orcamento: OrcamentoDeEscopo, gasto_atual: float) -> str:
    if gasto_atual >= orcamento.limite:
        return "ESTOURADO"
    if gasto_atual >= orcamento.limite * orcamento.limiar_de_alerta:
        return "ALERTA"
    return "OK"


@dataclass
class RegistroDeCusto:
    custos: list = field(default_factory=list)

    def registrar(self, custo: CustoDeTarefa) -> None:
        self.custos.append(custo)

    def total_por_escopo(self, escopo: str) -> float:
        return sum(c.valor for c in self.custos if c.escopo == escopo)


@dataclass(frozen=True)
class PeriodoDeCusto:
    periodo: str
    escopo: str
    total: float


@dataclass(frozen=True)
class TendenciaDeCusto:
    escopo: str
    total_anterior: float
    total_atual: float
    variacao: float


@dataclass
class HistoricoDeCusto:
    periodos: list = field(default_factory=list)

    def registrar(self, periodo: PeriodoDeCusto) -> None:
        self.periodos.append(periodo)


def detectar_tendencia_de_custo(historico: HistoricoDeCusto) -> TendenciaDeCusto | None:
    if len(historico.periodos) < 2:
        return None  # U4: tendencia exige pelo menos dois periodos
    anterior, atual = historico.periodos[-2], historico.periodos[-1]
    return TendenciaDeCusto(atual.escopo, anterior.total, atual.total, atual.total - anterior.total)


@dataclass(frozen=True)
class OtimizacaoDeCusto:
    descricao: str
    custo_antes: float
    custo_depois: float


def validar_otimizacao_de_custo(otimizacao: OtimizacaoDeCusto) -> None:
    if otimizacao.custo_depois >= otimizacao.custo_antes:
        raise OtimizacaoDeCustoNaoValidada(
            f"otimizacao '{otimizacao.descricao}' nao reduziu custo medido "
            f"({otimizacao.custo_antes} -> {otimizacao.custo_depois}) (U5)"
        )
