"""Classificacao de risco por comprovacao de inocuidade, nao por enumeracao de perigo.

A decisao central deste modulo e a inversao do default, e ela tem custo historico
documentado: uma lista de proibicoes foi contornada doze vezes em sete rodadas de
revisao adversarial antes de a abordagem mudar. A razao e estrutural -- comando de
shell e uma linguagem propria, com aspas, substituicao e variantes por plataforma,
e enumerar o que e perigoso dentro dela nao termina.

Aqui a regra e a inversa: **so o que se prova inocuo por construcao e LIVRE.**
Nenhum comando de shell atinge esse nivel, sem excecao por conteudo -- e o teste
`test_nenhum_comando_de_shell_e_livre` trava essa politica contra reintroducao.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

TETO_DE_TAMANHO = 20_000
"""Acima disto, trava sem analisar. Analisar comando gigante por padrao de texto e
caro e explorável como negacao de servico contra o proprio classificador -- travar
e o lado certo do erro."""


class Nivel(str, Enum):
    TRAVADO = "TRAVADO"
    RASTREADO = "RASTREADO"
    LIVRE = "LIVRE"


class Origem(str, Enum):
    """De onde veio o texto que motivou a acao."""

    OPERADOR = "OPERADOR"
    PROCESSADO = "PROCESSADO"


class Tipo(str, Enum):
    SHELL = "SHELL"
    ARQUIVO_LEITURA = "ARQUIVO_LEITURA"
    ARQUIVO_ESCRITA = "ARQUIVO_ESCRITA"
    REDE = "REDE"


@dataclass(frozen=True)
class Acao:
    tipo: Tipo
    conteudo: str = ""
    destino: str | None = None
    origem: Origem = Origem.OPERADOR


@dataclass(frozen=True)
class Classificacao:
    nivel: Nivel
    familia: str
    motivo: str


@dataclass(frozen=True)
class Politica:
    """Configuracao por sistema. `caminhos_protegidos` inclui o proprio painel de
    controle do classificador -- um mecanismo de seguranca que nao se protege nao
    se protege de fato (a familia R9 nasceu exatamente desse buraco)."""

    destinos_autorizados: frozenset[str] = field(default_factory=frozenset)
    caminhos_protegidos: tuple[str, ...] = (".engine/", ".git/hooks/", ".claude/")


def classificar(acao: Acao, politica: Politica) -> Classificacao:
    """Devolve o nivel de risco. Nunca devolve LIVRE para shell."""
    if len(acao.conteudo) > TETO_DE_TAMANHO:
        return Classificacao(Nivel.TRAVADO, "R12", "acima do teto de tamanho: nao inspecionavel")

    if acao.tipo is Tipo.ARQUIVO_ESCRITA and acao.destino:
        alvo = acao.destino.replace("\\", "/")
        for protegido in politica.caminhos_protegidos:
            if protegido in alvo:
                return Classificacao(Nivel.TRAVADO, "R9", f"escrita em caminho protegido: {protegido}")

    if acao.tipo is Tipo.REDE:
        if acao.destino not in politica.destinos_autorizados:
            return Classificacao(Nivel.TRAVADO, "R2", f"destino nao autorizado: {acao.destino}")
        if acao.origem is Origem.PROCESSADO:
            return Classificacao(
                Nivel.TRAVADO, "R1", "saida de dado decidida a partir de conteudo de origem nao confiavel"
            )
        return Classificacao(Nivel.RASTREADO, "R2", "saida de dado para destino autorizado")

    if acao.tipo is Tipo.SHELL:
        # Nunca LIVRE. A escolha entre TRAVADO e RASTREADO e um refinamento;
        # a garantia e que nenhum ramo aqui devolve LIVRE.
        if acao.origem is Origem.PROCESSADO:
            return Classificacao(Nivel.TRAVADO, "R8", "comando influenciado por conteudo de origem nao confiavel")
        return Classificacao(Nivel.RASTREADO, "R8", "comando de shell: conteudo nao inspecionavel a fundo")

    if acao.tipo is Tipo.ARQUIVO_ESCRITA:
        return Classificacao(Nivel.RASTREADO, "R10", "escrita em arquivo")

    return Classificacao(Nivel.LIVRE, "-", "leitura de arquivo: inocua por construcao")
