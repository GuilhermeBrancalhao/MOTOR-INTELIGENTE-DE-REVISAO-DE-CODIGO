"""Roteamento em tempo de execução: fallback por degradação, recuperação com estabilidade.

As regras L1-L6 formalizadas: `Roteador.rotear` recusa candidato não aprovado
(L1); fallback automático sob degradação (L2); toda decisão vai a `historico`
(L3); `JanelaDeSaude.esta_degradado` exige amostra mínima (L4); retorno ao
principal exige janela de estabilidade (L5); `estado_de` é sempre consultável
(L6).
"""

from __future__ import annotations

from dataclasses import dataclass, field


class CandidatoNaoAprovado(Exception):
    """L1: candidato de roteamento fora da lista aprovada pelo 26."""


@dataclass(frozen=True)
class SinalDeSaude:
    total_chamadas: int
    falhas: int
    latencia_media_ms: float


@dataclass(frozen=True)
class JanelaDeSaude:
    limiar_taxa_falha: float = 0.5
    limiar_latencia_ms: float = 5000.0
    minimo_de_chamadas: int = 5

    def esta_degradado(self, sinal: SinalDeSaude) -> bool:
        if sinal.total_chamadas < self.minimo_de_chamadas:
            return False  # L4: amostra insuficiente para julgar degradacao
        taxa_falha = sinal.falhas / sinal.total_chamadas
        return taxa_falha >= self.limiar_taxa_falha or sinal.latencia_media_ms >= self.limiar_latencia_ms


@dataclass(frozen=True)
class DecisaoDeRoteamento:
    tarefa: str
    candidato_escolhido: str
    motivo: str


@dataclass
class Roteador:
    candidatos_aprovados: set
    janela: JanelaDeSaude = field(default_factory=JanelaDeSaude)
    janela_estabilidade: int = 3
    estado_atual: dict = field(default_factory=dict)
    consecutivas_saudaveis: dict = field(default_factory=dict)
    historico: list = field(default_factory=list)

    def rotear(
        self, tarefa: str, principal: str, fallback: str, sinal_principal: SinalDeSaude
    ) -> DecisaoDeRoteamento:
        if principal not in self.candidatos_aprovados or fallback not in self.candidatos_aprovados:
            raise CandidatoNaoAprovado(
                f"candidato nao aprovado pelo 26 para tarefa '{tarefa}' (L1)"
            )

        estado_anterior = self.estado_atual.get(tarefa, principal)
        degradado = self.janela.esta_degradado(sinal_principal)

        if estado_anterior == fallback:
            if degradado:
                self.consecutivas_saudaveis[tarefa] = 0
                decisao = DecisaoDeRoteamento(tarefa, fallback, "principal_ainda_degradado")
            else:
                contagem = self.consecutivas_saudaveis.get(tarefa, 0) + 1
                self.consecutivas_saudaveis[tarefa] = contagem
                if contagem >= self.janela_estabilidade:
                    self.estado_atual[tarefa] = principal
                    self.consecutivas_saudaveis[tarefa] = 0
                    decisao = DecisaoDeRoteamento(
                        tarefa, principal, "recuperado_apos_janela_de_estabilidade"
                    )
                else:
                    decisao = DecisaoDeRoteamento(tarefa, fallback, "ainda_em_janela_de_estabilidade")
        else:
            if degradado:
                self.estado_atual[tarefa] = fallback
                decisao = DecisaoDeRoteamento(tarefa, fallback, "fallback_por_degradacao")
            else:
                decisao = DecisaoDeRoteamento(tarefa, principal, "principal_saudavel")

        self.historico.append(decisao)  # L3
        return decisao

    def estado_de(self, tarefa: str) -> str | None:
        return self.estado_atual.get(tarefa)  # L6
