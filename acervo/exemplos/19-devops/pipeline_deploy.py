"""Pipeline de entrega: sequência não pulável, rollout gradual, reversão, artefato imutável.

As regras P1-P6 formalizadas: `Pipeline.executar_estagio` bloqueia estágio fora de
ordem e após falha (P1/P5); `Pipeline` congelado impede reatribuir `artefato` (P6);
`implantar_em_producao` rejeita deploy completo sem justificativa (P3);
`GerenciadorDeploy` rastreia o artefato atual (P4) e reverte para o anterior (P2).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Estagio(str, Enum):
    BUILD = "BUILD"
    TESTE = "TESTE"
    SEGURANCA = "SEGURANCA"
    STAGING = "STAGING"
    PRODUCAO = "PRODUCAO"


ORDEM = [Estagio.BUILD, Estagio.TESTE, Estagio.SEGURANCA, Estagio.STAGING, Estagio.PRODUCAO]


class EstagioForaDeOrdem(Exception):
    """P5: estágio executado fora da posição esperada da sequência."""


class EstagioFalhou(Exception):
    """P1/P5: um estágio falhou; nenhum estágio seguinte pode rodar."""


class PipelineIncompleto(Exception):
    """P1: deploy solicitado sem que todos os estágios anteriores tenham passado."""


class DeployCompletoRequerJustificativa(Exception):
    """P3: deploy de 100% do tráfego sem forcar_completo=True."""


class SemVersaoAnteriorParaReverter(Exception):
    """P2: reversão solicitada sem histórico anterior no ambiente."""


@dataclass(frozen=True)
class Artefato:
    hash: str
    commit: str


@dataclass(frozen=True)
class Pipeline:
    artefato: Artefato
    estagios_concluidos: list = field(default_factory=list)

    def executar_estagio(self, estagio: Estagio, passou: bool) -> None:
        idx_esperado = len(self.estagios_concluidos)
        if idx_esperado >= len(ORDEM) or ORDEM[idx_esperado] != estagio:
            raise EstagioForaDeOrdem(
                f"esperado {ORDEM[idx_esperado] if idx_esperado < len(ORDEM) else 'nenhum'}, "
                f"recebido {estagio} (P5)"
            )
        if not passou:
            raise EstagioFalhou(f"{estagio} falhou, pipeline bloqueado (P1/P5)")
        self.estagios_concluidos.append(estagio)

    def pronto_para_producao(self) -> bool:
        return self.estagios_concluidos == ORDEM[:-1]

    def implantar_em_producao(
        self, gerenciador: "GerenciadorDeploy", percentual: int = 25, forcar_completo: bool = False
    ):
        if not self.pronto_para_producao():
            raise PipelineIncompleto("nem todos os estagios anteriores passaram (P1)")
        if percentual == 100 and not forcar_completo:
            raise DeployCompletoRequerJustificativa(
                "deploy completo exige forcar_completo=True (P3)"
            )
        self.executar_estagio(Estagio.PRODUCAO, True)
        return gerenciador.registrar(self.artefato, percentual)


@dataclass(frozen=True)
class RegistroDeploy:
    artefato: Artefato
    percentual: int
    e_rollback: bool = False


@dataclass
class GerenciadorDeploy:
    historico: list = field(default_factory=list)

    def registrar(self, artefato: Artefato, percentual: int, e_rollback: bool = False) -> RegistroDeploy:
        registro = RegistroDeploy(artefato, percentual, e_rollback)
        self.historico.append(registro)
        return registro

    def artefato_atual(self) -> Artefato | None:
        if not self.historico:
            return None
        return self.historico[-1].artefato

    def reverter(self) -> RegistroDeploy:
        if len(self.historico) < 2:
            raise SemVersaoAnteriorParaReverter("nao ha versao anterior para reverter (P2)")
        artefato_anterior = self.historico[-2].artefato
        return self.registrar(artefato_anterior, 100, e_rollback=True)
