"""Orçamento de janela de contexto: prioridade declarada, descarte registrado.

As seis regras (C1-C6) formalizadas: `Orcamento` recusa margem de
compactação zero (C4); `montar_janela` descarta por `ORDEM_DE_PRIORIDADE`,
nunca por ordem de chegada (C2); todo item removido gera `Descarte`
correspondente (C3); `INSTRUCAO_SISTEMA` só é recusada, nunca descartada
silenciosamente (C6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Categoria(str, Enum):
    INSTRUCAO_SISTEMA = "INSTRUCAO_SISTEMA"
    HISTORICO_RECENTE = "HISTORICO_RECENTE"
    DOCUMENTO_RECUPERADO = "DOCUMENTO_RECUPERADO"
    RESULTADO_FERRAMENTA = "RESULTADO_FERRAMENTA"
    HISTORICO_ANTIGO = "HISTORICO_ANTIGO"


ORDEM_DE_PRIORIDADE = {
    Categoria.INSTRUCAO_SISTEMA: 0,
    Categoria.HISTORICO_RECENTE: 1,
    Categoria.DOCUMENTO_RECUPERADO: 2,
    Categoria.RESULTADO_FERRAMENTA: 3,
    Categoria.HISTORICO_ANTIGO: 4,
}
"""Menor numero = maior prioridade = ultimo a ser descartado (C2)."""


@dataclass(frozen=True)
class ItemDeContexto:
    id: str
    categoria: Categoria
    tokens: int
    conteudo: str = ""


@dataclass(frozen=True)
class Descarte:
    item_id: str
    categoria: Categoria
    motivo: str


class OrcamentoInvalido(ValueError):
    """C4: margem de compactação zero equivaleria a acionar no proprio limite."""


@dataclass(frozen=True)
class Orcamento:
    limite_total: int
    margem_compactacao: int

    def __post_init__(self) -> None:
        if self.margem_compactacao <= 0:
            raise OrcamentoInvalido("margem_compactacao precisa ser positiva (C4)")
        if self.limite_total <= 0:
            raise OrcamentoInvalido("limite_total precisa ser positivo")


class OrcamentoExcedidoPelaInstrucao(ValueError):
    """C6: instrucao de prioridade maxima excede o orcamento sozinha."""


@dataclass(frozen=True)
class JanelaMontada:
    itens: tuple[ItemDeContexto, ...]
    descartes: tuple[Descarte, ...]
    tokens_usados: int


def proximo_da_margem(consumo_atual: int, orcamento: Orcamento) -> bool:
    return (orcamento.limite_total - consumo_atual) <= orcamento.margem_compactacao


def montar_janela(candidatos: tuple[ItemDeContexto, ...], orcamento: Orcamento) -> JanelaMontada:
    """C2: descarta sempre pela prioridade declarada, nunca pela ordem em
    que os itens aparecem em `candidatos`. C3: todo descarte é registrado.
    C6: instrução de prioridade máxima nunca é descartada silenciosamente.
    """
    instrucoes = [c for c in candidatos if c.categoria is Categoria.INSTRUCAO_SISTEMA]
    tokens_instrucao = sum(c.tokens for c in instrucoes)
    if tokens_instrucao > orcamento.limite_total:
        raise OrcamentoExcedidoPelaInstrucao(
            f"instrucao de sistema ({tokens_instrucao} tokens) excede o orcamento total "
            f"({orcamento.limite_total}) sozinha (C6)"
        )

    restantes = list(candidatos)
    descartes: list[Descarte] = []

    def tokens_totais(itens: list[ItemDeContexto]) -> int:
        return sum(i.tokens for i in itens)

    while tokens_totais(restantes) > orcamento.limite_total:
        # entre os que ainda nao sao INSTRUCAO_SISTEMA, remove o de menor prioridade
        candidatos_a_descarte = [i for i in restantes if i.categoria is not Categoria.INSTRUCAO_SISTEMA]
        pior = max(candidatos_a_descarte, key=lambda i: ORDEM_DE_PRIORIDADE[i.categoria])
        restantes.remove(pior)
        descartes.append(Descarte(pior.id, pior.categoria, "orcamento excedido: prioridade mais baixa"))

    return JanelaMontada(tuple(restantes), tuple(descartes), tokens_totais(restantes))
