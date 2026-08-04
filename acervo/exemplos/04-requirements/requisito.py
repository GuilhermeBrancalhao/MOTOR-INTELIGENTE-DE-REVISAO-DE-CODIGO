"""Requisito verificável como estrutura de dado, não como frase em prosa.

As oito regras (Q1-Q8) formalizadas: um requisito só existe se for
falsificável (Q1); lacuna sem resposta vira `Pendencia`, nunca requisito com
valor assumido (Q2); todo requisito carrega rastro para trás (lacuna, origem)
e para frente (verificação) (Q3); identificador nunca muda de significado,
requisito retirado aposenta o id em vez de reciclar (Q4).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Origem(str, Enum):
    """Q3, rastro para trás. Mesma ideia de procedência do 01-FUNDACAO,
    aplicada ao dado de origem de um requisito específico."""

    RESPONDIDA = "RESPONDIDA"
    INFERIDA = "INFERIDA"
    DECIDIDA_POR_HUMANO = "DECIDIDA_POR_HUMANO"


class IdentificadorReciclado(ValueError):
    """Q4: um id retirado nunca volta a nomear outra coisa."""


@dataclass(frozen=True)
class CriterioDeAceite:
    """Q1: a forma mínima de um enunciado falsificável — uma condição que um
    fato observável pode contrariar. `descricao` sozinha não basta; precisa
    ser algo que `verificar` de fato possa avaliar."""

    descricao: str
    verificar: object  # Callable[[dict], bool], tipado solto para o exemplo


@dataclass(frozen=True)
class Requisito:
    id: str
    enunciado: str
    criterio: CriterioDeAceite
    origem: Origem
    lacuna_id: str | None
    """Q3, rastro para trás: de qual lacuna da descoberta este requisito
    nasceu. `None` só é aceitável para requisito DECIDIDA_POR_HUMANO."""
    verificacao_id: str | None = None
    """Q3, rastro para frente: qual verificação confere este requisito.
    `None` significa que ainda não tem — entra na lista à parte que 09 e 04
    tratam como pendência de segunda ordem, não erro."""

    def __post_init__(self) -> None:
        if self.origem != Origem.DECIDIDA_POR_HUMANO and self.lacuna_id is None:
            raise ValueError(f"{self.id}: requisito sem origem humana precisa de lacuna_id (Q3)")


@dataclass(frozen=True)
class Pendencia:
    """Q2: o que uma lacuna sem resposta vira — nunca um Requisito com valor
    assumido no lugar da resposta que faltou."""

    lacuna_id: str
    peso: int


@dataclass
class Conjunto:
    """O conjunto de requisitos de um projeto, com a disciplina de Q4 e Q7."""

    requisitos: dict[str, Requisito] = field(default_factory=dict)
    aposentados: set[str] = field(default_factory=set)
    pendencias: list[Pendencia] = field(default_factory=list)
    mudancas: list[tuple[str, str]] = field(default_factory=list)
    """Q7: (id, razao) de cada mudança. Razão vazia ou genérica é rejeitada
    por quem chama `registrar_mudanca`, não por este tipo — a validação de
    conteúdo da razão é responsabilidade de quem grava, o tipo só guarda."""

    def adicionar(self, r: Requisito) -> None:
        if r.id in self.aposentados:
            raise IdentificadorReciclado(f"'{r.id}' foi aposentado e não pode ser reutilizado")
        self.requisitos[r.id] = r

    def retirar(self, id_: str) -> None:
        """Q4: retirar aposenta o id, nunca libera para reuso."""
        self.requisitos.pop(id_, None)
        self.aposentados.add(id_)

    def registrar_pendencia(self, lacuna_id: str, peso: int) -> None:
        self.pendencias.append(Pendencia(lacuna_id, peso))

    def registrar_mudanca(self, id_: str, razao: str) -> None:
        """Q7: toda mudança exige razão registrada, ligada ao id."""
        if not razao.strip():
            raise ValueError("mudança sem razão registrada viola Q7")
        self.mudancas.append((id_, razao))

    def sem_rastro_para_frente(self) -> tuple[Requisito, ...]:
        """Q3: requisitos que ainda não têm verificação associada — a lista
        à parte que Q3 exige manter visível, não escondida dentro do total."""
        return tuple(r for r in self.requisitos.values() if r.verificacao_id is None)

    def completo(self) -> bool:
        """Um conjunto só é chamado de completo com zero pendência aberta e
        zero requisito sem rastro para frente — Q2 e Q3 juntas."""
        return not self.pendencias and not self.sem_rastro_para_frente()
