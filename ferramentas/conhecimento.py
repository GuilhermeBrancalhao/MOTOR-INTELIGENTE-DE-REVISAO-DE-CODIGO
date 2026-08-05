"""Knowledge learning layer from ENGINE reports.

Turns report findings into a persistent backlog so new projects can feed future
knowledge updates.
"""
from __future__ import annotations

import hashlib
import json
import unicodedata
from datetime import datetime
from pathlib import Path

from ferramentas import classificador_semantico, relatorio

SEVERIDADES: tuple[str, ...] = ("critico", "alto", "medio", "baixo")
_CRITICAL_TOKENS: tuple[str, ...] = (
    "bloque",
    "erro",
    "falha",
    "seguran",
    "vulner",
    "quebra",
    "incidente",
)


def caminho_lacunas(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "lacunas.jsonl"


def caminho_backlog(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "backlog_conhecimento.json"


def caminho_pendentes(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "conhecimento_pendente"


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _normalizar_texto(texto: str) -> str:
    base = unicodedata.normalize("NFKD", str(texto or ""))
    sem_acento = "".join(ch for ch in base if not unicodedata.combining(ch))
    return " ".join(sem_acento.strip().lower().split())


def _id_lacuna(ciclo: str, categoria: str, evidencia: str) -> str:
    bruto = f"{_normalizar_texto(ciclo)}|{categoria}|{_normalizar_texto(evidencia)}"
    return hashlib.sha1(bruto.encode("utf-8")).hexdigest()[:12]


def _severidade_para_pendencia(texto: str) -> str:
    alvo = _normalizar_texto(texto)
    if any(token in alvo for token in _CRITICAL_TOKENS):
        return "critico"
    return "alto"


def _sugerir(evidencia: str, categoria: str) -> str:
    if categoria == "diff_pendente":
        return "Adicionar checklist de revisao e exemplos no cartao da tecnologia afetada."
    if categoria == "pendencia":
        return f"Registrar padrao/armadilha para evitar reincidencia: {evidencia}."
    return "Revisar e atualizar o conhecimento relacionado ao item."


def _escolher_tecnologia(texto: str, cartoes: list[str]) -> str:
    alvo = _normalizar_texto(texto)
    for tecnologia in cartoes:
        if _normalizar_texto(tecnologia) in alvo:
            return tecnologia
    if len(cartoes) == 1:
        return cartoes[0]
    return "geral"


def extrair_do_relatorio(texto_relatorio: str, ciclo: str, fase: str, cartoes: list[str]) -> list[dict]:
    """Extracts knowledge gaps from cycle report markdown.

    MVP scope: parse two explicit sections that already exist in the report.
    """
    secao = ""
    lacunas: list[dict] = []
    for linha in str(texto_relatorio or "").splitlines():
        bruta = linha.strip()
        if bruta.startswith("## "):
            secao = _normalizar_texto(bruta)
            continue
        if not bruta.startswith("- "):
            continue
        evidencia = bruta[2:].strip()
        if not evidencia:
            continue

        if "pendenc" in secao and "abertas" in secao:
            categoria = "pendencia"
            severidade = _severidade_para_pendencia(evidencia)
        elif "diffs por apresentar" in secao:
            categoria = "diff_pendente"
            severidade = "medio"
        else:
            continue

        tecnologia = _escolher_tecnologia(evidencia, cartoes)
        classificada = classificador_semantico.classificar(
            evidencia=evidencia,
            cartoes=cartoes,
            categoria_origem=categoria,
            severidade_inicial=severidade,
            tecnologia_inicial=tecnologia,
        )
        lacunas.append(
            {
                "id": _id_lacuna(ciclo, categoria, evidencia),
                "ciclo": ciclo,
                "fase": fase,
                "tecnologia": classificada["tecnologia"],
                "categoria": categoria,
                "categoria_semantica": classificada["categoria_semantica"],
                "severidade": classificada["severidade"],
                "confianca": classificada["confianca"],
                "origem": classificada["origem"],
                "evidencia": evidencia,
                "sugestao": classificada["sugestao"] or _sugerir(evidencia, categoria),
                "status": "aberta",
            }
        )
    return lacunas


def _ler_jsonl(caminho: Path) -> list[dict]:
    if not caminho.is_file():
        return []
    linhas: list[dict] = []
    try:
        for linha in caminho.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(linha)
            except json.JSONDecodeError:
                continue
            if isinstance(item, dict):
                linhas.append(item)
    except OSError:
        return []
    return linhas


def _gravar_jsonl(caminho: Path, itens: list[dict]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("a", encoding="utf-8") as arquivo:
        for item in itens:
            arquivo.write(json.dumps(item, ensure_ascii=False) + "\n")


def _consolidar_abertas(historico: list[dict]) -> list[dict]:
    por_id: dict[str, dict] = {}
    for item in historico:
        if not isinstance(item, dict):
            continue
        ident = str(item.get("id") or "")
        if not ident:
            continue
        por_id[ident] = item
    return [item for item in por_id.values() if item.get("status", "aberta") != "fechada"]


def _gravar_backlog(raiz: Path, ciclo: str, abertas: list[dict]) -> dict:
    contagem = {nivel: 0 for nivel in SEVERIDADES}
    for item in abertas:
        sev = str(item.get("severidade") or "").lower()
        if sev in contagem:
            contagem[sev] += 1

    ordem = {nivel: indice for indice, nivel in enumerate(SEVERIDADES)}
    itens_ordenados = sorted(
        abertas,
        key=lambda item: (
            ordem.get(str(item.get("severidade") or "baixo"), len(ordem)),
            str(item.get("tecnologia") or ""),
            str(item.get("categoria") or ""),
            str(item.get("id") or ""),
        ),
    )

    payload = {
        "gerado_em": _agora(),
        "ciclo": ciclo,
        "resumo": contagem,
        "itens": itens_ordenados,
    }
    caminho = caminho_backlog(raiz)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return payload


def _atualizar_pendentes(raiz: Path, abertas: list[dict]) -> list[Path]:
    por_tecnologia: dict[str, list[dict]] = {}
    for item in abertas:
        tecnologia = str(item.get("tecnologia") or "geral")
        por_tecnologia.setdefault(tecnologia, []).append(item)

    diretorio = caminho_pendentes(raiz)
    diretorio.mkdir(parents=True, exist_ok=True)
    gerados: list[Path] = []
    for tecnologia, itens in sorted(por_tecnologia.items()):
        linhas = [
            f"# Pendencias de conhecimento: {tecnologia}",
            "",
            "Gerado automaticamente pelo comando `conhecimento atualizar`.",
            "",
        ]
        for item in itens[:20]:
            linhas.append(f"- [{item.get('severidade', 'medio')}] {item.get('evidencia', '')}")
            linhas.append(f"  - sugestao: {item.get('sugestao', '')}")
            lines_id = f"  - id: {item.get('id', '')}"
            linhas.append(lines_id)
        alvo = diretorio / f"{tecnologia}.md"
        alvo.write_text("\n".join(linhas) + "\n", encoding="utf-8")
        gerados.append(alvo)
    return gerados


def atualizar_por_relatorio(raiz: Path, dados_estado: dict | None) -> dict:
    """Extracts gaps from current report and updates knowledge artifacts."""
    dados = dados_estado if isinstance(dados_estado, dict) else {}
    ciclo = str((dados.get("ciclo") or {}).get("id") or "")
    fase = str(dados.get("fase") or "")
    cartoes = [str(item) for item in (dados.get("cartoes") or []) if item]

    texto = relatorio.de_ciclo(raiz)
    novas = extrair_do_relatorio(texto, ciclo, fase, cartoes)

    historico = _ler_jsonl(caminho_lacunas(raiz))
    existentes = {str(item.get("id") or "") for item in historico}
    agora = _agora()
    para_gravar: list[dict] = []
    for item in novas:
        if item["id"] in existentes:
            continue
        novo = dict(item)
        novo["aberta_em"] = agora
        para_gravar.append(novo)

    if para_gravar:
        _gravar_jsonl(caminho_lacunas(raiz), para_gravar)
        historico += para_gravar

    abertas = _consolidar_abertas(historico)
    backlog = _gravar_backlog(raiz, ciclo, abertas)
    gerados = _atualizar_pendentes(raiz, abertas)

    return {
        "novas": len(para_gravar),
        "abertas": len(abertas),
        "criticas": backlog.get("resumo", {}).get("critico", 0),
        "arquivos_pendentes": [str(caminho) for caminho in gerados],
    }


def lacunas_criticas_do_estado(dados_estado: dict | None) -> list[str]:
    """Critical pending items that should block DOC -> ENTREGA."""
    dados = dados_estado if isinstance(dados_estado, dict) else {}
    pendencias = [str(item) for item in (dados.get("pendencias") or []) if item]
    return [item for item in pendencias if _severidade_para_pendencia(item) == "critico"]
