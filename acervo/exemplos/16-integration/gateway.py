"""Gateway de integração externa: versão, idempotência, circuit breaker.

As regras I1-I4 e I6 formalizadas: `verificar_versao` rejeita `major`
incompatível (I1); `ChamadaIdempotente` garante efeito único por chave
(I2); `PoliticaDeRetry` é obrigatória, sem padrão implícito (I3);
`CircuitBreaker` isola falha externa (I4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EstadoCircuito(str, Enum):
    FECHADO = "FECHADO"
    ABERTO = "ABERTO"
    MEIO_ABERTO = "MEIO_ABERTO"


class CircuitoAberto(Exception):
    """I4: falha imediata, sem tentar contra sistema externo degradado."""


class VersaoIncompativel(Exception):
    """I1: contrato de resposta não confere com a versão mínima esperada."""


@dataclass(frozen=True)
class VersaoContrato:
    major: int
    minor: int

    def compativel_com(self, minima: "VersaoContrato") -> bool:
        return self.major == minima.major and self.minor >= minima.minor


@dataclass(frozen=True)
class PoliticaDeRetry:
    timeout_s: float
    max_tentativas: int
    backoff_inicial_s: float

    def __post_init__(self) -> None:
        if self.timeout_s <= 0 or self.max_tentativas <= 0:
            raise ValueError("timeout_s e max_tentativas precisam ser positivos (I3)")


@dataclass
class CircuitBreaker:
    limiar_abertura: int
    tempo_espera_s: float
    estado: EstadoCircuito = EstadoCircuito.FECHADO
    falhas_consecutivas: int = 0

    def pode_chamar(self) -> bool:
        return self.estado != EstadoCircuito.ABERTO

    def registrar_sucesso(self) -> None:
        self.falhas_consecutivas = 0
        self.estado = EstadoCircuito.FECHADO

    def registrar_falha(self) -> None:
        self.falhas_consecutivas += 1
        if self.falhas_consecutivas >= self.limiar_abertura:
            self.estado = EstadoCircuito.ABERTO


@dataclass
class Gateway:
    versao_minima_esperada: VersaoContrato
    circuito: CircuitBreaker
    cache_idempotencia: dict = field(default_factory=dict)

    def chamar(self, chave_idempotencia: str, executar_chamada_externa) -> dict:
        """`executar_chamada_externa` é injetado (Callable) para que o
        exemplo não dependa de rede real. Devolve {"dados": ..., "versao": VersaoContrato}."""
        if not self.circuito.pode_chamar():
            raise CircuitoAberto("sistema externo degradado, falha imediata (I4)")

        if chave_idempotencia in self.cache_idempotencia:
            return self.cache_idempotencia[chave_idempotencia]

        try:
            resposta = executar_chamada_externa()
        except Exception:
            self.circuito.registrar_falha()
            raise

        self.circuito.registrar_sucesso()
        versao: VersaoContrato = resposta["versao"]
        if not versao.compativel_com(self.versao_minima_esperada):
            raise VersaoIncompativel(
                f"versao {versao} incompativel com minima {self.versao_minima_esperada} (I1)"
            )

        self.cache_idempotencia[chave_idempotencia] = resposta
        return resposta
