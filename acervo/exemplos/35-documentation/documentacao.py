"""Governança de documentação: ADR imutável, versionado, vigência, gerado vs. manual.

As regras W1-W6 formalizadas: `ADR.__post_init__` exige contexto/decisão/
consequência (W1); `RegistroDeADRs.registrar`/`substituir` garantem imutabilidade
com substituição explícita (W2); `Documento.__post_init__` exige
`versionado_junto_do_codigo` (W3) e `fonte_de_verdade` para conteúdo gerado
(W5); `verificar_vigencia` detecta desatualização (W4); `editar_documento`
recusa edição de conteúdo gerado (W5); `publico_alvo` restrito (W6).
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field


class ADRIncompleto(Exception):
    """W1: ADR sem contexto, decisão ou consequência preenchidos."""


class ADRImutavel(Exception):
    """W2: tentativa de sobrescrever ADR já registrado sem passar por substituir."""


class DocumentoNaoVersionado(Exception):
    """W3: documento fora do controle de versão junto do código."""


class FonteDeVerdadeAusente(Exception):
    """W5: documento gerado automaticamente sem fonte de verdade declarada."""


class DocumentoDesatualizado(Exception):
    """W4: documento afirma algo que o código não faz mais."""


class EdicaoManualDeConteudoGerado(Exception):
    """W5: tentativa de editar manualmente documento gerado automaticamente."""


class PublicoAlvoInvalido(Exception):
    """W6: público-alvo diferente de USUARIO ou MANTENEDOR."""


_PUBLICOS_VALIDOS = {"USUARIO", "MANTENEDOR"}


@dataclass(frozen=True)
class ADR:
    numero: int
    titulo: str
    contexto: str
    decisao: str
    consequencia: str
    status: str = "ACEITO"
    supersede: int | None = None

    def __post_init__(self) -> None:
        if not all([self.contexto, self.decisao, self.consequencia]):
            raise ADRIncompleto(f"ADR {self.numero} sem contexto, decisao ou consequencia (W1)")


@dataclass
class RegistroDeADRs:
    adrs: dict = field(default_factory=dict)

    def registrar(self, adr: ADR) -> None:
        if adr.numero in self.adrs:
            raise ADRImutavel(f"ADR {adr.numero} ja existe, use substituir (W2)")
        self.adrs[adr.numero] = adr

    def substituir(self, adr_novo: ADR) -> None:
        if adr_novo.supersede is None or adr_novo.supersede not in self.adrs:
            raise ValueError("substituir exige supersede apontando para ADR existente")
        anterior = self.adrs[adr_novo.supersede]
        self.adrs[anterior.numero] = dataclasses.replace(anterior, status="SUPERADO")
        self.registrar(adr_novo)


@dataclass(frozen=True)
class Documento:
    titulo: str
    versionado_junto_do_codigo: bool
    publico_alvo: str
    gerado_automaticamente: bool = False
    fonte_de_verdade: str | None = None

    def __post_init__(self) -> None:
        if not self.versionado_junto_do_codigo:
            raise DocumentoNaoVersionado(f"documento '{self.titulo}' fora do controle de versao (W3)")
        if self.publico_alvo not in _PUBLICOS_VALIDOS:
            raise PublicoAlvoInvalido(
                f"publico_alvo '{self.publico_alvo}' invalido, use USUARIO ou MANTENEDOR (W6)"
            )
        if self.gerado_automaticamente and not self.fonte_de_verdade:
            raise FonteDeVerdadeAusente(
                f"documento gerado '{self.titulo}' sem fonte de verdade declarada (W5)"
            )


@dataclass(frozen=True)
class VerificacaoDeVigencia:
    documento: str
    afirmacao: str
    ainda_verdadeiro_no_codigo: bool


def verificar_vigencia(verificacao: VerificacaoDeVigencia) -> None:
    if not verificacao.ainda_verdadeiro_no_codigo:
        raise DocumentoDesatualizado(
            f"documento '{verificacao.documento}' afirma algo que o codigo nao faz mais: "
            f"'{verificacao.afirmacao}' (W4)"
        )


def editar_documento(doc: Documento, novo_conteudo: str) -> str:
    if doc.gerado_automaticamente:
        raise EdicaoManualDeConteudoGerado(
            f"documento '{doc.titulo}' e gerado automaticamente; edite {doc.fonte_de_verdade} (W5)"
        )
    return novo_conteudo
