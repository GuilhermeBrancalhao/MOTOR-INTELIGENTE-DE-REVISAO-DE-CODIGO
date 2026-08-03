"""Checkpoint confirmado antes de avancar, e retomada conservadora.

A garantia central do motor de workflow e uma ordem: **gravar, confirmar, so entao
avancar**. Invertida, uma falha entre as duas operacoes deixa o estado ambiguo --
o passo pode ter concluido, mas a retomada nao sabe disso.

A escolha diante da ambiguidade e deliberadamente conservadora: **sem checkpoint
confirmado, o passo e tratado como nao concluido e reexecuta.** Isso custa uma
reexecucao ocasionalmente desnecessaria e evita o cenario oposto, muito pior --
avancar com base num passo que pode nao ter terminado.

A gravacao escreve o novo antes de invalidar o anterior, de modo que sempre existe
um checkpoint completo em disco, mesmo que a escrita seja interrompida no meio.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TipoPasso(str, Enum):
    DETERMINISTICO = "DETERMINISTICO"
    IA = "IA"


class EstadoWorkflow(str, Enum):
    EM_EXECUCAO = "EM_EXECUCAO"
    AGUARDANDO_SINAL = "AGUARDANDO_SINAL"
    PAUSADO = "PAUSADO"
    CONCLUIDO = "CONCLUIDO"
    FALHA_DEFINITIVA = "FALHA_DEFINITIVA"


class FalhaNaGravacao(Exception):
    """Simula queda de processo entre a gravacao e a confirmacao."""


@dataclass(frozen=True)
class Checkpoint:
    workflow_id: str
    passo_atual: str
    estado_acumulado: dict
    confirmado: bool = False


@dataclass
class Armazem:
    """Guarda o ultimo checkpoint CONFIRMADO. Um checkpoint gravado e nao
    confirmado nunca substitui o anterior -- e por isso que a retomada tem sempre
    um estado completo para ler, nunca um pela metade."""

    _confirmado: Checkpoint | None = None
    _em_gravacao: Checkpoint | None = None

    def gravar(self, ck: Checkpoint) -> None:
        self._em_gravacao = ck

    def confirmar(self) -> None:
        if self._em_gravacao is None:
            raise FalhaNaGravacao("confirmar sem gravacao pendente")
        self._confirmado = self._em_gravacao
        self._em_gravacao = None

    def ultimo_confirmado(self) -> Checkpoint | None:
        return self._confirmado


def avancar(armazem: Armazem, ck: Checkpoint, falhar_antes_de_confirmar: bool = False) -> None:
    """Grava, confirma, so entao o chamador pode avancar.

    `falhar_antes_de_confirmar` existe para o teste injetar a queda de processo no
    ponto exato onde a garantia vive.
    """
    armazem.gravar(ck)
    if falhar_antes_de_confirmar:
        raise FalhaNaGravacao("processo caiu entre gravar e confirmar")
    armazem.confirmar()


def passo_a_retomar(armazem: Armazem, primeiro_passo: str) -> str:
    """De onde a retomada continua. Sem checkpoint confirmado, do inicio."""
    ck = armazem.ultimo_confirmado()
    return ck.passo_atual if ck else primeiro_passo


def validar_saida(tipo: TipoPasso, saida: dict, formato: set[str]) -> bool:
    """Passo de IA tem a saida validada contra o formato esperado; passo
    deterministico nao -- sua saida se repete por construcao, e verificar de novo
    o que ja e garantido so custa tempo."""
    if tipo is TipoPasso.DETERMINISTICO:
        return True
    return formato.issubset(saida.keys())


@dataclass
class CicloDeCorrecao:
    """Correcao automatica com limite. Sem limite, uma saida consistentemente
    malformada faria o motor tentar para sempre sem convergir."""

    limite: int
    tentativas: int = 0

    def tentar(self) -> bool:
        self.tentativas += 1
        return self.tentativas <= self.limite

    def estado_final(self) -> EstadoWorkflow:
        return EstadoWorkflow.PAUSADO
