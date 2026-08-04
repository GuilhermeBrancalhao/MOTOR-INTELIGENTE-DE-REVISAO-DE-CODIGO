"""Geração de código: validado, marcado, reproduzível, revisado, especificação versionada.

As regras Y1-Y6 formalizadas: `aceitar_codigo_gerado` exige validação bem-
sucedida (Y1) e revisão humana (Y4); `CodigoNaoMarcado`/`editar_codigo_gerado`
garantem marcação e imutabilidade manual (Y2); `gerar` é determinístico por
ausência de estado externo (Y3); `EspecificacaoDeGeracao.__post_init__` exige
versão (Y5) e escopo declarado (Y6).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


class EspecificacaoIncompleta(Exception):
    """Y5/Y6: especificação de geração sem versão ou escopo declarado."""


class CodigoNaoMarcado(Exception):
    """Y2: código gerado sem a marcação correspondente."""


class ResultadoDeValidacaoAusente(Exception):
    """Y1: código gerado submetido sem resultado de validação."""


class ValidacaoFalhou(Exception):
    """Y1: código gerado não compilou ou não passou nos testes."""


class RevisaoHumanaAusente(Exception):
    """Y4: código gerado sem revisão humana registrada."""


class EdicaoManualDeCodigoGerado(Exception):
    """Y2: tentativa de editar diretamente código marcado como gerado."""


@dataclass(frozen=True)
class EspecificacaoDeGeracao:
    nome: str
    prompt_ou_fonte: str
    versao: str
    escopo_declarado: str

    def __post_init__(self) -> None:
        if not all([self.prompt_ou_fonte, self.versao, self.escopo_declarado]):
            raise EspecificacaoIncompleta(
                f"especificacao '{self.nome}' sem versao ou escopo declarado (Y5/Y6)"
            )


@dataclass(frozen=True)
class ResultadoDeValidacao:
    compilou: bool
    testes_passaram: bool


@dataclass(frozen=True)
class CodigoGerado:
    especificacao: EspecificacaoDeGeracao
    conteudo: str
    marcado_como_gerado: bool
    validacao: ResultadoDeValidacao | None = None
    revisado_por_humano: bool = False


def gerar(
    especificacao: EspecificacaoDeGeracao, gerador: Callable[[EspecificacaoDeGeracao], str]
) -> CodigoGerado:
    conteudo = gerador(especificacao)  # Y3: depende so da especificacao e do gerador
    return CodigoGerado(especificacao=especificacao, conteudo=conteudo, marcado_como_gerado=True)


def aceitar_codigo_gerado(codigo: CodigoGerado) -> None:
    if not codigo.marcado_como_gerado:
        raise CodigoNaoMarcado("codigo gerado sem marcacao correspondente (Y2)")
    if codigo.validacao is None:
        raise ResultadoDeValidacaoAusente("codigo gerado sem resultado de validacao (Y1)")
    if not (codigo.validacao.compilou and codigo.validacao.testes_passaram):
        raise ValidacaoFalhou("codigo gerado nao compilou ou nao passou nos testes (Y1)")
    if not codigo.revisado_por_humano:
        raise RevisaoHumanaAusente("codigo gerado sem revisao humana registrada (Y4)")


def editar_codigo_gerado(codigo: CodigoGerado, novo_conteudo: str) -> str:
    if codigo.marcado_como_gerado:
        raise EdicaoManualDeCodigoGerado(
            "codigo marcado como gerado; ajuste a especificacao e gere novamente (Y2)"
        )
    return novo_conteudo
