"""Estado de interface para chamada de IA: carregamento distinto, streaming, fallback marcado.

As regras F1-F6 formalizadas: `RequisicaoDeIA.iniciar` marca CARREGANDO distinto de
OCIOSO (F1); `receber_fragmento` acumula incrementalmente (F2); `resolver_exibicao`
nunca ambigua fresco vs. fallback (F3); `promover_para_global` exige autorização
(F4); `cancelar` descarta fragmento tardio (F5); `adaptar_resposta_do_provedor`
isola o formato bruto (F6).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EstadoCarregamento(str, Enum):
    OCIOSO = "OCIOSO"
    CARREGANDO = "CARREGANDO"
    ERRO = "ERRO"
    CANCELADO = "CANCELADO"
    CONCLUIDO = "CONCLUIDO"


class RequisicaoJaFinalizada(Exception):
    """Fragmento recebido fora do estado CARREGANDO (exceto pós-cancelamento, que é ignorado)."""


class PromocaoNaoAutorizada(Exception):
    """F4: promoção de resposta de IA a estado global sem autorização explícita."""


@dataclass
class RequisicaoDeIA:
    id: str
    estado: EstadoCarregamento = EstadoCarregamento.OCIOSO
    fragmentos: list = field(default_factory=list)
    erro: str | None = None

    def iniciar(self) -> None:
        self.estado = EstadoCarregamento.CARREGANDO

    def receber_fragmento(self, texto: str) -> None:
        if self.estado == EstadoCarregamento.CANCELADO:
            return  # F5: fragmento tardio apos cancelamento e descartado
        if self.estado != EstadoCarregamento.CARREGANDO:
            raise RequisicaoJaFinalizada(f"nao pode receber fragmento em estado {self.estado}")
        self.fragmentos.append(texto)  # F2: acumulo incremental

    def texto_parcial(self) -> str:
        return "".join(self.fragmentos)

    def concluir(self) -> None:
        if self.estado == EstadoCarregamento.CANCELADO:
            return
        self.estado = EstadoCarregamento.CONCLUIDO

    def falhar(self, motivo: str) -> None:
        if self.estado == EstadoCarregamento.CANCELADO:
            return
        self.estado = EstadoCarregamento.ERRO
        self.erro = motivo

    def cancelar(self) -> None:
        self.estado = EstadoCarregamento.CANCELADO  # F5


@dataclass(frozen=True)
class ResultadoExibido:
    texto: str
    e_fallback: bool


def resolver_exibicao(requisicao: RequisicaoDeIA, cache_anterior: str | None) -> ResultadoExibido | None:
    """F1/F3: nunca retorna resultado enquanto carrega; nunca ambigua fresco vs. fallback."""
    if requisicao.estado == EstadoCarregamento.CONCLUIDO:
        return ResultadoExibido(requisicao.texto_parcial(), e_fallback=False)
    if requisicao.estado == EstadoCarregamento.ERRO and cache_anterior is not None:
        return ResultadoExibido(cache_anterior, e_fallback=True)
    return None


def promover_para_global(
    requisicao: RequisicaoDeIA, estado_global: dict, chave: str, autorizado: bool
) -> None:
    if not autorizado:
        raise PromocaoNaoAutorizada(f"promocao de '{chave}' exige autorizacao explicita (F4)")
    estado_global[chave] = requisicao.texto_parcial()


def adaptar_resposta_do_provedor(bruta: dict, adaptador) -> str:
    """F6: a UI nunca consome o formato bruto do provedor diretamente."""
    return adaptador(bruta)
