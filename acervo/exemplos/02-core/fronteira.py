"""A fronteira de saída como código: onde o não-determinismo para de valer.

As oito regras (N1-N8) resumidas em uma frase: antes da fronteira, texto livre
do modelo; depois, dado com tipo, validado em três camadas na ordem certa —
forma, domínio, autorização (N3) — e sem efeito nenhum enquanto a validação
não passar (N4).

A consequência prática de N6 (contexto determinístico) e N2 (nada além da
fronteira recebe texto livre) é que tudo neste módulo, exceto a própria
chamada ao modelo, roda sem rede e sem modelo real — é por isso que o
`ChamadaModelo` abaixo é um `Callable` injetado, nunca uma dependência fixa.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable


class MotivoRejeicao(str, Enum):
    FORMA = "FORMA"
    DOMINIO = "DOMINIO"
    AUTORIZACAO = "AUTORIZACAO"


class SemEfeito(Exception):
    """Levantada quando algo tenta agir a partir de resposta rejeitada.
    N4: falha de validação nunca produz efeito, sem exceção."""


@dataclass(frozen=True)
class Contexto:
    """Montado sem relógio, sem aleatório, sem estado global (N6) — dado o
    mesmo dado de entrada, o mesmo Contexto, sempre."""

    partes: tuple[str, ...]

    def texto(self) -> str:
        return "\n".join(self.partes)


def montar_contexto(entrada: dict) -> Contexto:
    """Determinística por construção: nenhuma chamada externa, nenhum
    `datetime.now()`, nenhuma leitura de variável global."""
    partes = tuple(f"{k}: {v}" for k, v in sorted(entrada.items()))
    return Contexto(partes)


@dataclass(frozen=True)
class RespostaValidada:
    """O único formato que atravessa a fronteira de saída. Depois daqui, o
    resto do sistema trata isto como trataria qualquer dado externo comum."""

    campo: str
    valor: str


ChamadaModelo = Callable[[Contexto], str]
"""A única linha do sistema que não é determinística — assinatura estreita
de propósito, para que o vazamento de N2 seja visível no tipo."""


def validar_forma(texto: str, campos_esperados: frozenset[str]) -> dict | None:
    """Camada 1: o texto parece o formato esperado? Aqui é JSON simples
    'campo=valor', uma linha; formato real seria mais rico, a ordem de
    validacao e o ponto que importa, nao o parser."""
    partes = texto.strip().split("=", 1)
    if len(partes) != 2:
        return None
    campo, valor = partes
    if campo not in campos_esperados:
        return None
    return {"campo": campo, "valor": valor}


def validar_dominio(dado: dict, valores_permitidos: frozenset[str]) -> bool:
    """Camada 2: mesmo bem formado, o valor faz sentido no domínio?"""
    return dado["valor"] in valores_permitidos


def validar_autorizacao(campo: str, campos_autorizados: frozenset[str]) -> bool:
    """Camada 3: mesmo válido no domínio, quem pediu pode mudar este campo?
    N5: falha aqui nunca se corrige com retry — é recusa, não erro transitório."""
    return campo in campos_autorizados


def atravessar_fronteira(
    resposta_bruta: str,
    campos_esperados: frozenset[str],
    valores_permitidos: frozenset[str],
    campos_autorizados: frozenset[str],
) -> tuple[RespostaValidada | None, MotivoRejeicao | None]:
    """A fronteira de saída (N1): um único lugar nomeável por onde toda
    resposta do modelo precisa passar antes de virar dado tipado.

    A ordem das três camadas é a regra, não um detalhe: forma antes de
    domínio antes de autorização — cada camada assume que a anterior já
    filtrou, e invertê-las abriria a possibilidade de autorizar um campo
    cuja forma nem foi checada.
    """
    dado = validar_forma(resposta_bruta, campos_esperados)
    if dado is None:
        return None, MotivoRejeicao.FORMA
    if not validar_dominio(dado, valores_permitidos):
        return None, MotivoRejeicao.DOMINIO
    if not validar_autorizacao(dado["campo"], campos_autorizados):
        return None, MotivoRejeicao.AUTORIZACAO
    return RespostaValidada(dado["campo"], dado["valor"]), None


def aplicar_efeito(resposta: RespostaValidada | None, motivo: MotivoRejeicao | None) -> str:
    """N4, em código: sem `RespostaValidada`, não existe caminho que produza
    efeito — a exceção não é tratamento de erro, é a garantia em si."""
    if resposta is None:
        raise SemEfeito(f"rejeitada: {motivo.value if motivo else 'desconhecido'}")
    return f"aplicado: {resposta.campo}={resposta.valor}"
