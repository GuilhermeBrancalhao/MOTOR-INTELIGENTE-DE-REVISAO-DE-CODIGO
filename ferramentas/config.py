"""Configuração do ENGINE.

Ordem de precedência, da mais fraca para a mais forte:
PADRAO -> <plugin>/engine.config.json -> <projeto>/.engine/config.json

Arquivo malformado nunca derruba a sessão nem passa despercebido: cai no default
e registra um aviso em `_avisos`, que o hook de contexto mostra uma vez.

**A absorção é por LISTA BRANCA, não por `update`.** Antes, `cfg.update(dados)` copiava
qualquer chave do arquivo do hospedeiro para dentro da configuração efetiva — inclusive
`_avisos` (que sobrescrevia a lista interna e apagava a trilha de problemas) e
`padroes_segredo` (o único insumo da família R5, que um `[]` no arquivo desarmava
inteira). Agora: só chave presente em `PADRAO` pode ser sobreposta por arquivo, chave
desconhecida é ignorada com aviso, e `_avisos` nunca vem de arquivo.

`padroes_segredo` é o único caso especial: o valor do arquivo é **acrescentado** ao
default em vez de substituí-lo. Ampliar a lista de segredos por config é legítimo;
reduzi-la não pode ser possível, porque seria desarmar a proteção pelo lado de fora.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

PADRAO: dict = {
    "porta_plano": True,
    "teto_cartao_linhas": 40,
    # Chave privada, credencial de registro e token. `cat $HOME/.ssh/id_rsa` saía
    # LIVRE porque nenhum padrão cobria a família `id_*` do SSH — e o mesmo valia
    # para `.npmrc`/`.netrc`/`.pypirc` (senha de registro em texto puro) e para os
    # cofres de chave de assinatura (`*.jks`, `*.keystore`, `*.p8`, `*.ppk`).
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
        "id_rsa",
        "id_dsa",
        "id_ecdsa",
        "id_ed25519",
        "*.ppk",
        ".npmrc",
        ".netrc",
        ".pypirc",
        "*.p8",
        "*token*",
        "*.jks",
        "*.keystore",
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
            _aplicar(cfg, dados, caminho.name)
        else:
            cfg["_avisos"].append(f"{caminho.name} não é um objeto JSON; usando o default")
    return cfg


#: Chaves que só se ACRESCENTAM ao default; nunca o substituem. Ver o docstring do
#: módulo: reduzir a lista de segredos por arquivo é desarmar a família R5.
_SOMENTE_ACRESCENTA = ("padroes_segredo",)


def _aplicar(cfg: dict, dados: dict, nome: str) -> None:
    """Sobrepõe em `cfg` só as chaves da lista branca (as presentes em `PADRAO`)."""
    for chave, valor in dados.items():
        if chave not in PADRAO:
            cfg["_avisos"].append(
                f"{nome}: chave desconhecida {chave!r} ignorada (não está no contrato)"
            )
            continue
        if chave in _SOMENTE_ACRESCENTA:
            _acrescentar(cfg, chave, valor, nome)
            continue
        cfg[chave] = valor


def _acrescentar(cfg: dict, chave: str, valor, nome: str) -> None:
    if not isinstance(valor, list):
        cfg["_avisos"].append(
            f"{nome}: {chave!r} não é uma lista; mantendo só o default"
        )
        return
    for item in valor:
        if item not in cfg[chave]:
            cfg[chave].append(item)
