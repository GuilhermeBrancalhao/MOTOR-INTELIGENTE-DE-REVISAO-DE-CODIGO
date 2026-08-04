"""Compilação de prompt promovido em payload concreto de provedor.

As regras Q1-Q6 formalizadas: `compilar` recusa prompt fora de PROMOVIDO (Q1);
determinismo por ausência de estado externo (Q2); `OrcamentoExcedido` após
renderização (Q3); `Dialeto.formatar_mensagens` isola formatação (Q4);
`PosicaoDeCacheInvalida` rejeita posição fora de conteúdo estável (Q5);
`VariavelAusente` antes da renderização (Q6).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


class PromptNaoPromovido(Exception):
    """Q1: prompt fora do estado PROMOVIDO."""


class VariavelAusente(Exception):
    """Q6: variável declarada no contrato sem valor fornecido."""


class PosicaoDeCacheInvalida(Exception):
    """Q5: ponto de cache fora de conteúdo estável entre chamadas."""


class OrcamentoExcedido(Exception):
    """Q3: payload compilado excede o orçamento de tokens declarado."""


@dataclass(frozen=True)
class PromptPromovido:
    nome: str
    corpo: str
    variaveis_declaradas: frozenset
    hash: str
    estado: str = "PROMOVIDO"


@dataclass(frozen=True)
class Dialeto:
    nome: str
    formatar_mensagens: Callable[[str], tuple]


@dataclass(frozen=True)
class PontoDeCache:
    posicao: str


@dataclass(frozen=True)
class PayloadCompilado:
    hash_origem: str
    dialeto: str
    mensagens: tuple
    tokens_estimados: int
    pontos_de_cache: tuple


def compilar(
    prompt: PromptPromovido,
    variaveis: dict,
    dialeto: Dialeto,
    orcamento_tokens: int,
    pontos_de_cache: tuple = (),
) -> PayloadCompilado:
    if prompt.estado != "PROMOVIDO":
        raise PromptNaoPromovido(f"prompt '{prompt.nome}' nao esta PROMOVIDO (Q1)")

    ausentes = prompt.variaveis_declaradas - set(variaveis.keys())
    if ausentes:
        raise VariavelAusente(f"variaveis nao fornecidas: {sorted(ausentes)} (Q6)")

    for ponto in pontos_de_cache:
        if ponto.posicao != "inicio_estavel":
            raise PosicaoDeCacheInvalida(
                f"ponto de cache em posicao invalida: '{ponto.posicao}' (Q5)"
            )

    corpo_renderizado = prompt.corpo.format(**variaveis)
    mensagens = tuple(dialeto.formatar_mensagens(corpo_renderizado))
    tokens_estimados = len(corpo_renderizado.split())

    if tokens_estimados > orcamento_tokens:
        raise OrcamentoExcedido(
            f"payload compilado ({tokens_estimados} tokens) excede orcamento "
            f"({orcamento_tokens}) (Q3)"
        )

    return PayloadCompilado(
        hash_origem=prompt.hash,
        dialeto=dialeto.nome,
        mensagens=mensagens,
        tokens_estimados=tokens_estimados,
        pontos_de_cache=pontos_de_cache,
    )
