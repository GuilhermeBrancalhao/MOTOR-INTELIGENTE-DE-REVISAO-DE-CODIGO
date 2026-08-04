"""Trabalho assíncrono: estado consultável, worker sem afinidade, backpressure, idempotência.

As regras S1-S6 formalizadas: `Trabalho`/`EstadoDoTrabalho` modelam ciclo assíncrono
consultável (S1); `retirar_proximo` sem parâmetro de worker (S2); checagem de
`limite_concorrente` aplica backpressure (S3); `enfileirar` busca por chave de
idempotência (S4); toda transição passa por método nomeado (S5); `marcar_falha`
termina em estado consultável após esgotar tentativas (S6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EstadoDoTrabalho(str, Enum):
    ENFILEIRADO = "ENFILEIRADO"
    EXECUTANDO = "EXECUTANDO"
    CONCLUIDO = "CONCLUIDO"
    FALHOU_PERMANENTEMENTE = "FALHOU_PERMANENTEMENTE"


class TransicaoInvalida(Exception):
    """S5: operação de estado chamada fora da transição válida esperada."""


class CapacidadeInsuficiente(Exception):
    """S3: limite de execução concorrente atingido."""


@dataclass
class Trabalho:
    id: str
    chave_idempotencia: str
    estado: EstadoDoTrabalho = EstadoDoTrabalho.ENFILEIRADO
    tentativas: int = 0
    max_tentativas: int = 3
    resultado: object = None


@dataclass
class FilaDeTrabalhos:
    limite_concorrente: int = 5
    trabalhos: dict = field(default_factory=dict)

    def enfileirar(self, trabalho: Trabalho) -> Trabalho:
        existente = self._buscar_ativo_por_chave(trabalho.chave_idempotencia)
        if existente is not None:
            return existente  # S4: nunca duplica
        self.trabalhos[trabalho.id] = trabalho
        return trabalho

    def _buscar_ativo_por_chave(self, chave: str) -> Trabalho | None:
        for t in self.trabalhos.values():
            if t.chave_idempotencia == chave and t.estado != EstadoDoTrabalho.FALHOU_PERMANENTEMENTE:
                return t
        return None

    def retirar_proximo(self) -> Trabalho | None:
        em_execucao = sum(1 for t in self.trabalhos.values() if t.estado == EstadoDoTrabalho.EXECUTANDO)
        if em_execucao >= self.limite_concorrente:
            raise CapacidadeInsuficiente("limite de execucao concorrente atingido (S3)")
        for t in self.trabalhos.values():
            if t.estado == EstadoDoTrabalho.ENFILEIRADO:
                t.estado = EstadoDoTrabalho.EXECUTANDO  # S5
                return t
        return None

    def marcar_concluido(self, trabalho_id: str, resultado: object) -> None:
        t = self.trabalhos[trabalho_id]
        if t.estado != EstadoDoTrabalho.EXECUTANDO:
            raise TransicaoInvalida(f"nao pode concluir trabalho em estado {t.estado} (S5)")
        t.estado = EstadoDoTrabalho.CONCLUIDO
        t.resultado = resultado

    def marcar_falha(self, trabalho_id: str) -> None:
        t = self.trabalhos[trabalho_id]
        if t.estado != EstadoDoTrabalho.EXECUTANDO:
            raise TransicaoInvalida(f"nao pode falhar trabalho em estado {t.estado} (S5)")
        t.tentativas += 1
        if t.tentativas >= t.max_tentativas:
            t.estado = EstadoDoTrabalho.FALHOU_PERMANENTEMENTE  # S6
        else:
            t.estado = EstadoDoTrabalho.ENFILEIRADO  # retry

    def consultar_estado(self, trabalho_id: str) -> EstadoDoTrabalho:
        return self.trabalhos[trabalho_id].estado  # S1: nao bloqueia
