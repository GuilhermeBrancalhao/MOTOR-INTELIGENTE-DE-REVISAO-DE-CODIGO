#!/usr/bin/env python3
"""Hook UserPromptSubmit V3 — injeta motores + volumes + sugestão automática.

Estende V2 adicionando:
1. Análise de diffs locais (git diff)
2. Sugestão automática de motor baseada em padrão de código
3. Injeção de sugestão no cartão (após motores)
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import forcar_utf8, raiz_do_ciclo  # noqa: E402

forcar_utf8()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from ferramentas import config, estado  # noqa: E402

# Importar analisador de diff
try:
    from engine_analisa_diff import AnalisadorDiff
except ImportError:
    AnalisadorDiff = None


# Mapeamento: fase → motores consultáveis
MOTORES_POR_FASE = {
    "DESCOBERTA": [],
    "ANALISE": [],
    "PLANO": ["arquitetar-sistema", "materializar-ideia"],
    "EVOLUCAO": ["arquitetar-sistema"],
    "BUILD": ["materializar-ideia", "revisar-codigo"],
    "TESTE": [],
    "REVISAO": ["revisar-codigo", "otimizar-performance"],
    "DOC": ["diagramar"],
    "ENTREGA": [],
}

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
        linhas = conteudo.split("\n")
        in_frontmatter = False
        for linha in linhas:
            if linha.startswith("---"):
                in_frontmatter = not in_frontmatter
            elif in_frontmatter and linha.startswith("description:"):
                desc = linha.replace("description:", "").strip().strip('"').strip("'")
                return _cortar(desc, 100)
    except Exception:
        pass

    return None


def _ler_resumo_volume(raiz: Path, volume: str) -> Optional[str]:
    """Lê resumo do volume de seu README ou _VOLUME.yml."""
    volume_path = raiz / "volumes" / "prontos" / volume
    if not volume_path.exists():
        volume_path = Path.home() / "projetos" / "acervo" / volume

    if not volume_path.exists():
        return None

    try:
        readme = volume_path / "README.md"
        if readme.exists():
            conteudo = readme.read_text(encoding="utf-8")
            for linha in conteudo.split("\n"):
                if linha.strip() and not linha.startswith("#"):
                    return _cortar(linha.strip(), 100)

        primeira = list(volume_path.glob("01-*.md"))
        if primeira:
            conteudo = primeira[0].read_text(encoding="utf-8")
            for linha in conteudo.split("\n"):
                if linha.strip() and linha.startswith("# "):
                    return _cortar(linha.replace("# ", ""), 100)
    except Exception:
        pass

    return f"Volume {volume}"


def _extrair_diff_local(cwd: str) -> str:
    """Extrai diff local via 'git diff'."""
    try:
        result = subprocess.run(
            ["git", "diff"],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout if result.returncode == 0 else ""
    except Exception:
        return ""


def _analisar_e_sugerir_motor(cwd: str, fase: str) -> Optional[str]:
    """Analisa diff local e sugere motor apropriado."""
    if not AnalisadorDiff:
        return None

    # Não sugerir em fases iniciais
    if fase in ["DESCOBERTA", "ANALISE"]:
        return None

    diff = _extrair_diff_local(cwd)
    if not diff or not diff.strip():
        return None

    try:
        analisador = AnalisadorDiff()
        motor = analisador.analisar_diff(diff)
        if motor:
            return analisador.gerar_sugestao(motor)
    except Exception:
        pass

    return None


def montar_cartao_estendido(dados: dict, cfg: dict, raiz: Path, cwd: str) -> str:
    """Monta cartão com motores + volumes + sugestão automática."""
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

    # Seção: Sugestão automática de motor (V3 novo)
    sugestao = _analisar_e_sugerir_motor(str(cwd), fase)
    if sugestao:
        acrescentar(sugestao)

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
            acrescentar(f"  - {_cortar(item.get('o_que', ''), 60)}")

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

        cwd = evento.get("cwd") or "."
        raiz = raiz_do_ciclo(Path(cwd))

        dados = estado.carregar(raiz)
        if not dados or not dados.get("ativo"):
            return 0

        cfg = config.carregar(raiz)
        cartao = montar_cartao_estendido(dados, cfg, raiz, cwd)

        if cartao.strip():
            print(cartao)
        return 0
    except Exception:  # noqa: BLE001
        return 0


if __name__ == "__main__":
    sys.exit(principal())
