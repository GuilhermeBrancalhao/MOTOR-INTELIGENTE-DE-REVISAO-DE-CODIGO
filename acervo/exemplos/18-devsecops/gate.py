"""Gate de segurança contínuo: controle declarado, waiver com prazo, bloqueio por padrão.

As regras D1-D6 formalizadas: `Controle` sem `verificacao_automatizada` é reportado
como lacuna (D1/D6); `GateDeSeguranca.avaliar` bloqueia toda falha sem waiver ativo
(D2); `Waiver.esta_ativo` trata expiração sem exigir revogação manual (D3).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Controle:
    nome: str
    vetor_de_risco: str
    verificacao_automatizada: str | None = None

    @property
    def tem_automacao(self) -> bool:
        return self.verificacao_automatizada is not None


@dataclass(frozen=True)
class Waiver:
    controle_nome: str
    motivo: str
    expira_em: str  # "YYYY-MM-DD", comparação lexicográfica é suficiente no formato ISO

    def esta_ativo(self, data_atual: str) -> bool:
        return data_atual <= self.expira_em


@dataclass(frozen=True)
class FalhaBloqueante:
    controle: str
    vetor_de_risco: str


@dataclass(frozen=True)
class Lacuna:
    controle: str


@dataclass(frozen=True)
class Excecao:
    controle: str
    motivo: str


@dataclass
class ResultadoGate:
    aprovado: bool
    falhas_bloqueantes: list[FalhaBloqueante] = field(default_factory=list)
    lacunas: list[Lacuna] = field(default_factory=list)
    excecoes: list[Excecao] = field(default_factory=list)


@dataclass
class GateDeSeguranca:
    controles: list[Controle]

    def avaliar(
        self,
        resultados: dict[str, bool],
        waivers: list[Waiver],
        data_atual: str,
    ) -> ResultadoGate:
        """`resultados` mapeia identificador de verificação automatizada -> passou (bool).
        Um controle ausente de `resultados` e sem `verificacao_automatizada` vira lacuna."""
        falhas: list[FalhaBloqueante] = []
        lacunas: list[Lacuna] = []
        excecoes: list[Excecao] = []

        waivers_por_controle = {w.controle_nome: w for w in waivers}

        for controle in self.controles:
            if not controle.tem_automacao:
                lacunas.append(Lacuna(controle.nome))
                continue

            passou = resultados.get(controle.verificacao_automatizada, False)
            if passou:
                continue

            waiver = waivers_por_controle.get(controle.nome)
            if waiver is not None and waiver.esta_ativo(data_atual):
                excecoes.append(Excecao(controle.nome, waiver.motivo))
                continue

            falhas.append(FalhaBloqueante(controle.nome, controle.vetor_de_risco))

        return ResultadoGate(
            aprovado=not falhas,
            falhas_bloqueantes=falhas,
            lacunas=lacunas,
            excecoes=excecoes,
        )
