"""Rastreabilidade regra-teste, e a distincao entre os dois tipos de teste.

Este volume trata de uma pratica, nao de um componente -- entao o exemplo
executavel dele e a ferramenta que torna a pratica verificavel: dada a lista de
invariantes declaradas e a lista de nomes de teste, quais regras ficaram sem
protecao?

A regra de nomeacao que o volume defende vira aqui um predicado: um teste de
regressao nomeia a violacao que previne, e por isso o nome pode ser casado com a
regra. `test_guarda_2` nao pode -- e essa impossibilidade e o argumento.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Proposito(str, Enum):
    CAMINHO_FELIZ = "CAMINHO_FELIZ"
    REGRESSAO_DE_REGRA = "REGRESSAO_DE_REGRA"


@dataclass(frozen=True)
class Regra:
    id: str
    termos: frozenset[str]
    """Termos que um teste dessa regra deve mencionar no nome. Sao o vinculo
    verificavel entre a prosa da regra e o nome do teste."""


@dataclass(frozen=True)
class Teste:
    # O pytest coleta classes cujo nome comeca com "Test", e `Teste` casa esse
    # padrao. Sem esta marca, a suite emite PytestCollectionWarning ao tentar
    # instanciar a dataclass como classe de teste. Ironia registrada: o volume
    # sobre testar tropecou na convencao de nomes da propria ferramenta.
    __test__ = False

    nome: str
    proposito: Proposito
    mutacao_registrada: str | None = None
    """A mutacao que derrubou o teste. Um teste de regressao sem isso e uma
    hipotese: ninguem observou ele ficar vermelho."""

    @property
    def provado(self) -> bool:
        if self.proposito is Proposito.CAMINHO_FELIZ:
            return True  # nao afirma proteger regra; nao precisa da prova
        return bool(self.mutacao_registrada)


def cobre(teste: Teste, regra: Regra) -> bool:
    nome = teste.nome.lower()
    return all(t.lower() in nome for t in regra.termos)


@dataclass
class Suite:
    regras: tuple[Regra, ...]
    testes: tuple[Teste, ...]

    def testes_de(self, regra: Regra) -> tuple[Teste, ...]:
        return tuple(t for t in self.testes if cobre(t, regra))

    def regras_sem_teste(self) -> tuple[Regra, ...]:
        """A lacuna que o diagrama de rastreabilidade torna visivel: regra sem
        nenhuma seta chegando."""
        return tuple(r for r in self.regras if not self.testes_de(r))

    def regressoes_nao_provadas(self) -> tuple[Teste, ...]:
        """Testes que afirmam proteger uma regra e nunca foram vistos falhar."""
        return tuple(
            t for t in self.testes
            if t.proposito is Proposito.REGRESSAO_DE_REGRA and not t.provado
        )

    def madura(self) -> bool:
        """Suite madura: toda regra com teste, e toda regressao provada."""
        return not self.regras_sem_teste() and not self.regressoes_nao_provadas()
