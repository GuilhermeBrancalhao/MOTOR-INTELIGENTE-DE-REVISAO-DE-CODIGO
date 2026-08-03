"""Reconciliacao por ancora: acha o dia mais recente em que o saldo do banco
bate com o saldo projetado do sistema, andando PARA FRENTE a partir de um saldo
inicial conhecido -- nunca de tras para frente a partir do saldo atual.

Andar de tras para frente a partir do saldo ATUAL de hoje e a armadilha: uma
lista de movimentos que ainda nao inclui um lancamento com data de registro
correta mas que so foi recebido depois (ex.: juros lancados com atraso) faz o
saldo atual carregar um residuo que nao pertence a nenhum dia -- e esse residuo
desloca TODOS os dias por igual, fazendo a ancora sumir mesmo quando a
conciliacao esta correta. Ancorar em um saldo passado conhecido e caminhar para
a frente isola o residuo no dia em que ele realmente aparece.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

CENTAVO = 0.005


@dataclass(frozen=True)
class Movimento:
    data: date
    valor: float  # positivo = entrada, negativo = saida


@dataclass(frozen=True)
class Ancora:
    data: date
    saldo_banco: float
    saldo_sistema: float
    residuo: float


def saldo_projetado(saldo_inicial: float, movimentos: list[Movimento], ate: date) -> float:
    """Saldo do sistema projetado somando movimentos ate (inclusive) a data."""
    return saldo_inicial + sum(m.valor for m in movimentos if m.data <= ate)


def achar_ancora(
    saldo_inicial_conhecido: float,
    data_inicial_conhecida: date,
    movimentos: list[Movimento],
    saldos_banco: dict[date, float],
) -> Ancora | None:
    """Devolve a ancora mais recente entre os dias com saldo de banco conhecido,
    ou None se nenhum dia fecha no centavo."""
    melhor: Ancora | None = None
    for dia in sorted(saldos_banco):
        if dia < data_inicial_conhecida:
            continue
        projetado = saldo_projetado(saldo_inicial_conhecido, movimentos, dia)
        residuo = round(saldos_banco[dia] - projetado, 2)
        if abs(residuo) < CENTAVO:
            melhor = Ancora(data=dia, saldo_banco=saldos_banco[dia], saldo_sistema=projetado, residuo=residuo)
    return melhor
