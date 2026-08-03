"""O laco decisao-acao-observacao, com o guardiao no lugar certo.

Uma acao por passo, guardiao consultado antes de cada chamada ao modelo, e motivo
de encerramento sempre explicito no resultado. O modelo entra como um `Callable`
para que a suite prove o comportamento do motor sem depender de modelo real -- a
garantia que importa nao e a qualidade da resposta, e o que o motor faz diante de
qualquer resposta, inclusive invalida.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from orcamento import Guardiao, Motivo, Orcamento


@dataclass(frozen=True)
class ChamarFerramenta:
    nome: str
    argumentos: dict


@dataclass(frozen=True)
class RespostaFinal:
    conteudo: str


@dataclass(frozen=True)
class Observacao:
    conteudo: str
    erro: bool = False
    recuperavel: bool = True


@dataclass(frozen=True)
class Passo:
    numero: int
    acao: object
    observacao: Observacao | None


@dataclass(frozen=True)
class Resultado:
    motivo: Motivo
    passos: tuple[Passo, ...]
    saida: str | None

    def __post_init__(self) -> None:
        # `saida` so existe quando o objetivo foi atingido. A ausencia do valor e
        # o sinal estrutural de que o resultado nao esta completo.
        if self.motivo is not Motivo.OBJETIVO_ATINGIDO and self.saida is not None:
            raise ValueError("saida so pode existir com OBJETIVO_ATINGIDO")


class ContratoViolado(Exception):
    """O modelo devolveu algo que nao e uma das duas acoes previstas."""


def executar(modelo, ferramentas: dict, orcamento: Orcamento, custo_por_passo=(10, 0.1)) -> Resultado:
    """Roda o laco ate um dos tres motivos de encerramento.

    `modelo` recebe o historico e devolve `ChamarFerramenta` ou `RespostaFinal`.
    Qualquer outra coisa e violacao de contrato e encerra sem despachar nada.
    """
    guardiao = Guardiao(orcamento)
    passos: list[Passo] = []
    historico: list[Passo] = []
    tokens, tempo = custo_por_passo

    while True:
        if not guardiao.pode_seguir():
            return Resultado(Motivo.ORCAMENTO_EXCEDIDO, tuple(passos), None)

        acao = modelo(tuple(historico))

        if isinstance(acao, RespostaFinal):
            passos.append(Passo(len(passos) + 1, acao, None))
            return Resultado(Motivo.OBJETIVO_ATINGIDO, tuple(passos), acao.conteudo)

        if not isinstance(acao, ChamarFerramenta):
            return Resultado(Motivo.ERRO_NAO_RECUPERAVEL, tuple(passos), None)

        fn = ferramentas.get(acao.nome)
        if fn is None:
            return Resultado(Motivo.ERRO_NAO_RECUPERAVEL, tuple(passos), None)

        try:
            obs = fn(**acao.argumentos)
        except Exception as e:  # erro de ferramenta vira observacao, nunca sobe
            obs = Observacao(str(e), erro=True, recuperavel=True)

        passo = Passo(len(passos) + 1, acao, obs)
        passos.append(passo)
        historico.append(passo)
        guardiao.registrar_passo(tokens, tempo)

        if obs.erro and not obs.recuperavel:
            return Resultado(Motivo.ERRO_NAO_RECUPERAVEL, tuple(passos), None)
