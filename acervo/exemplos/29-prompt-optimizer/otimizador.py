"""Busca automática de variante de prompt: mesma amostra, melhoria real, nunca promoção.

As regras O1-O6 formalizadas: `avaliar_variante` sempre recebe `casos_de_ouro`
idêntico (O1); só supera baseline além de `limiar_melhoria_minima` vira proposta
(O2); `Otimizador` não expõe método de promoção (O3); `buscar` respeita
`max_tentativas` (O4); toda tentativa vai a `HistoricoDeBusca` (O5);
`casos_de_ouro` nunca é modificado internamente (O6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Variante:
    nome: str
    corpo: str


@dataclass(frozen=True)
class ResultadoDeAvaliacao:
    variante: str
    taxa_acerto: float
    amostra_usada: tuple


@dataclass
class HistoricoDeBusca:
    tentativas: list = field(default_factory=list)

    def registrar(self, resultado: ResultadoDeAvaliacao) -> None:
        self.tentativas.append(resultado)  # O5: toda tentativa, aprovada ou nao


@dataclass
class Otimizador:
    avaliar_variante: Callable[[Variante, tuple], float]
    casos_de_ouro: tuple
    limiar_melhoria_minima: float = 0.02
    max_tentativas: int = 10

    def buscar(self, baseline: Variante, gerador_de_candidatos):
        historico = HistoricoDeBusca()
        taxa_baseline = self.avaliar_variante(baseline, self.casos_de_ouro)  # O1
        melhor_proposta: ResultadoDeAvaliacao | None = None

        for i, candidata in enumerate(gerador_de_candidatos):
            if i >= self.max_tentativas:  # O4
                break
            taxa = self.avaliar_variante(candidata, self.casos_de_ouro)  # O1
            resultado = ResultadoDeAvaliacao(candidata.nome, taxa, self.casos_de_ouro)
            historico.registrar(resultado)  # O5

            supera_baseline = (taxa - taxa_baseline) > self.limiar_melhoria_minima  # O2
            if supera_baseline:
                if melhor_proposta is None or taxa > melhor_proposta.taxa_acerto:
                    melhor_proposta = resultado

        return melhor_proposta, historico
        # Nenhum método deste tipo altera casos_de_ouro (O6) nem promove nada (O3) —
        # a única saída é uma proposta e o histórico, ambos consumidos fora deste volume.
