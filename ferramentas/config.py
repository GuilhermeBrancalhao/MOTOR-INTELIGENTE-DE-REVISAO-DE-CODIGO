"""Configuração do ENGINE.

Ordem de precedência, da mais fraca para a mais forte:
PADRAO -> <plugin>/engine.config.json -> <projeto>/.engine/config.json

Arquivo malformado nunca derruba a sessão nem passa despercebido: cai no default
e registra um aviso em `_avisos`, que o hook de contexto mostra uma vez.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

PADRAO: dict = {
    "porta_plano": True,
    "teto_cartao_linhas": 40,
    "padroes_segredo": [
        ".env",
        ".env.*",
        "*.pfx",
        "*.pem",
        "*.key",
        "*.p12",
        "credentials*",
        "*_secret*",
        "*secrets*",
    ],
    "travado_extra": [],
}


def raiz_plugin() -> Path:
    """Raiz do repositório do plugin (pai de `ferramentas/`)."""
    return Path(__file__).resolve().parent.parent


def carregar(raiz_projeto: Path) -> dict:
    """Devolve a configuração efetiva para um projeto hospedeiro."""
    cfg = copy.deepcopy(PADRAO)
    cfg["_avisos"] = []
    candidatos = (
        raiz_plugin() / "engine.config.json",
        Path(raiz_projeto) / ".engine" / "config.json",
    )
    for caminho in candidatos:
        if not caminho.is_file():
            continue
        try:
            dados = json.loads(caminho.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError, UnicodeDecodeError) as erro:
            cfg["_avisos"].append(
                f"{caminho.name} ilegível ({erro.__class__.__name__}); usando o default"
            )
            continue
        if isinstance(dados, dict):
            cfg.update(dados)
        else:
            cfg["_avisos"].append(f"{caminho.name} não é um objeto JSON; usando o default")
    return cfg
