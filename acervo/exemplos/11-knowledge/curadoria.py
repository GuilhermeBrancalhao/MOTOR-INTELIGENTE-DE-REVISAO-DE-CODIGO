"""Curadoria de conhecimento: autoridade, ciclo de vida, conflito.

As seis regras (K1-K6) formalizadas: `Documento` recusa `Origem` incompleta
(K1); `consultar_valido` nunca devolve `Expirado` (K2); `detectar_conflitos`
agrupa por `fato_chave` e nunca resolve sozinho (K3); `revalidar` é a única
transição de volta a `Valido`, sempre explícita (K6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EstadoCiclo(str, Enum):
    VALIDO = "VALIDO"
    EXPIRANDO = "EXPIRANDO"
    EXPIRADO = "EXPIRADO"


class OrigemIncompleta(ValueError):
    """K1: origem sem os três campos obrigatórios."""


@dataclass(frozen=True)
class Origem:
    fonte: str
    validado_por: str
    confianca: float

    def __post_init__(self) -> None:
        if not (self.fonte and self.validado_por):
            raise OrigemIncompleta("fonte e validado_por são obrigatórios (K1)")
        if not (0.0 <= self.confianca <= 1.0):
            raise ValueError("confianca fora do intervalo [0,1]")


@dataclass
class Documento:
    id: str
    conteudo: str
    origem: Origem
    fato_chave: str | None = None
    estado: EstadoCiclo = EstadoCiclo.VALIDO


@dataclass(frozen=True)
class Conflito:
    documentos: tuple[str, ...]
    fato_chave: str
    resolvido: bool = False
    prevalece: str | None = None


@dataclass
class BaseDeConhecimento:
    documentos: dict[str, Documento] = field(default_factory=dict)
    conflitos: list[Conflito] = field(default_factory=list)
    falhas: list[str] = field(default_factory=list)

    def ingerir(self, doc: Documento) -> None:
        """K4: falha de ingestão nunca é silenciosa — mas aqui a validação
        de Origem já acontece antes, em __post_init__; este método só
        detecta conflito e registra."""
        if doc.fato_chave:
            existentes = [
                d for d in self.documentos.values()
                if d.fato_chave == doc.fato_chave and d.estado != EstadoCiclo.EXPIRADO
            ]
            if existentes:
                ids = tuple(d.id for d in existentes) + (doc.id,)
                self.conflitos.append(Conflito(ids, doc.fato_chave))
        self.documentos[doc.id] = doc

    def consultar_valido(self, id_: str) -> Documento | None:
        """K2: a garantia central. EXPIRADO nunca é devolvido aqui, mesmo
        que o documento continue fisicamente presente em `documentos`."""
        doc = self.documentos.get(id_)
        if doc is None or doc.estado == EstadoCiclo.EXPIRADO:
            return None
        return doc

    def expirar(self, id_: str) -> None:
        self.documentos[id_].estado = EstadoCiclo.EXPIRADO

    def marcar_expirando(self, id_: str) -> None:
        self.documentos[id_].estado = EstadoCiclo.EXPIRANDO

    def revalidar(self, id_: str) -> None:
        """K6: única forma de um documento voltar de EXPIRANDO para VALIDO
        — sempre uma chamada explícita, nunca implícita por tempo."""
        doc = self.documentos[id_]
        if doc.estado != EstadoCiclo.EXPIRANDO:
            raise ValueError(f"{id_}: só é possível revalidar documento EXPIRANDO")
        doc.estado = EstadoCiclo.VALIDO

    def resolver_conflito(self, indice: int, prevalece: str) -> None:
        c = self.conflitos[indice]
        if prevalece not in c.documentos:
            raise ValueError("prevalece precisa ser um dos documentos em conflito")
        self.conflitos[indice] = Conflito(c.documentos, c.fato_chave, resolvido=True, prevalece=prevalece)
        for id_ in c.documentos:
            if id_ != prevalece:
                self.documentos[id_].estado = EstadoCiclo.EXPIRADO
