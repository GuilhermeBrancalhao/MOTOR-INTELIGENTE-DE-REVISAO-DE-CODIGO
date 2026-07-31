"""Estado do ENGINE: persistência em disco e máquina de fases.

O estado vive em `<projeto>/.engine/estado.json`. É disco, não contexto — é isso que
faz o modo sobreviver à compactação.
"""
from __future__ import annotations

import json
import os
import re
from datetime import datetime
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


class EstadoCorrompido(Exception):
    """O arquivo de estado existe, mas não é JSON válido ou não é um objeto.

    Sobrescrever nesse caso apagaria um ciclo em andamento sem ninguém perceber —
    por isso é um erro explícito, não um `None` silencioso.
    """


class CicloJaAtivo(Exception):
    """Já existe um ciclo ativo; `novo_ciclo` recusa sobrescrevê-lo sem `forcar=True`."""


def caminho(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "estado.json"


def carregar(raiz: Path) -> dict | None:
    """Devolve `None` tanto quando o estado não existe quanto quando está corrompido.

    Usada pelos hooks: falhar ali não pode derrubar o turno do usuário, então os
    dois casos "sem estado" e "estado ilegível" são tratados como equivalentes.
    """
    alvo = caminho(raiz)
    if not alvo.is_file():
        return None
    try:
        return json.loads(alvo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return None


def carregar_estrito(raiz: Path) -> dict | None:
    """Como `carregar`, mas distingue "não existe" de "existe e está quebrado".

    Devolve `None` só quando o arquivo não existe. Quando existe mas o conteúdo não
    é JSON válido (ou não é um objeto), levanta `EstadoCorrompido` em vez de
    devolver `None` — quem grava por cima do estado precisa saber da diferença para
    não apagar um ciclo em andamento.
    """
    alvo = caminho(raiz)
    if not alvo.is_file():
        return None
    try:
        dados = json.loads(alvo.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as erro:
        raise EstadoCorrompido(f"estado ilegível em {alvo}: {erro}") from erro
    if not isinstance(dados, dict):
        raise EstadoCorrompido(f"estado em {alvo} não é um objeto JSON")
    return dados


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


def novo_ciclo(
    raiz: Path, objetivo: str, agora: str, modo: str = "normal", forcar: bool = False
) -> dict:
    """Abre um ciclo novo, gravando por cima do estado anterior (se houver).

    Recusa sobrescrever um ciclo ainda ativo a menos que `forcar=True` — sem essa
    trava, chamar `novo_ciclo` duas vezes perderia silenciosamente o ciclo em
    andamento (cartões, decisões, pendências, diffs pendentes).

    O `id` do ciclo é `<dia>-<n>`, onde `n` conta quantos ciclos já existiram nesse
    dia segundo `historico` — a lista (preservada entre ciclos) de todos os ids já
    usados. Isso evita colisão de id quando dois ciclos abrem no mesmo dia.

    Estado corrompido NUNCA é sobrescrito em silêncio: `carregar_estrito` (não o
    `carregar` tolerante, que devolve `None` tanto para "não existe" quanto para
    "quebrado") distingue os dois casos, e o arquivo ilegível é preservado com o
    mesmo mecanismo de renomeação do `desligar` (`estado.corrompido-<carimbo>.json`)
    ANTES de o ciclo novo ser gravado. O `historico` dentro dele estava ilegível de
    qualquer forma — mas continua recuperável no arquivo preservado.
    """
    try:
        existente = carregar_estrito(raiz)
    except EstadoCorrompido:
        _preservar_estado_corrompido(raiz, agora)
        existente = None
    historico: list[str] = []
    if existente is not None:
        if existente.get("ativo") and not forcar:
            objetivo_ativo = existente.get("ciclo", {}).get("objetivo", "?")
            raise CicloJaAtivo(
                f"já existe um ciclo ativo (objetivo: {objetivo_ativo!r}); "
                "use forcar=True para sobrescrevê-lo"
            )
        historico = list(existente.get("historico", []))

    dia = agora[:10]
    numero = sum(1 for id_usado in historico if id_usado.startswith(f"{dia}-")) + 1
    novo_id = f"{dia}-{numero}"
    historico.append(novo_id)

    dados = {
        "versao": VERSAO,
        "ativo": True,
        "ciclo": {
            "id": novo_id,
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
        "historico": historico,
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


def desligar(raiz: Path, agora: str | None = None) -> dict:
    """Marca o estado como inativo, preservando um estado corrompido em vez de apagá-lo.

    Antes, `carregar(raiz) or {}` tratava "corrompido" igual a "não existe" e
    gravava um dicionário vazio por cima — apagando `ciclo`, `cartoes`, `decisoes`,
    `pendencias` e `diffs_pendentes` de um ciclo em andamento. Agora, se o JSON
    estiver quebrado, o arquivo original é renomeado para
    `estado.corrompido-<carimbo>.json` antes de qualquer gravação nova.
    """
    try:
        dados = carregar_estrito(raiz)
    except EstadoCorrompido:
        _preservar_estado_corrompido(raiz, agora)
        dados = None
    dados = dados or {}
    dados["ativo"] = False
    gravar(raiz, dados)
    return dados


def _preservar_estado_corrompido(raiz: Path, agora: str | None) -> None:
    carimbo = agora if agora is not None else datetime.now().strftime("%Y%m%d%H%M%S")
    # `agora` pode ser um instante ISO (`2026-07-31T10:00:00`), e `:` é inválido em
    # nome de arquivo no Windows — o carimbo é saneado para caracteres seguros.
    carimbo = re.sub(r"[^0-9A-Za-z._-]", "-", carimbo)
    alvo = caminho(raiz)
    destino = alvo.parent / f"estado.corrompido-{carimbo}.json"
    os.replace(alvo, destino)


def registrar_diff(raiz: Path, caminho_arquivo: str) -> dict:
    """Registra um diff pendente. Levanta `EstadoCorrompido` se o estado existir e
    estiver ilegível — sem estado (arquivo ausente) continua devolvendo `{}` em
    silêncio, porque esse caminho é chamado por hooks que não podem quebrar o turno.
    """
    dados = carregar_estrito(raiz)
    if dados is None:
        return {}
    pendentes = dados.setdefault("diffs_pendentes", [])
    if caminho_arquivo not in pendentes:
        pendentes.append(caminho_arquivo)
    gravar(raiz, dados)
    return dados
