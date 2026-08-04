"""Seleção de modelo: requisito antes de avaliação, fallback obrigatório, custo por tarefa.

As regras M1-M6 formalizadas: filtro por `RequisitoDeCapacidade` precede
avaliação (M1); `CandidatoDeModelo.aprovado` exige `ResultadoDeAvaliacao` (M2);
`validar_plano` exige fallback (M3); `comparar_custo_por_tarefa` usa custo total,
não preço unitário (M4); nenhum preço é fixo no módulo (M5);
`registrar_troca` é o único caminho para o histórico (M6).
"""

from __future__ import annotations

from dataclasses import dataclass, field


class ModeloNaoAvaliado(Exception):
    """M2: candidato consultado antes de qualquer avaliação contra casos de ouro."""


class FallbackAusente(Exception):
    """M3: plano de tarefa declarado sem modelo de fallback."""


@dataclass(frozen=True)
class RequisitoDeCapacidade:
    contexto_minimo_tokens: int
    modalidade: str
    tolerancia_latencia_s: float


@dataclass(frozen=True)
class ResultadoDeAvaliacao:
    modelo: str
    casos_de_ouro_aprovados: int
    casos_de_ouro_total: int
    data_avaliacao: str


@dataclass
class CandidatoDeModelo:
    nome: str
    atende_requisito: bool
    avaliacao: ResultadoDeAvaliacao | None = None

    def aprovado(self, limiar_aprovacao: float = 0.9) -> bool:
        if self.avaliacao is None:
            raise ModeloNaoAvaliado(f"modelo '{self.nome}' sem avaliacao de casos de ouro (M2)")
        if not self.atende_requisito:
            return False  # M1: nao atende requisito, reprovado independente da avaliacao
        taxa = self.avaliacao.casos_de_ouro_aprovados / self.avaliacao.casos_de_ouro_total
        return taxa >= limiar_aprovacao


@dataclass(frozen=True)
class PlanoDeTarefa:
    tarefa: str
    modelo_principal: str
    modelo_fallback: str | None


def validar_plano(plano: PlanoDeTarefa) -> None:
    if plano.modelo_fallback is None:
        raise FallbackAusente(f"tarefa '{plano.tarefa}' sem fallback definido (M3)")


@dataclass(frozen=True)
class CustoPorTarefa:
    modelo: str
    tokens_entrada: int
    tokens_saida: int
    tentativas: int
    preco_por_1k_entrada: float
    preco_por_1k_saida: float

    def total(self) -> float:
        return self.tentativas * (
            (self.tokens_entrada / 1000) * self.preco_por_1k_entrada
            + (self.tokens_saida / 1000) * self.preco_por_1k_saida
        )


def comparar_custo_por_tarefa(a: CustoPorTarefa, b: CustoPorTarefa) -> str:
    """M4: compara custo total da tarefa, nunca preço unitário isolado."""
    return a.modelo if a.total() <= b.total() else b.modelo


@dataclass(frozen=True)
class RegistroDeTroca:
    tarefa: str
    modelo_anterior: str
    modelo_novo: str
    motivo: str
    data: str
    resultado_avaliacao: ResultadoDeAvaliacao


def registrar_troca(historico: list, troca: RegistroDeTroca) -> None:
    """M6: toda troca de modelo é registrada, nunca silenciosa."""
    historico.append(troca)
