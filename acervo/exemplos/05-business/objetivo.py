"""Autoridade de stakeholder e objetivo de negócio falsificável, como código.

As seis regras (B1-B6) formalizadas: um stakeholder tem exatamente uma
classificação de autoridade (B1); um objetivo só existe com critério de
falsificação não vazio (B2); só quem `DECIDE` valida (B3); discordância entre
dois `DECIDE` é registrada, nunca resolvida automaticamente (B4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Autoridade(str, Enum):
    DECIDE = "DECIDE"
    CONSULTADO = "CONSULTADO"
    INFORMADO = "INFORMADO"


class AutoridadeInsuficiente(ValueError):
    """B3: alguém sem classificação DECIDE tentou validar um objetivo."""


@dataclass(frozen=True)
class Stakeholder:
    nome: str
    autoridade: Autoridade
    """B1: um único valor — o tipo já impede dupla classificação por
    construção, não é preciso validar em runtime que não há duas."""


@dataclass(frozen=True)
class ObjetivoDeNegocio:
    enunciado: str
    criterio_de_falsificacao: str
    """B2: o fato observável que provaria o objetivo descumprido. Vazio
    significa desejo, não objetivo — ver `eh_falsificavel`."""

    def eh_falsificavel(self) -> bool:
        return bool(self.criterio_de_falsificacao.strip())


@dataclass(frozen=True)
class Discordancia:
    proponentes: tuple[Stakeholder, Stakeholder]
    objetivos: tuple[ObjetivoDeNegocio, ObjetivoDeNegocio]
    resolvida: bool = False


@dataclass
class Processo:
    """O processo de captura: acumula objetivos validados e discordâncias
    registradas, nunca decide discordância por conta própria (B4)."""

    validados: list[tuple[ObjetivoDeNegocio, Stakeholder]] = field(default_factory=list)
    discordancias: list[Discordancia] = field(default_factory=list)

    def validar(self, objetivo: ObjetivoDeNegocio, por: Stakeholder) -> None:
        """B2 + B3: objetivo precisa ser falsificável E validado por quem
        DECIDE. As duas condições são checadas, nenhuma substitui a outra."""
        if not objetivo.eh_falsificavel():
            raise ValueError(f"objetivo sem critério de falsificação: {objetivo.enunciado!r}")
        if por.autoridade is not Autoridade.DECIDE:
            raise AutoridadeInsuficiente(
                f"{por.nome} tem autoridade {por.autoridade.value}, não pode validar objetivo (B3)"
            )
        # Se já existe outro DECIDE com objetivo incompatível, registra
        # discordância em vez de aceitar silenciosamente o novo.
        for obj_existente, quem in self.validados:
            if quem.autoridade is Autoridade.DECIDE and quem.nome != por.nome and obj_existente != objetivo:
                self.discordancias.append(Discordancia((quem, por), (obj_existente, objetivo)))
                return
        self.validados.append((objetivo, por))

    def discordancias_abertas(self) -> tuple[Discordancia, ...]:
        return tuple(d for d in self.discordancias if not d.resolvida)
