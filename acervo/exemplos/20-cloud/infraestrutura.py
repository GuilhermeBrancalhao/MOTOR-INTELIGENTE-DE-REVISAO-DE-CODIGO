"""Infraestrutura declarada: dono obrigatório, redundância verificável, drift detectável.

As regras N1-N6 formalizadas: `Recurso` recusa criação sem `dono` (N3);
`validar_config_sem_segredo` rejeita segredo em texto plano (N5);
`PlanoDeInfraestrutura.verificar_redundancia` reporta lacuna (N2);
`aplicar_mudanca` isola por ambiente (N4); `detectar_drift` reporta divergência (N6).
"""

from __future__ import annotations

from dataclasses import dataclass, field

_CHAVES_DE_SEGREDO = {"senha", "token", "chave_api", "secret", "password"}


class RecursoSemDono(Exception):
    """N3: recurso declarado sem dono responsável."""


class SegredoInlineDetectado(Exception):
    """N5: segredo encontrado em texto plano na configuração declarada."""


class MudancaForaDoAmbiente(Exception):
    """N4: mudança destinada a um ambiente aplicada a recurso de outro."""


def validar_config_sem_segredo(config_bruta: dict) -> None:
    for chave, valor in config_bruta.items():
        if chave.lower() in _CHAVES_DE_SEGREDO and valor:
            raise SegredoInlineDetectado(f"segredo inline em '{chave}' (N5)")


@dataclass(frozen=True)
class Recurso:
    nome: str
    tipo: str
    ambiente: str
    dono: str
    redundante: bool = False

    def __post_init__(self) -> None:
        if not self.dono:
            raise RecursoSemDono(f"recurso {self.nome} sem dono declarado (N3)")


@dataclass(frozen=True)
class AlvoDeDisponibilidade:
    nome: str
    exige_redundancia: bool


@dataclass(frozen=True)
class Divergencia:
    recurso: str
    campo: str
    declarado: object
    real: object


@dataclass
class PlanoDeInfraestrutura:
    recursos: list

    def verificar_redundancia(self, alvo: AlvoDeDisponibilidade) -> list:
        if not alvo.exige_redundancia:
            return []
        return [r for r in self.recursos if not r.redundante]

    def aplicar_mudanca(self, recurso_atualizado: Recurso, ambiente_alvo: str) -> None:
        if recurso_atualizado.ambiente != ambiente_alvo:
            raise MudancaForaDoAmbiente(
                f"mudanca para '{recurso_atualizado.ambiente}' nao pode ser aplicada "
                f"em '{ambiente_alvo}' (N4)"
            )
        self.recursos = [
            recurso_atualizado if r.nome == recurso_atualizado.nome else r
            for r in self.recursos
        ]

    def detectar_drift(self, estado_real: dict) -> list:
        divergencias = []
        for r in self.recursos:
            real = estado_real.get(r.nome)
            if real is None:
                divergencias.append(Divergencia(r.nome, "existencia", "existe", "ausente"))
                continue
            if real.get("redundante") != r.redundante:
                divergencias.append(
                    Divergencia(r.nome, "redundante", r.redundante, real.get("redundante"))
                )
        return divergencias
