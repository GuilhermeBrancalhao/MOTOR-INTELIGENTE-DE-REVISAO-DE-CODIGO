"""Pipeline de RAG: recuperar, reordenar, confirmar validade, medir fidelidade.

As seis regras (R1-R6) formalizadas: `reordenar` produz `score_relevancia`
distinto de `score_proximidade` (R3); `confirmar_validade` roda depois da
reordenação (R6); `compor_resposta` recusa explicitamente sem candidato
válido (R4); `medir_fidelidade` roda depois da geração, nunca presumida (R2).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Candidato:
    id_documento: str
    score_proximidade: float
    score_relevancia: float | None = None


@dataclass(frozen=True)
class Citacao:
    id_documento: str
    trecho: str
    valido_no_momento_da_citacao: bool


@dataclass(frozen=True)
class RespostaComFidelidade:
    texto: str
    citacoes: tuple[Citacao, ...]
    fidelidade: float
    recusada: bool
    motivo_recusa: str | None = None


def reordenar(candidatos: tuple[Candidato, ...], pergunta: str, relevancia_por_id: dict) -> tuple[Candidato, ...]:
    """R3: score_relevancia é calculado aqui, distinto de score_proximidade
    já presente nos candidatos recuperados."""
    reordenados = [
        Candidato(c.id_documento, c.score_proximidade, relevancia_por_id.get(c.id_documento, 0.0))
        for c in candidatos
    ]
    reordenados.sort(key=lambda c: c.score_relevancia, reverse=True)
    return tuple(reordenados)


def confirmar_validade(candidatos: tuple[Candidato, ...], consultar_valido) -> tuple[Candidato, ...]:
    """R6: validade checada agora, no momento da consulta — nunca herdada
    de quando o documento foi indexado. `consultar_valido` é a função de
    11-KNOWLEDGE injetada, para não acoplar este pipeline a uma implementação."""
    return tuple(c for c in candidatos if consultar_valido(c.id_documento) is not None)


def compor_resposta(
    candidatos_validos: tuple[Candidato, ...],
    gerar_texto,
    trechos_por_id: dict,
    afirmacoes_sustentadas: set,
) -> RespostaComFidelidade:
    """R4: recusa explícita sem candidato válido. R2: fidelidade medida
    depois da geração via `medir_fidelidade`, nunca assumida aqui."""
    if not candidatos_validos:
        return RespostaComFidelidade("", (), 0.0, recusada=True, motivo_recusa="sem fonte valida suficiente")

    citacoes = tuple(
        Citacao(c.id_documento, trechos_por_id.get(c.id_documento, ""), valido_no_momento_da_citacao=True)
        for c in candidatos_validos
    )
    texto = gerar_texto(candidatos_validos)
    fidelidade = medir_fidelidade(texto, citacoes, afirmacoes_sustentadas)
    return RespostaComFidelidade(texto, citacoes, fidelidade, recusada=False)


def medir_fidelidade(texto: str, citacoes: tuple[Citacao, ...], afirmacoes_sustentadas: set) -> float:
    """R2: fidelidade é proporção de afirmações extraídas do texto que
    rastreiam a alguma citação. `afirmacoes_sustentadas` simula o resultado
    de um extrator real, que não é o foco deste exemplo mínimo."""
    afirmacoes = _extrair_afirmacoes(texto)
    if not afirmacoes:
        return 1.0
    sustentadas = sum(1 for a in afirmacoes if a in afirmacoes_sustentadas)
    return sustentadas / len(afirmacoes)


def _extrair_afirmacoes(texto: str) -> tuple[str, ...]:
    return tuple(s.strip() for s in texto.split(".") if s.strip())
