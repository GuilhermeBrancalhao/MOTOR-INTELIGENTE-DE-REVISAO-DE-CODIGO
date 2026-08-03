"""Guarda contra escrita duplicada: a chave de identidade e composta (data +
valor com sinal + contraparte normalizada), nunca valor isolado.

Dois movimentos legitimos podem ter o mesmo valor absoluto -- duas
transferencias redondas de mesmo montante em dias diferentes, ou para
contrapartes diferentes, nao sao a mesma coisa. Um duplicado real tambem tem o
mesmo valor absoluto que o original, entao valor sozinho nunca decide: decide
sempre o composto.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ChaveMovimento:
    data: date
    valor: float  # com sinal: negativo = saida, positivo = entrada
    contraparte: str

    def normalizada(self) -> "ChaveMovimento":
        return ChaveMovimento(self.data, round(self.valor, 2), self.contraparte.strip().upper())


class GuardaDuplicidade:
    """Fonte da verdade e a memoria local desta guarda, nunca um indice de
    sistema de terceiro -- ver `trilha.py` para o motivo (o indice remoto pode
    mutar ou apagar o campo que seria usado como chave depois da escrita)."""

    def __init__(self) -> None:
        self._vistos: set[ChaveMovimento] = set()

    def ja_registrado(self, chave: ChaveMovimento) -> bool:
        return chave.normalizada() in self._vistos

    def registrar(self, chave: ChaveMovimento) -> None:
        self._vistos.add(chave.normalizada())
