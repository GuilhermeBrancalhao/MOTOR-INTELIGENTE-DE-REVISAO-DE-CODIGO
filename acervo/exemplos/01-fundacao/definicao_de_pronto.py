"""A Definicao de PRONTO como codigo executavel.

Os quatro criterios de `00-INTRODUCAO/Convencoes.md` secao 4 sao uma regra de
decisao, nao uma lista de boas intencoes -- e regra de decisao se escreve como
funcao e se prova com teste. Este modulo e a forma executavel dela.

A decisao de desenho central esta em `Exemplos.NAO_CITADOS`: um volume que nao
cita nenhum exemplo **nao satisfaz** o criterio 2. Nao e caso vacuo, nao e
"passa porque nao ha o que reprovar" -- o criterio manda `pytest exemplos/<vol>`
passar, e um comando que nao tem o que rodar nao passou. Essa leitura foi a que
manteve sete volumes em RASCUNHO na auditoria de 2026-08-03 mesmo com media
acima de 8,0, e esta travada por teste.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Status(str, Enum):
    """Os tres valores gravaveis em `_VOLUME.yml`.

    `PENDENTE` nao esta aqui de proposito: e estado derivado (volume declarado no
    contrato mas sem pasta no disco), calculado por `status.py`, nunca gravado.
    """

    RASCUNHO = "RASCUNHO"
    REQUER_REVISAO = "REQUER_REVISAO"
    PRONTO = "PRONTO"


class Exemplos(str, Enum):
    """Resultado do criterio 2, com o caso "nao ha o que rodar" explicito."""

    PASSAM = "PASSAM"
    FALHAM = "FALHAM"
    NAO_CITADOS = "NAO_CITADOS"


@dataclass(frozen=True)
class Auditoria:
    """Criterio 3. `media` e a linha que `status.py` le do relatorio."""

    media: float
    menor_nota_de_secao: float

    @property
    def aprovada(self) -> bool:
        return self.media >= 8.0 and self.menor_nota_de_secao >= 6.0


@dataclass(frozen=True)
class Gates:
    """O estado dos quatro criterios para um volume."""

    estrutural_verde: bool
    exemplos: Exemplos
    auditoria: Auditoria | None
    registrado_no_changelog: bool


def motivo_de_nao_promocao(g: Gates) -> str | None:
    """Devolve o primeiro criterio que impede `PRONTO`, ou `None` se os quatro passam.

    A ordem importa: relatar o criterio 1 antes do 3 evita mandar alguem gastar
    uma auditoria num volume que nem passa no gate mecanico -- a parte cara da
    verificacao vem depois da barata, nunca antes.
    """
    if not g.estrutural_verde:
        return "criterio 1: gate estrutural vermelho"
    if g.exemplos is Exemplos.FALHAM:
        return "criterio 2: testes dos exemplos falham"
    if g.exemplos is Exemplos.NAO_CITADOS:
        return "criterio 2: o volume nao cita exemplo, entao nao ha suite a rodar"
    if g.auditoria is None:
        return "criterio 3: auditoria nao registrada"
    if not g.auditoria.aprovada:
        return "criterio 3: media abaixo de 8,0 ou secao abaixo de 6"
    if not g.registrado_no_changelog:
        return "criterio 4: resultado nao registrado no CHANGELOG"
    return None


def decidir_status(g: Gates) -> Status:
    """Aplica a Definicao de PRONTO.

    `REQUER_REVISAO` e reservado ao volume que ja passou os gates mecanicos e
    reprovou no julgamento -- ele nao regride para RASCUNHO, que significaria
    "nem tentado". Gate estrutural vermelho, ao contrario, mantem RASCUNHO.
    """
    if motivo_de_nao_promocao(g) is None:
        return Status.PRONTO
    if not g.estrutural_verde:
        return Status.RASCUNHO
    if g.auditoria is not None and not g.auditoria.aprovada:
        return Status.REQUER_REVISAO
    return Status.RASCUNHO
