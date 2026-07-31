#!/usr/bin/env python3
"""Hook UserPromptSubmit estendido — injeta motores + volumes PRONTO.

Extends engine_contexto.py para carregar:
1. Motores relevantes para a fase (revisar-codigo, materializar-ideia, etc)
2. Volumes de conhecimento PRONTO do acervo externo (07-PROMPT-ENGINE, 12-MEMORY, 31-TESTING)

Ambos carregados dinamicamente, dentro do teto de linhas do cartão.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import forcar_utf8, raiz_do_ciclo  # noqa: E402

forcar_utf8()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ferramentas import config, estado  # noqa: E402


# Mapeamento: fase → motores consultáveis
MOTORES_POR_FASE = {
    "DESCOBERTA": [],  # Descobridor não consulta motores
    "ANALISE": [],  # Cartografo não consulta motores
    "PLANO": ["arquitetar-sistema", "materializar-ideia"],
    "EVOLUCAO": ["arquitetar-sistema"],
    "BUILD": ["materializar-ideia", "revisar-codigo"],
    "TESTE": [],  # Testador não consulta (ainda)
    "REVISAO": ["revisar-codigo", "otimizar-performance"],
    "DOC": ["diagramar"],
    "ENTREGA": [],
}

# Volumes sempre disponíveis se PRONTO
VOLUMES_PRONTOS = [
    "07-PROMPT-ENGINE",
    "12-MEMORY",
    "31-TESTING",
]

INVARIANTES = (
    "1. Nunca afirmar sucesso sem ter olhado. Rodou, cola a saída; não rodou, diz que não rodou.",
    "2. Nunca ajustar o teste para o código passar. O teste é o contrato.",
    "3. Nunca inventar arquivo, API, número ou regra de negócio. Sem evidência, é pendência.",
    "4. Nunca tocar em item fora do escopo declarado do ciclo.",
    "5. Toda decisão técnica sai com a justificativa junto.",
)

MINIMO_CARTAO = 9


def _teto_efetivo(cfg: dict) -> int:
    bruto = cfg.get("teto_cartao_linhas", 40)
    try:
        teto = int(bruto)
    except (TypeError, ValueError):
        teto = 40
    return max(teto, MINIMO_CARTAO)


def _cortar(texto: str, limite: int) -> str:
    texto = " ".join(str(texto).split())
    return texto if len(texto) <= limite else texto[: limite - 1] + "…"


def _ler_descricao_motor(raiz: Path, motor: str) -> Optional[str]:
    """Lê a descrição do motor de seu SKILL.md."""
    skill_path = raiz / "motores" / motor / "SKILL.md"
    if not skill_path.exists():
        return None

    try:
        conteudo = skill_path.read_text(encoding="utf-8")
        # Extrai a descrição do frontmatter (entre ---)
        linhas = conteudo.split("\n")
        in_frontmatter = False
        for linha in linhas:
            if linha.startswith("---"):
                in_frontmatter = not in_frontmatter
            elif in_frontmatter and linha.startswith("description:"):
                # Remove 'description: ' e aspas
                desc = linha.replace("description:", "").strip().strip('"').strip("'")
                return _cortar(desc, 100)
    except Exception:
        pass

    return None


def _ler_resumo_volume(raiz: Path, volume: str) -> Optional[str]:
    """Lê resumo do volume de seu README ou _VOLUME.yml."""
    # Tenta volume_prontos primeiro (symlink), depois o acervo externo
    volume_path = raiz / "volumes" / "prontos" / volume
    if not volume_path.exists():
        # Fallback para caminho absoluto (exemplo: onde o acervo estiver clonado)
        volume_path = Path.home() / "projetos" / "acervo" / volume

    if not volume_path.exists():
        return None

    try:
        # Tenta README.md
        readme = volume_path / "README.md"
        if readme.exists():
            conteudo = readme.read_text(encoding="utf-8")
            # Pega primeira linha não-vazia
            for linha in conteudo.split("\n"):
                if linha.strip() and not linha.startswith("#"):
                    return _cortar(linha.strip(), 100)

        # Fallback: primeira seção do volume
        primeira = list(volume_path.glob("01-*.md"))
        if primeira:
            conteudo = primeira[0].read_text(encoding="utf-8")
            for linha in conteudo.split("\n"):
                if linha.strip() and linha.startswith("# "):
                    return _cortar(linha.replace("# ", ""), 100)
    except Exception:
        pass

    return f"Volume {volume}"


def montar_cartao_estendido(dados: dict, cfg: dict, raiz: Path) -> str:
    """Monta cartão com motores + volumes injetados."""
    teto = _teto_efetivo(cfg)
    ciclo = dados.get("ciclo", {})
    fase = dados.get("fase", "?")

    cabecalho = [
        "== ENGINE ativo ==",
        f"Fase: {fase}   Modo: {ciclo.get('modo', 'normal')}",
        f"Objetivo: {_cortar(ciclo.get('objetivo', ''), 160)}",
    ]
    rodape = ["Invariantes:", *INVARIANTES]

    orcamento = max(teto - len(cabecalho) - len(rodape), 0)
    corpo: list[str] = []

    def acrescentar(linha: str) -> None:
        if len(corpo) < orcamento:
            corpo.append(linha)

    # Seção: Motores da fase
    motores = MOTORES_POR_FASE.get(fase, [])
    if motores:
        acrescentar("📋 Motores desta fase:")
        for motor in motores:
            desc = _ler_descricao_motor(raiz, motor)
            if desc:
                acrescentar(f"  • {motor}: {desc}")
            else:
                acrescentar(f"  • {motor}")

    # Seção: Volumes PRONTO
    volumes_existentes = []
    for vol in VOLUMES_PRONTOS:
        resumo = _ler_resumo_volume(raiz, vol)
        if resumo:
            volumes_existentes.append((vol, resumo))

    if volumes_existentes:
        acrescentar("📚 Volumes PRONTO (consultáveis):")
        for vol, resumo in volumes_existentes:
            acrescentar(f"  • {vol}: {resumo}")

    # Seção: Cartões (original)
    cartoes = dados.get("cartoes") or []
    if cartoes:
        acrescentar(f"Cartões: {_cortar(', '.join(cartoes), 120)}")

    # Seção: Decisões (original)
    decisoes = dados.get("decisoes") or []
    if decisoes:
        acrescentar("Decisões:")
        for item in decisoes:
            acrescentar(
                f"  - {_cortar(item.get('o_que', ''), 60)}"
            )

    # Seção: Diffs pendentes (original)
    diffs = dados.get("diffs_pendentes") or []
    if diffs:
        acrescentar(f"Diffs ({len(diffs)}): {_cortar(', '.join(diffs), 100)}")

    linhas = cabecalho + corpo[:orcamento] + rodape
    return "\n".join(linhas[:teto])


def principal() -> int:
    try:
        try:
            evento = json.load(sys.stdin)
        except Exception:  # noqa: BLE001
            return 0

        if not isinstance(evento, dict):
            return 0

        raiz = raiz_do_ciclo(Path(evento.get("cwd") or "."))

        dados = estado.carregar(raiz)
        if not dados or not dados.get("ativo"):
            return 0

        cfg = config.carregar(raiz)
        cartao = montar_cartao_estendido(dados, cfg, raiz)

        if cartao.strip():
            print(cartao)
        return 0
    except Exception:  # noqa: BLE001
        return 0


if __name__ == "__main__":
    sys.exit(principal())
