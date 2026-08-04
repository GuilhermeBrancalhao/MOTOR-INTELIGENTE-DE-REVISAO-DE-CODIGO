"""Índice vetorial: versão de modelo, métrica e partição sempre explícitas.

As seis regras (V1-V6) formalizadas: `comparar` recusa vetores de versões de
modelo diferentes (V1); `Consulta` exige métrica e partição, sem padrão
implícito (V2, V3); `buscar` nunca cruza partição (V3) nem devolve vetor
excluído (V6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Metrica(str, Enum):
    COSSENO = "COSSENO"
    PRODUTO_ESCALAR = "PRODUTO_ESCALAR"
    EUCLIDIANA = "EUCLIDIANA"


class ConsultaIncompleta(ValueError):
    """V2/V3: métrica ou partição ausente."""


class VersaoIncompativel(ValueError):
    """V1: comparação entre vetores de versões de modelo diferentes."""


@dataclass(frozen=True)
class Vetor:
    id_documento: str
    valores: tuple[float, ...]
    versao_modelo: str
    particao: str


@dataclass(frozen=True)
class Consulta:
    vetor_busca: tuple[float, ...]
    metrica: Metrica | None
    particao: str | None
    versao_modelo: str | None
    limite: int = 5

    def __post_init__(self) -> None:
        if self.metrica is None or self.particao is None or self.versao_modelo is None:
            raise ConsultaIncompleta("metrica, particao e versao_modelo sao obrigatorios (V2, V3)")


@dataclass(frozen=True)
class ResultadoBusca:
    id_documento: str
    score: float
    particao: str


def _similaridade(a: tuple[float, ...], b: tuple[float, ...], metrica: Metrica) -> float:
    if metrica is Metrica.PRODUTO_ESCALAR:
        return sum(x * y for x, y in zip(a, b))
    if metrica is Metrica.EUCLIDIANA:
        return -sum((x - y) ** 2 for x, y in zip(a, b))  # maior = mais proximo
    # COSSENO
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def comparar(v1: Vetor, v2: Vetor, metrica: Metrica) -> float:
    """V1: nunca compara vetores de versões de modelo diferentes."""
    if v1.versao_modelo != v2.versao_modelo:
        raise VersaoIncompativel(
            f"versoes incompativeis: {v1.versao_modelo!r} vs {v2.versao_modelo!r}"
        )
    return _similaridade(v1.valores, v2.valores, metrica)


@dataclass
class IndiceVetorial:
    vetores: list[Vetor] = field(default_factory=list)
    excluidos: set[str] = field(default_factory=set)

    def indexar(self, v: Vetor) -> None:
        self.vetores.append(v)

    def excluir(self, id_documento: str) -> None:
        """V6: exclusão lógica, independente de remoção física."""
        self.excluidos.add(id_documento)

    def buscar(self, consulta: Consulta) -> tuple[ResultadoBusca, ...]:
        """V3: só compara vetores da mesma partição e versão de modelo.
        V6: nunca devolve documento excluído."""
        candidatos = [
            v for v in self.vetores
            if v.particao == consulta.particao
            and v.versao_modelo == consulta.versao_modelo
            and v.id_documento not in self.excluidos
        ]
        pontuados = [
            ResultadoBusca(v.id_documento, _similaridade(consulta.vetor_busca, v.valores, consulta.metrica), v.particao)
            for v in candidatos
        ]
        pontuados.sort(key=lambda r: r.score, reverse=True)
        return tuple(pontuados[: consulta.limite])
