"""Semantic classifier for knowledge gaps.

This module is deterministic and dependency-free. It approximates semantic
classification through weighted keyword families and confidence scoring.
"""
from __future__ import annotations

SEVERIDADES: tuple[str, ...] = ("critico", "alto", "medio", "baixo")

_CATEGORIAS: dict[str, tuple[str, ...]] = {
    "seguranca": (
        "seguranca", "vulner", "token", "segredo", "auth", "autentic", "jwt", "xss", "csrf",
        "injec", "sql injection", "privilege", "credencial",
    ),
    "performance": (
        "performance", "lento", "latencia", "timeout", "cpu", "memoria", "otimiz", "throughput",
    ),
    "concorrencia": (
        "concorr", "race", "deadlock", "lock", "thread", "sincron", "programa.lock", "estado.lock",
    ),
    "testes": (
        "teste", "pytest", "xunit", "nunit", "mstest", "coverage", "assert", "flaky",
    ),
    "arquitetura": (
        "arquitet", "acopl", "camada", "dominio", "clean", "solid", "refator", "design",
    ),
    "documentacao": (
        "doc", "document", "readme", "mermaid", "adr", "diagrama",
    ),
}

_TECNOLOGIAS: dict[str, tuple[str, ...]] = {
    "csharp": ("c#", ".cs", "csproj", "linq", "asp.net", "dotnet", "nullable", "async"),
    "vbnet": ("vb.net", ".vb", "vbproj", "option strict", "on error resume next"),
    "fsharp": ("f#", ".fs", "fsproj", "union", "pattern match", "failwith"),
    "python": ("python", ".py", "pyproject", "pytest", "asyncio"),
    "typescript": ("typescript", "tsconfig", ".tsx", ".ts"),
    "react": ("react", "jsx", "tsx", "useeffect", "state"),
    "fastapi": ("fastapi", "router", "pydantic", "uvicorn"),
    "postgresql": ("postgres", "postgresql", "pg_", "sql"),
    "sqlite": ("sqlite", "sqlite3", ".db"),
}

_CRITICO: tuple[str, ...] = (
    "critico", "bloque", "vulner", "seguran", "incidente", "perda", "corrup",
)

_ALTO: tuple[str, ...] = ("erro", "falha", "quebra", "timeout", "reprovado")


def _normalizar(texto: str) -> str:
    return " ".join(str(texto or "").strip().lower().split())


def _contar_tokens(texto: str, tokens: tuple[str, ...]) -> int:
    return sum(1 for token in tokens if token in texto)


def _categoria_semantica(texto: str) -> tuple[str, int]:
    melhor = "geral"
    pontos = 0
    for categoria, tokens in _CATEGORIAS.items():
        score = _contar_tokens(texto, tokens)
        if score > pontos:
            melhor = categoria
            pontos = score
    return melhor, pontos


def _tecnologia(texto: str, cartoes: list[str], tecnologia_inicial: str) -> tuple[str, int]:
    melhor = tecnologia_inicial or "geral"
    pontos = 0

    permitidas = set(cartoes) if cartoes else set(_TECNOLOGIAS.keys())
    if tecnologia_inicial:
        permitidas.add(tecnologia_inicial)

    for tecnologia, tokens in _TECNOLOGIAS.items():
        if tecnologia not in permitidas:
            continue
        score = _contar_tokens(texto, tokens)
        if score > pontos:
            melhor = tecnologia
            pontos = score

    return melhor or "geral", pontos


def _severidade(texto: str, severidade_inicial: str) -> tuple[str, int]:
    if _contar_tokens(texto, _CRITICO):
        return "critico", 3
    if _contar_tokens(texto, _ALTO):
        return "alto", 2
    if severidade_inicial in SEVERIDADES:
        return severidade_inicial, 1
    return "medio", 1


def _sugestao(categoria_semantica: str, evidencia: str, categoria_origem: str) -> str:
    if categoria_semantica == "seguranca":
        return "Adicionar armadilhas de seguranca e checklist de validacao no cartao alvo."
    if categoria_semantica == "performance":
        return "Adicionar praticas de medicao e otimizacao no cartao alvo."
    if categoria_semantica == "concorrencia":
        return "Adicionar regra de lock/estado atomico e teste de corrida no cartao alvo."
    if categoria_semantica == "testes":
        return "Adicionar criterios de aceite executavel e anti-flaky no cartao alvo."
    if categoria_semantica == "arquitetura":
        return "Adicionar convencoes de camada e acoplamento baixo no cartao alvo."
    if categoria_origem == "diff_pendente":
        return "Reforcar checklist de revisao para diff pendente no cartao alvo."
    return f"Registrar padrao para evitar reincidencia: {evidencia}."


def classificar(
    *,
    evidencia: str,
    cartoes: list[str],
    categoria_origem: str,
    severidade_inicial: str,
    tecnologia_inicial: str,
) -> dict:
    """Classifies a gap with semantic metadata and confidence.

    Returns a stable dict to be embedded in `lacunas.jsonl`.
    """
    texto = _normalizar(evidencia)
    categoria_semantica, pontos_categoria = _categoria_semantica(texto)
    tecnologia, pontos_tecnologia = _tecnologia(texto, cartoes, tecnologia_inicial)
    severidade, pontos_severidade = _severidade(texto, severidade_inicial)

    pontos = pontos_categoria + pontos_tecnologia + pontos_severidade
    confianca = min(0.95, 0.35 + (pontos * 0.12))
    origem = "ia-semantica" if pontos_categoria or pontos_tecnologia else "regra"

    return {
        "tecnologia": tecnologia,
        "categoria_semantica": categoria_semantica,
        "severidade": severidade,
        "confianca": round(confianca, 2),
        "origem": origem,
        "sugestao": _sugestao(categoria_semantica, evidencia, categoria_origem),
    }
