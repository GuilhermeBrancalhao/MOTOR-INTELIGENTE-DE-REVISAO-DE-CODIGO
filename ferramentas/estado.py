"""Estado do ENGINE: persistência em disco e máquina de fases.

O estado vive em `<projeto>/.engine/estado.json`. É disco, não contexto — é isso que
faz o modo sobreviver à compactação.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

FASES: tuple[str, ...] = (
    "DESCOBERTA",
    "ANALISE",
    "EVOLUCAO",
    "PLANO",
    "BUILD",
    "TESTE",
    "REVISAO",
    "DOC",
    "ENTREGA",
)

TRANSICOES: dict[str, tuple[str, ...]] = {
    "DESCOBERTA": ("ANALISE",),
    "ANALISE": ("EVOLUCAO", "PLANO"),
    "EVOLUCAO": ("PLANO",),
    "PLANO": ("BUILD",),
    "BUILD": ("TESTE",),
    "TESTE": ("BUILD", "REVISAO"),
    "REVISAO": ("BUILD", "DOC"),
    "DOC": ("ENTREGA",),
    "ENTREGA": (),
}

VERSAO = 1


class TransicaoInvalida(Exception):
    """Passagem de fase que não existe no grafo da especificação."""


def caminho(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "estado.json"


def carregar(raiz: Path) -> dict | None:
    alvo = caminho(raiz)
    if not alvo.is_file():
        return None
    try:
        return json.loads(alvo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None


def gravar(raiz: Path, dados: dict) -> None:
    """Escrita atômica: grava num temporário e substitui.

    Um hook interrompido no meio da escrita não pode deixar o estado corrompido —
    seria a única forma de o motor perder o ciclo sem ninguém perceber.
    """
    alvo = caminho(raiz)
    alvo.parent.mkdir(parents=True, exist_ok=True)
    temporario = alvo.with_suffix(".json.tmp")
    temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporario, alvo)


def novo_ciclo(raiz: Path, objetivo: str, agora: str, modo: str = "normal") -> dict:
    dados = {
        "versao": VERSAO,
        "ativo": True,
        "ciclo": {
            "id": f"{agora[:10]}-1",
            "objetivo": objetivo,
            "iniciado_em": agora,
            "modo": modo,
        },
        "fase": "DESCOBERTA",
        "fases_concluidas": [],
        "cartoes": [],
        "decisoes": [],
        "pendencias": [],
        "diffs_pendentes": [],
        "cobrancas_por_fase": {},
    }
    gravar(raiz, dados)
    return dados


def transicionar(dados: dict, destino: str) -> dict:
    atual = dados["fase"]
    if destino not in TRANSICOES.get(atual, ()):
        permitidas = ", ".join(TRANSICOES.get(atual, ())) or "nenhuma"
        raise TransicaoInvalida(
            f"{atual} -> {destino} não existe no grafo; a partir de {atual} só: {permitidas}"
        )
    if atual not in dados["fases_concluidas"]:
        dados["fases_concluidas"].append(atual)
    dados["fase"] = destino
    return dados


def desligar(raiz: Path) -> dict:
    dados = carregar(raiz) or {}
    dados["ativo"] = False
    gravar(raiz, dados)
    return dados


def registrar_diff(raiz: Path, caminho_arquivo: str) -> dict:
    dados = carregar(raiz)
    if dados is None:
        return {}
    pendentes = dados.setdefault("diffs_pendentes", [])
    if caminho_arquivo not in pendentes:
        pendentes.append(caminho_arquivo)
    gravar(raiz, dados)
    return dados
