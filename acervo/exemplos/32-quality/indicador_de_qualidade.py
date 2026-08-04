"""Indicador de qualidade: prova por mutação, gate com piso, dívida registrada, tendência.

As regras H1-H6 formalizadas: `Medicao.taxa_prova_de_mutacao` ignora
`cobertura_de_linha` (H1); `GateDeQualidade.verificar` exige exceção registrada
para passar abaixo do limiar (H2); `ItemDeDivida` exige os quatro campos (H3);
`detectar_regressao` exige duas medições (H4) e retorna objeto explícito de
regressão (H5); `Medicao` mantém campos nomeados separados (H6).
"""

from __future__ import annotations

from dataclasses import dataclass, field


class LimiarNaoAtingido(Exception):
    """H2: taxa de prova por mutação abaixo do limiar, sem exceção registrada."""


class ItemDeDividaIncompleto(Exception):
    """H3: item de dívida técnica registrado sem todos os campos exigidos."""


@dataclass(frozen=True)
class Medicao:
    data: str
    regras_totais: int
    regras_com_prova_de_mutacao: int
    cobertura_de_linha: float

    def taxa_prova_de_mutacao(self) -> float:
        if self.regras_totais == 0:
            return 0.0
        return self.regras_com_prova_de_mutacao / self.regras_totais  # H1: nunca cobertura_de_linha


@dataclass
class GateDeQualidade:
    limiar_minimo: float = 0.8

    def verificar(self, medicao: Medicao, excecao_registrada: bool = False) -> None:
        if medicao.taxa_prova_de_mutacao() < self.limiar_minimo and not excecao_registrada:
            raise LimiarNaoAtingido(
                f"taxa de prova por mutacao {medicao.taxa_prova_de_mutacao():.2f} abaixo "
                f"do limiar {self.limiar_minimo} (H2)"
            )


@dataclass(frozen=True)
class ItemDeDivida:
    descricao: str
    motivo_adiamento: str
    data_registro: str
    custo_estimado: str

    def __post_init__(self) -> None:
        if not all([self.descricao, self.motivo_adiamento, self.data_registro, self.custo_estimado]):
            raise ItemDeDividaIncompleto("item de divida tecnica exige os quatro campos (H3)")


@dataclass(frozen=True)
class Regressao:
    data_anterior: str
    data_atual: str
    taxa_anterior: float
    taxa_atual: float


@dataclass
class HistoricoDeQualidade:
    medicoes: list = field(default_factory=list)

    def registrar(self, medicao: Medicao) -> None:
        self.medicoes.append(medicao)


def detectar_regressao(historico: HistoricoDeQualidade) -> Regressao | None:
    if len(historico.medicoes) < 2:
        return None  # H4: tendencia exige pelo menos duas medicoes
    anterior, atual = historico.medicoes[-2], historico.medicoes[-1]
    if atual.taxa_prova_de_mutacao() < anterior.taxa_prova_de_mutacao():
        return Regressao(
            anterior.data, atual.data, anterior.taxa_prova_de_mutacao(), atual.taxa_prova_de_mutacao()
        )
    return None
