"""Governança de IA: dono nomeado, classificação de risco, revisão humana, auditoria.

As regras G1-G6 formalizadas: `RegistroDeCasosDeUso.registrar_caso` exige dono
(G1); `verificar_pronto_para_producao` exige classificação (G2) e aprovação
(G5); `registrar_decisao` exige revisão humana para risco ALTO/CRITICO (G3);
histórico imutável de decisões (G4); `RevisaoPeriodica` acumula sem substituir
(G6).
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from enum import Enum


class NivelDeRisco(str, Enum):
    BAIXO = "BAIXO"
    MEDIO = "MEDIO"
    ALTO = "ALTO"
    CRITICO = "CRITICO"


_NIVEIS_QUE_EXIGEM_REVISAO_HUMANA = {NivelDeRisco.ALTO, NivelDeRisco.CRITICO}


class DonoResponsavelAusente(Exception):
    """G1: caso de uso sem responsável nomeado."""


class CasoDeUsoNaoClassificado(Exception):
    """G2: verificação de produção para caso nunca registrado."""


class RevisaoHumanaAusente(Exception):
    """G3: decisão de risco alto/crítico sem revisão humana real."""


class AprovacaoAusente(Exception):
    """G5: produção sem aprovação explícita registrada."""


@dataclass(frozen=True)
class CasoDeUso:
    nome: str
    nivel_de_risco: NivelDeRisco
    dono_responsavel: str
    aprovado_para_producao: bool = False


@dataclass(frozen=True)
class DecisaoAutomatizada:
    caso_de_uso: str
    entrada: dict
    modelo_usado: str
    decisao: str
    revisada_por_humano: bool = False


@dataclass(frozen=True)
class RevisaoPeriodica:
    caso_de_uso: str
    data: str
    nivel_confirmado: NivelDeRisco
    dono_confirmado: str


@dataclass
class RegistroDeCasosDeUso:
    casos: dict = field(default_factory=dict)
    trilha_de_auditoria: list = field(default_factory=list)
    historico_de_revisoes: list = field(default_factory=list)

    def registrar_caso(self, caso: CasoDeUso) -> None:
        if not caso.dono_responsavel:
            raise DonoResponsavelAusente(f"caso '{caso.nome}' sem dono responsavel (G1)")
        self.casos[caso.nome] = caso

    def aprovar_para_producao(self, nome: str, aprovado: bool) -> None:
        caso = self.casos.get(nome)
        if caso is None:
            raise CasoDeUsoNaoClassificado(f"caso '{nome}' nao classificado (G2)")
        self.casos[nome] = dataclasses.replace(caso, aprovado_para_producao=aprovado)

    def verificar_pronto_para_producao(self, nome: str) -> None:
        caso = self.casos.get(nome)
        if caso is None:
            raise CasoDeUsoNaoClassificado(f"caso '{nome}' nao classificado (G2)")
        if not caso.aprovado_para_producao:
            raise AprovacaoAusente(f"caso '{nome}' sem aprovacao explicita para producao (G5)")

    def registrar_decisao(self, decisao: DecisaoAutomatizada) -> None:
        caso = self.casos.get(decisao.caso_de_uso)
        if caso is None:
            raise CasoDeUsoNaoClassificado(f"caso '{decisao.caso_de_uso}' nao classificado (G2)")
        if caso.nivel_de_risco in _NIVEIS_QUE_EXIGEM_REVISAO_HUMANA and not decisao.revisada_por_humano:
            raise RevisaoHumanaAusente(
                f"decisao de risco {caso.nivel_de_risco} exige revisao humana (G3)"
            )
        self.trilha_de_auditoria.append(decisao)  # G4: imutavel, nunca editado

    def revisar_periodicamente(self, revisao: RevisaoPeriodica) -> None:
        self.historico_de_revisoes.append(revisao)  # G6: acumula, nunca substitui
