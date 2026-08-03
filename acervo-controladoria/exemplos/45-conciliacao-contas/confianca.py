"""Classificacao de confianca de um casamento: so ALTA escreve sozinho.

A garantia central e a degradacao segura: a ausencia de uma fonte de evidencia
(ex.: base de historico indisponivel neste ambiente) so pode FAZER a confianca
descer, nunca subir. Rodar sem uma fonte produz mais pendencia humana, nunca
mais escrita errada.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

LIMIAR_HISTORICO_OCORRENCIAS = 5
LIMIAR_HISTORICO_DOMINANCIA = 0.8


class Confianca(Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAIXA = "BAIXA"


@dataclass(frozen=True)
class Evidencia:
    match_exato_valor: bool
    similaridade_nome: float
    ocorrencias_historicas: int = 0
    dominancia_historica: float = 0.0


def classificar(evidencia: Evidencia) -> Confianca:
    if evidencia.match_exato_valor and evidencia.similaridade_nome >= 0.85:
        return Confianca.ALTA
    # historico forte: fornecedor recorrente reconhecido pelo nome, mesmo sem
    # bater exato no valor -- cobre debito de cartao/boleto sem identificador
    # explicito. Exige volume E dominancia; uma ocorrencia isolada nao vira
    # regra sozinha.
    if (
        evidencia.ocorrencias_historicas >= LIMIAR_HISTORICO_OCORRENCIAS
        and evidencia.dominancia_historica >= LIMIAR_HISTORICO_DOMINANCIA
    ):
        return Confianca.ALTA
    if evidencia.similaridade_nome >= 0.5 or evidencia.match_exato_valor:
        return Confianca.MEDIA
    return Confianca.BAIXA
