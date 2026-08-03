"""Trilha de auditoria: registro local, append-only, e a UNICA fonte confiavel
de "isso ja foi escrito".

Um indice em sistema de terceiro pode apagar ou mudar o campo que seria usado
como chave depois da escrita (ex.: um ERP que limpa o numero do boleto apos a
baixa via API) -- consultar esse indice para decidir idempotencia da um falso
negativo sistematico: o item some do indice e o motor tenta escrever de novo.
A trilha e local, imutavel e consultada ANTES de qualquer indice remoto.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RegistroTrilha:
    chave: str
    usuario: str
    quando: datetime
    acao: str
    detalhe: str = ""


class Trilha:
    def __init__(self) -> None:
        self._registros: list[RegistroTrilha] = []
        self._chaves: set[str] = set()

    def ja_processado(self, chave: str) -> bool:
        return chave in self._chaves

    def registrar(
        self, chave: str, usuario: str, quando: datetime, acao: str, detalhe: str = ""
    ) -> RegistroTrilha:
        if self.ja_processado(chave):
            raise ValueError(f"chave ja registrada, escrita seria duplicata: {chave}")
        registro = RegistroTrilha(chave, usuario, quando, acao, detalhe)
        self._registros.append(registro)
        self._chaves.add(chave)
        return registro

    def historico(self) -> tuple[RegistroTrilha, ...]:
        return tuple(self._registros)
