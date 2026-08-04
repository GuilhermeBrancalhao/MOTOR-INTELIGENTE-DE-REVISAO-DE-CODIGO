"""Orçamento de desempenho: SLO declarado, medição sob carga, regressão, otimização validada.

As regras J1-J6 formalizadas: `declarar_operacao_pronta` exige SLO (J1) e
`PoliticaDeSobrecarga` (J4); `verificar_slo` exige carga mínima realista (J2);
`detectar_regressao_de_performance` compara p95 entre medições (J3);
`validar_otimizacao` exige melhoria mensurável (J5); `SLO.__post_init__` exige
margem para operação com IA (J6).
"""

from __future__ import annotations

from dataclasses import dataclass, field


class SLOAusente(Exception):
    """J1: operação proposta sem SLO declarado."""


class EstrategiaDeSobrecargaAusente(Exception):
    """J4: operação proposta sem política de sobrecarga declarada."""


class MedicaoSobCargaInsuficiente(Exception):
    """J2: medição com concorrência abaixo do mínimo realista."""


class MargemDeVariabilidadeAusente(Exception):
    """J6: SLO de operação com IA sem margem entre p95 e p99."""


class OtimizacaoNaoValidada(Exception):
    """J5: otimização proposta sem melhoria mensurável de p95."""


@dataclass(frozen=True)
class SLO:
    operacao: str
    p95_ms: float
    p99_ms: float
    envolve_chamada_de_ia: bool = False

    def __post_init__(self) -> None:
        if self.envolve_chamada_de_ia and self.p99_ms <= self.p95_ms:
            raise MargemDeVariabilidadeAusente(
                f"SLO de '{self.operacao}' envolve IA mas p99 nao e maior que p95 (J6)"
            )


@dataclass(frozen=True)
class PoliticaDeSobrecarga:
    limite_concorrente: int
    estrategia: str


@dataclass(frozen=True)
class OperacaoDeclarada:
    nome: str
    slo: SLO
    politica_de_sobrecarga: PoliticaDeSobrecarga


def declarar_operacao_pronta(
    nome: str, slo: SLO | None, politica: PoliticaDeSobrecarga | None
) -> OperacaoDeclarada:
    if slo is None:
        raise SLOAusente(f"operacao '{nome}' sem SLO declarado (J1)")
    if politica is None:
        raise EstrategiaDeSobrecargaAusente(f"operacao '{nome}' sem estrategia de sobrecarga (J4)")
    return OperacaoDeclarada(nome, slo, politica)


@dataclass(frozen=True)
class MedicaoDeCarga:
    operacao: str
    concorrencia: int
    amostras_ms: tuple

    def percentil(self, p: float) -> float:
        amostras_ordenadas = sorted(self.amostras_ms)
        indice = min(int(len(amostras_ordenadas) * p), len(amostras_ordenadas) - 1)
        return amostras_ordenadas[indice]


def verificar_slo(slo: SLO, medicao: MedicaoDeCarga, concorrencia_minima: int = 10) -> None:
    if medicao.concorrencia < concorrencia_minima:
        raise MedicaoSobCargaInsuficiente(
            f"concorrencia {medicao.concorrencia} abaixo do minimo realista "
            f"{concorrencia_minima} (J2)"
        )
    p95 = medicao.percentil(0.95)
    if p95 > slo.p95_ms:
        raise ValueError(f"SLO de '{slo.operacao}' violado: p95 medido {p95}ms > {slo.p95_ms}ms")


@dataclass(frozen=True)
class Regressao:
    operacao: str
    p95_anterior: float
    p95_atual: float


def detectar_regressao_de_performance(
    medicao_anterior: MedicaoDeCarga, medicao_atual: MedicaoDeCarga
) -> Regressao | None:
    anterior = medicao_anterior.percentil(0.95)
    atual = medicao_atual.percentil(0.95)
    if atual > anterior:
        return Regressao(medicao_atual.operacao, anterior, atual)
    return None


@dataclass(frozen=True)
class Otimizacao:
    descricao: str
    medicao_antes: MedicaoDeCarga
    medicao_depois: MedicaoDeCarga


def validar_otimizacao(otimizacao: Otimizacao) -> None:
    antes = otimizacao.medicao_antes.percentil(0.95)
    depois = otimizacao.medicao_depois.percentil(0.95)
    if depois >= antes:
        raise OtimizacaoNaoValidada(
            f"otimizacao '{otimizacao.descricao}' nao reduziu p95 medido "
            f"({antes}ms -> {depois}ms) (J5)"
        )
