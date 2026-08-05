"""Proposal workflow for smart merge into existing technology cards.

This module builds human-reviewable proposals from backlog items and applies them
only after explicit approval.
"""
from __future__ import annotations

import hashlib
import json
import unicodedata
from datetime import datetime
from pathlib import Path

from ferramentas import conhecimento


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _normalizar(texto: str) -> str:
    base = unicodedata.normalize("NFKD", str(texto or ""))
    sem_acento = "".join(ch for ch in base if not unicodedata.combining(ch))
    return " ".join(sem_acento.lower().split())


def _diretorio_cartoes(diretorio_cartoes: Path | None = None) -> Path:
    if diretorio_cartoes is not None:
        return Path(diretorio_cartoes)
    return Path(__file__).resolve().parent.parent / "cartoes"


def caminho_aprovacoes(raiz: Path) -> Path:
    return Path(raiz) / ".engine" / "aprovacoes_conhecimento.json"


def _carregar_aprovacoes(raiz: Path) -> dict:
    caminho = caminho_aprovacoes(raiz)
    if not caminho.is_file():
        return {"gerado_em": _agora(), "propostas": []}
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return {"gerado_em": _agora(), "propostas": []}
    if not isinstance(dados, dict):
        return {"gerado_em": _agora(), "propostas": []}
    if not isinstance(dados.get("propostas"), list):
        dados["propostas"] = []
    return dados


def _gravar_aprovacoes(raiz: Path, dados: dict) -> None:
    caminho = caminho_aprovacoes(raiz)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def _secao_alvo(item: dict) -> str:
    categoria = str(item.get("categoria_semantica") or "").lower()
    origem = str(item.get("categoria") or "").lower()
    if categoria in {"arquitetura", "documentacao"}:
        return "## Convencoes"
    if categoria == "testes" or origem == "diff_pendente":
        return "## Checklist de review"
    return "## Armadilhas"


def _texto_proposta(item: dict) -> str:
    sugestao = str(item.get("sugestao") or "").strip()
    evidencia = str(item.get("evidencia") or "").strip()
    if sugestao:
        return sugestao
    return evidencia or "Atualizar o cartao com aprendizado observado no ciclo."


def _id_proposta(chave: str) -> str:
    return hashlib.sha1(chave.encode("utf-8")).hexdigest()[:10]


def gerar_propostas(raiz: Path, *, diretorio_cartoes: Path | None = None) -> dict:
    """Generate pending proposals from current backlog.

    Does not mutate any card file.
    """
    caminho_backlog = conhecimento.caminho_backlog(raiz)
    if not caminho_backlog.is_file():
        return {"novas": 0, "pendentes": 0, "propostas": []}

    try:
        backlog = json.loads(caminho_backlog.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError, UnicodeDecodeError):
        return {"novas": 0, "pendentes": 0, "propostas": []}

    itens = backlog.get("itens") if isinstance(backlog, dict) else []
    if not isinstance(itens, list):
        itens = []

    dados = _carregar_aprovacoes(raiz)
    propostas = list(dados.get("propostas") or [])
    chaves_existentes = {str(p.get("chave") or "") for p in propostas}

    diretorio = _diretorio_cartoes(diretorio_cartoes)
    novas = 0
    for item in itens:
        if not isinstance(item, dict):
            continue
        tecnologia = str(item.get("tecnologia") or "").strip()
        if not tecnologia or tecnologia == "geral":
            continue
        cartao = diretorio / f"{tecnologia}.md"
        if not cartao.is_file():
            continue

        secao = _secao_alvo(item)
        texto = _texto_proposta(item)
        chave = "|".join([tecnologia, secao, _normalizar(texto)])
        if chave in chaves_existentes:
            continue

        try:
            conteudo = cartao.read_text(encoding="utf-8")
        except OSError:
            continue
        if _normalizar(texto) in _normalizar(conteudo):
            continue

        proposta = {
            "id": _id_proposta(chave),
            "chave": chave,
            "status": "pendente",
            "tecnologia": tecnologia,
            "cartao": str(cartao),
            "secao": secao,
            "texto": texto,
            "origem_item_id": str(item.get("id") or ""),
            "confianca": item.get("confianca", 0),
            "criada_em": _agora(),
        }
        propostas.append(proposta)
        chaves_existentes.add(chave)
        novas += 1

    dados["gerado_em"] = _agora()
    dados["propostas"] = propostas
    _gravar_aprovacoes(raiz, dados)

    pendentes = [p for p in propostas if p.get("status") == "pendente"]
    return {"novas": novas, "pendentes": len(pendentes), "propostas": pendentes}


def listar_pendentes(raiz: Path) -> list[dict]:
    dados = _carregar_aprovacoes(raiz)
    return [p for p in (dados.get("propostas") or []) if p.get("status") == "pendente"]


def _achar_proposta(propostas: list[dict], proposta_id: str) -> dict | None:
    for proposta in propostas:
        if str(proposta.get("id") or "") == proposta_id:
            return proposta
    return None


def _trecho_da_secao(conteudo: str, secao: str, limite: int = 8) -> str:
    linhas = conteudo.splitlines()
    alvo = _normalizar(secao)
    inicio = -1
    for i, linha in enumerate(linhas):
        if linha.startswith("## ") and _normalizar(linha) == alvo:
            inicio = i
            break
    if inicio < 0:
        return "(secao ainda nao existe no cartao)"

    fim = len(linhas)
    for i in range(inicio + 1, len(linhas)):
        if linhas[i].startswith("## "):
            fim = i
            break
    trecho = linhas[inicio:fim]
    return "\n".join(trecho[:limite]).strip() or "(secao vazia)"


