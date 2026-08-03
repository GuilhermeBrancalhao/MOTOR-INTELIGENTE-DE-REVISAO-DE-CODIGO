"""Guardiao de orcamento: tres dimensoes independentes, verificadas antes de agir.

O componente mais simples do motor de agente e o mais critico de acertar primeiro.
Duas decisoes de desenho o definem, e as duas tem contraexemplo concreto:

1. **Tres dimensoes independentes.** So passos: uma ferramenta lenta consome tempo
   sem consumir passos. So tempo: um laco de passos rapidos e numerosos consome
   tokens sem estourar tempo. Nenhuma das tres substitui as outras.
2. **Verificar antes de chamar o modelo, nunca depois.** Chamar e descartar a
   decisao desperdicaria justamente a dimensao (tokens, tempo) que a verificacao
   existe para proteger.

A validacao de entrada mora em `criar()`, nao em `__post_init__`: o construtor
precisa produzir orcamento zerado ou negativo durante o consumo -- e ai o guardiao
encerra. Validar na construcao impediria o proprio consumo de funcionar.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class Motivo(str, Enum):
    """Motivo de encerramento. Nunca um booleano de sucesso/falha: um resultado
    por orcamento excedido e parcial por definicao, e quem chama precisa saber."""

    OBJETIVO_ATINGIDO = "OBJETIVO_ATINGIDO"
    ORCAMENTO_EXCEDIDO = "ORCAMENTO_EXCEDIDO"
    ERRO_NAO_RECUPERAVEL = "ERRO_NAO_RECUPERAVEL"


class Dimensao(str, Enum):
    PASSOS = "PASSOS"
    TOKENS = "TOKENS"
    TEMPO = "TEMPO"


class OrcamentoInvalido(ValueError):
    """Orcamento com dimensao nao positiva nao inicia execucao -- falha alto, na
    entrada, em vez de deixar comecar para morrer no primeiro guardiao."""


@dataclass(frozen=True)
class Orcamento:
    passos: int
    tokens: int
    tempo_s: float

    @staticmethod
    def criar(passos: int, tokens: int, tempo_s: float) -> "Orcamento":
        if passos <= 0 or tokens <= 0 or tempo_s <= 0:
            raise OrcamentoInvalido(
                f"dimensao nao positiva: passos={passos} tokens={tokens} tempo_s={tempo_s}"
            )
        return Orcamento(passos, tokens, tempo_s)

    def estourou(self) -> Dimensao | None:
        """Qual dimensao acabou, ou `None`. Ordem de checagem estavel para que o
        motivo relatado seja reprodutivel entre execucoes."""
        if self.passos <= 0:
            return Dimensao.PASSOS
        if self.tokens <= 0:
            return Dimensao.TOKENS
        if self.tempo_s <= 0:
            return Dimensao.TEMPO
        return None

    def consumir(self, passos: int = 1, tokens: int = 0, tempo_s: float = 0.0) -> "Orcamento":
        """Devolve orcamento novo, sem mutar o anterior -- a trilha guarda o valor
        de cada passo, e mutar destruiria o historico."""
        return replace(
            self,
            passos=self.passos - passos,
            tokens=self.tokens - tokens,
            tempo_s=self.tempo_s - tempo_s,
        )


@dataclass
class Guardiao:
    """Decide se o proximo passo pode acontecer. Conta as consultas para que o
    teste possa provar que o modelo nao foi chamado com orcamento ja zerado."""

    orcamento: Orcamento
    consultas: int = 0

    def pode_seguir(self) -> bool:
        self.consultas += 1
        return self.orcamento.estourou() is None

    def registrar_passo(self, tokens: int, tempo_s: float) -> None:
        self.orcamento = self.orcamento.consumir(passos=1, tokens=tokens, tempo_s=tempo_s)
