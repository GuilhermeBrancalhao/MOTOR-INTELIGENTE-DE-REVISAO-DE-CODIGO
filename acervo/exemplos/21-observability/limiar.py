"""Sinal, limiar e alerta: a diferenca entre observavel e alertavel.

Tres decisoes de desenho, cada uma respondendo a um modo de falha real:

1. **Sucesso tecnico e correcao de resultado sao sinais separados.** Um modelo
   responde sem erro de rede e ainda produz saida errada. Colapsar os dois num
   indicador so torna essa classe de falha invisivel.
2. **Todo sinal que cruza o limiar NOTIFICA, nao apenas registra.** Um alerta que
   fica esperando alguem consultar nao e alerta.
3. **O proprio canal de notificacao e monitorado.** A falha do canal e silenciosa
   por natureza -- o sistema "acha" que avisou e ninguem recebeu.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Categoria(str, Enum):
    MOTIVO_ENCERRAMENTO = "MOTIVO_ENCERRAMENTO"
    INTERVENCAO_HUMANA = "INTERVENCAO_HUMANA"
    CUSTO_LATENCIA = "CUSTO_LATENCIA"
    CANAL_INDISPONIVEL = "CANAL_INDISPONIVEL"


class TipoEtapa(str, Enum):
    IA = "IA"
    DETERMINISTICO = "DETERMINISTICO"


@dataclass(frozen=True)
class Sinal:
    categoria: Categoria
    valor: float
    origem: str


@dataclass(frozen=True)
class Limiar:
    categoria: Categoria
    valor_critico: float
    base_observacao: str
    """De onde o valor veio -- 'p95 de 30 dias', nao um numero redondo escolhido
    antes de existir dado. Sem proveniencia, o limiar nao pode ser reavaliado."""

    def __post_init__(self) -> None:
        if not self.base_observacao.strip():
            raise ValueError("limiar sem proveniencia registrada")


@dataclass
class CanalFalso:
    """Canal de notificacao com heartbeat, para a suite provar os dois caminhos."""

    disponivel: bool = True
    entregues: list[str] = field(default_factory=list)

    def notificar(self, mensagem: str) -> bool:
        if not self.disponivel:
            return False
        self.entregues.append(mensagem)
        return True

    def heartbeat(self) -> bool:
        return self.disponivel


@dataclass(frozen=True)
class Resultado:
    alertou: bool
    notificado: bool
    motivo: str


@dataclass
class Avaliador:
    limiares: dict[Categoria, Limiar]
    canal: CanalFalso
    alertas_reversos: list[str] = field(default_factory=list)

    def avaliar(self, sinal: Sinal) -> Resultado:
        limiar = self.limiares.get(sinal.categoria)
        if limiar is None or sinal.valor < limiar.valor_critico:
            return Resultado(False, False, "abaixo do limiar: alimenta tendencia")

        entregue = self.canal.notificar(f"{sinal.categoria.value}={sinal.valor} de {sinal.origem}")
        if not entregue:
            # A falha do canal e ela mesma um sinal -- nunca silenciosa.
            self.alertas_reversos.append(f"canal indisponivel ao notificar {sinal.categoria.value}")
            return Resultado(True, False, "cruzou o limiar mas a notificacao NAO foi entregue")
        return Resultado(True, True, "notificado")

    def verificar_canal(self) -> bool:
        if not self.canal.heartbeat():
            self.alertas_reversos.append("heartbeat do canal falhou")
            return False
        return True


@dataclass(frozen=True)
class CustoDecomposto:
    etapa_id: str
    tipo: TipoEtapa
    tempo_s: float
    tokens: int | None = None

    def __post_init__(self) -> None:
        if self.tipo is TipoEtapa.DETERMINISTICO and self.tokens is not None:
            raise ValueError("etapa deterministica nao consome tokens")


def somar_tokens(custos: list[CustoDecomposto]) -> int:
    """`None` e 'nao se aplica', nunca zero: tratar como zero faria a etapa
    deterministica parecer artificialmente mais eficiente na comparacao."""
    return sum(c.tokens for c in custos if c.tokens is not None)


def tempo_por_tipo(custos: list[CustoDecomposto]) -> dict[TipoEtapa, float]:
    """A decomposicao obrigatoria: sem ela, um numero agregado nao diz se a
    otimizacao deve ir para o modelo/prompt ou para codigo/infraestrutura."""
    saida = {TipoEtapa.IA: 0.0, TipoEtapa.DETERMINISTICO: 0.0}
    for c in custos:
        saida[c.tipo] += c.tempo_s
    return saida