def detalhar(raiz: Path, proposta_id: str, *, diretorio_cartoes: Path | None = None) -> tuple[bool, dict | str]:
    dados = _carregar_aprovacoes(raiz)
    propostas = list(dados.get("propostas") or [])
    proposta = _achar_proposta(propostas, proposta_id)
    if proposta is None:
        return False, f"proposta {proposta_id!r} nao encontrada"

    cartao = Path(str(proposta.get("cartao") or ""))
    if not cartao.is_absolute():
        base = _diretorio_cartoes(diretorio_cartoes)
        cartao = base / f"{proposta.get('tecnologia', '')}.md"

    trecho = "(cartao nao encontrado)"
    if cartao.is_file():
        try:
            trecho = _trecho_da_secao(
                cartao.read_text(encoding="utf-8"),
                str(proposta.get("secao") or "## Armadilhas"),
            )
        except OSError:
            trecho = "(nao foi possivel ler o cartao)"

    return True, {
        "id": proposta.get("id", ""),
        "status": proposta.get("status", ""),
        "tecnologia": proposta.get("tecnologia", ""),
        "secao": proposta.get("secao", ""),
        "texto": proposta.get("texto", ""),
        "confianca": proposta.get("confianca", 0),
        "cartao": str(cartao),
        "trecho": trecho,
    }


def _inserir_no_cartao(conteudo: str, secao: str, texto: str) -> tuple[str, bool]:
    linhas = conteudo.splitlines()
    alvo = _normalizar(secao)
    secao_idx = -1
    for i, linha in enumerate(linhas):
        if linha.startswith("## ") and _normalizar(linha) == alvo:
            secao_idx = i
            break
    if secao_idx < 0:
        linhas += ["", secao, f"- {texto}"]
        return "\n".join(linhas) + "\n", True

    bullet = f"- {texto}"
    if _normalizar(bullet) in _normalizar("\n".join(linhas)):
        return conteudo, False

    insert_idx = len(linhas)
    for i in range(secao_idx + 1, len(linhas)):
        if linhas[i].startswith("## "):
            insert_idx = i
            break

    bloco = linhas[secao_idx + 1 : insert_idx]
    while bloco and not bloco[-1].strip():
        bloco.pop()
    novo_bloco = bloco + [bullet, ""]
    linhas = linhas[: secao_idx + 1] + novo_bloco + linhas[insert_idx:]
    return "\n".join(linhas).rstrip() + "\n", True


def aprovar(raiz: Path, proposta_id: str, *, diretorio_cartoes: Path | None = None) -> tuple[bool, str]:
    dados = _carregar_aprovacoes(raiz)
    propostas = list(dados.get("propostas") or [])
    alvo = _achar_proposta(propostas, proposta_id)

    if alvo is None:
        return False, f"proposta {proposta_id!r} nao encontrada"
    if alvo.get("status") != "pendente":
        return False, f"proposta {proposta_id!r} nao esta pendente"

    cartao = Path(alvo.get("cartao") or "")
    if not cartao.is_absolute():
        base = _diretorio_cartoes(diretorio_cartoes)
        cartao = base / f"{alvo.get('tecnologia', '')}.md"
    if not cartao.is_file():
        return False, f"cartao alvo nao encontrado: {cartao}"

    try:
        conteudo = cartao.read_text(encoding="utf-8")
    except OSError as erro:
        return False, f"nao foi possivel ler o cartao: {erro}"

    novo, mudou = _inserir_no_cartao(conteudo, str(alvo.get("secao") or "## Armadilhas"), str(alvo.get("texto") or ""))
    if mudou:
        try:
            cartao.write_text(novo, encoding="utf-8")
        except OSError as erro:
            return False, f"nao foi possivel gravar o cartao: {erro}"

    alvo["status"] = "aprovada"
    alvo["aprovada_em"] = _agora()
    _gravar_aprovacoes(raiz, {"gerado_em": _agora(), "propostas": propostas})
    return True, f"proposta {proposta_id} aplicada em {cartao.name}"


def rejeitar(raiz: Path, proposta_id: str, motivo: str = "") -> tuple[bool, str]:
    dados = _carregar_aprovacoes(raiz)
    propostas = list(dados.get("propostas") or [])

    for proposta in propostas:
        if str(proposta.get("id") or "") != proposta_id:
            continue
        if proposta.get("status") != "pendente":
            return False, f"proposta {proposta_id!r} nao esta pendente"
        proposta["status"] = "rejeitada"
        proposta["rejeitada_em"] = _agora()
        proposta["motivo_rejeicao"] = motivo.strip()
        _gravar_aprovacoes(raiz, {"gerado_em": _agora(), "propostas": propostas})
        return True, f"proposta {proposta_id} rejeitada"
    return False, f"proposta {proposta_id!r} nao encontrada"


def editar(raiz: Path, proposta_id: str, novo_texto: str) -> tuple[bool, str]:
    texto = str(novo_texto or "").strip()
    if not texto:
        return False, "novo texto vazio"

    dados = _carregar_aprovacoes(raiz)
    propostas = list(dados.get("propostas") or [])
    for proposta in propostas:
        if str(proposta.get("id") or "") != proposta_id:
            continue
        if proposta.get("status") != "pendente":
            return False, f"proposta {proposta_id!r} nao esta pendente"
        proposta["texto"] = texto
        proposta["editada_em"] = _agora()
        _gravar_aprovacoes(raiz, {"gerado_em": _agora(), "propostas": propostas})
        return True, f"proposta {proposta_id} editada"
    return False, f"proposta {proposta_id!r} nao encontrada"
