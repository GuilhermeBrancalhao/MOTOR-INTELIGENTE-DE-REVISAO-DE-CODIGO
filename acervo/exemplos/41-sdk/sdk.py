"""Modelo mínimo de disciplina de SDK exposto a desenvolvedor externo.

Formaliza AC1-AC6 do volume 41-SDK: versionamento semântico real, superfície
pública mínima e deliberada, erro que orienta correção, compatibilidade
retroativa dentro da mesma versão maior, depreciação explícita antes de
remoção, e exemplo de uso sempre verificado.
"""

from dataclasses import dataclass, field


class VersionamentoIncorreto(Exception):
    """AC1 — mudança que quebra compatibilidade sem versão maior nova."""


class ExposicaoSemJustificativa(Exception):
    """AC2 — membro público sem motivo declarado."""


class ErroSemOrientacao(Exception):
    """AC3 — erro do SDK criado sem orientação de correção."""


class DepreciacaoSemMotivo(Exception):
    """AC5 — membro marcado como depreciado sem motivo declarado."""


class RemocaoSemDeprecacao(Exception):
    """AC5 — membro público removido sem ciclo de depreciação prévio."""


class MembroNaoEncontrado(Exception):
    """Remoção de membro que não existe na superfície."""


class ExemploNaoVerificado(Exception):
    """AC6 — exemplo de uso aceito sem verificação contra o código real."""


@dataclass(frozen=True)
class VersaoSemantica:
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass(frozen=True)
class MudancaDeSuperficie:
    descricao: str
    quebra_compatibilidade: bool


def validar_release(
    versao_anterior: VersaoSemantica,
    versao_nova: VersaoSemantica,
    mudanca: MudancaDeSuperficie,
) -> None:
    """AC1 — mudança que quebra compatibilidade sempre exige versão maior nova."""
    if mudanca.quebra_compatibilidade and versao_nova.major == versao_anterior.major:
        raise VersionamentoIncorreto(
            f"mudanca '{mudanca.descricao}' quebra compatibilidade mas versao "
            f"maior nao mudou ({versao_anterior} -> {versao_nova}) (AC1)"
        )


@dataclass(frozen=True)
class MembroDeSDK:
    nome: str
    publico: bool
    motivo_publico: str = ""
    depreciado: bool = False
    motivo_de_depreciacao: str = ""

    def __post_init__(self) -> None:
        if self.publico and not self.motivo_publico:
            raise ExposicaoSemJustificativa(
                f"membro '{self.nome}' marcado como publico sem motivo declarado (AC2)"
            )
        if self.depreciado and not self.motivo_de_depreciacao:
            raise DepreciacaoSemMotivo(
                f"membro '{self.nome}' marcado como depreciado sem motivo declarado (AC5)"
            )


@dataclass(frozen=True)
class ErroDoSDK:
    o_que_falhou: str
    como_corrigir: str

    def __post_init__(self) -> None:
        if not self.como_corrigir:
            raise ErroSemOrientacao(
                f"erro '{self.o_que_falhou}' criado sem orientacao de correcao (AC3)"
            )


@dataclass
class SuperficieDoSDK:
    versao_atual: VersaoSemantica
    membros: dict = field(default_factory=dict)

    def adicionar_membro(self, membro: MembroDeSDK) -> None:
        self.membros[membro.nome] = membro

    def remover_membro(self, nome: str, nova_versao: VersaoSemantica) -> None:
        """AC4/AC5 — remoção de membro público exige depreciação prévia e versão maior nova."""
        membro = self.membros.get(nome)
        if membro is None:
            raise MembroNaoEncontrado(f"membro '{nome}' nao existe na superficie atual")
        if membro.publico:
            if not membro.depreciado:
                raise RemocaoSemDeprecacao(
                    f"membro publico '{nome}' removido sem ciclo de depreciacao previo (AC5)"
                )
            if nova_versao.major == self.versao_atual.major:
                raise VersionamentoIncorreto(
                    f"remocao de membro publico '{nome}' exige versao maior nova "
                    f"({self.versao_atual} -> {nova_versao}) (AC1/AC4)"
                )
        del self.membros[nome]
        self.versao_atual = nova_versao


@dataclass(frozen=True)
class ExemploDeUso:
    descricao: str
    codigo: str
    resultado_verificado: bool = False


def aceitar_exemplo(exemplo: ExemploDeUso) -> None:
    """AC6 — todo exemplo de uso é verificado contra o código real do SDK."""
    if not exemplo.resultado_verificado:
        raise ExemploNaoVerificado(
            f"exemplo '{exemplo.descricao}' nao foi verificado contra o SDK real (AC6)"
        )
