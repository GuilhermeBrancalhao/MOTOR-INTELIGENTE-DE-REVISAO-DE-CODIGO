"""Inventário de portfólio: dependência explícita, concentração e duplicação.

As seis regras (E1-E6) formalizadas: um `Sistema` exige fornecedor, modelo e
fonte de dado não vazios (E1); toda `DecisaoDePortfolio` carrega uma
`consequencia` nomeada, nunca decide por reflexo (E2); `custo_total_agregado`
soma por fornecedor, nunca por sistema isolado (E3).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field


class DependenciaIncompleta(ValueError):
    """E1: fornecedor, modelo ou fonte de dado ausente."""


@dataclass(frozen=True)
class Sistema:
    id: str
    fornecedor: str
    modelo: str
    fonte_de_dado: str
    categoria: str
    custo_mensal: float

    def __post_init__(self) -> None:
        if not (self.fornecedor and self.modelo and self.fonte_de_dado):
            raise DependenciaIncompleta(f"{self.id}: fornecedor/modelo/fonte_de_dado obrigatorios (E1)")


@dataclass(frozen=True)
class DecisaoDePortfolio:
    sistemas_envolvidos: tuple[str, ...]
    consequencia: str
    """E2: a razão nomeada. Vazia significa decisão sem justificativa —
    tratada como erro de uso, não como decisão válida."""
    decisao: str

    def __post_init__(self) -> None:
        if not self.consequencia.strip():
            raise ValueError("decisão de portfólio sem consequência nomeada viola E2")


LIMIAR_CONCENTRACAO = 3
"""A partir de quantos sistemas no mesmo fornecedor a concentração é sinalizada."""


@dataclass
class Inventario:
    sistemas: dict[str, Sistema] = field(default_factory=dict)
    decisoes: list[DecisaoDePortfolio] = field(default_factory=list)

    def registrar(self, s: Sistema) -> None:
        self.sistemas[s.id] = s

    def custo_total_agregado(self) -> dict[str, float]:
        """E3: soma por fornecedor entre TODOS os sistemas, nunca isolado."""
        totais: dict[str, float] = defaultdict(float)
        for s in self.sistemas.values():
            totais[s.fornecedor] += s.custo_mensal
        return dict(totais)

    def concentracao_por_fornecedor(self) -> dict[str, tuple[str, ...]]:
        """Fornecedores com LIMIAR_CONCENTRACAO ou mais sistemas registrados."""
        por_fornecedor: dict[str, list[str]] = defaultdict(list)
        for s in self.sistemas.values():
            por_fornecedor[s.fornecedor].append(s.id)
        return {
            f: tuple(ids) for f, ids in por_fornecedor.items() if len(ids) >= LIMIAR_CONCENTRACAO
        }

    def duplicacoes(self) -> tuple[tuple[str, str], ...]:
        """E5: pares de sistemas na mesma categoria, achado de portfólio."""
        por_categoria: dict[str, list[str]] = defaultdict(list)
        for s in self.sistemas.values():
            por_categoria[s.categoria].append(s.id)
        pares = []
        for ids in por_categoria.values():
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    pares.append((ids[i], ids[j]))
        return tuple(pares)

    def decidir(self, sistemas_envolvidos: tuple[str, ...], consequencia: str, decisao: str) -> None:
        self.decisoes.append(DecisaoDePortfolio(sistemas_envolvidos, consequencia, decisao))
