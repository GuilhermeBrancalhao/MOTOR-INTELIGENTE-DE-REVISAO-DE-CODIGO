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
import re
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
    """Sobrepõe em `cfg` só as chaves da lista branca (as presentes em `PADRAO`).

    Além da lista branca, duas chaves têm validação de FORMA na fusão — valor de
    tipo errado ou item malformado é descartado com aviso, nunca absorvido:

    - `teto_cartao_linhas` precisa ser inteiro (uma string, objeto ou booleano
      chegava cru ao hook de contexto e derrubava o cartão);
    - `travado_extra` precisa ser lista de objetos `{regra, motivo, padrao}` com
      `padrao` compilável — uma regex inválida chegava até `re.search` e o
      classificador falhava fechado (trava TUDO): não é brecha de segurança, mas
      inutiliza a sessão inteira a partir do `.engine/config.json` do projeto.
    """
    for chave, valor in dados.items():
        if chave not in PADRAO:
            cfg["_avisos"].append(
                f"{nome}: chave desconhecida {chave!r} ignorada (não está no contrato)"
            )
            continue
        if chave in _SOMENTE_ACRESCENTA:
            _acrescentar(cfg, chave, valor, nome)
            continue
        if chave == "teto_cartao_linhas":
            if not isinstance(valor, int) or isinstance(valor, bool):
                cfg["_avisos"].append(
                    f"{nome}: 'teto_cartao_linhas' precisa ser um número inteiro, "
                    f"veio {valor!r}; valor ignorado, mantendo {cfg[chave]}"
                )
                continue
            cfg[chave] = valor
            continue
        if chave == "travado_extra":
            cfg[chave] = _validar_travado_extra(valor, nome, cfg["_avisos"])
            continue
        cfg[chave] = valor


#: As três chaves obrigatórias de cada item de `travado_extra` — o formato que
#: `risco._familias` consome como `(item["regra"], item["motivo"], item["padrao"])`.
_CHAVES_TRAVADO_EXTRA = ("regra", "motivo", "padrao")


def _validar_travado_extra(valor, nome: str, avisos: list) -> list:
    """Valida a forma de `travado_extra`: devolve só os itens bem formados.

    Cada item precisa ser um dicionário com `regra`, `motivo` e `padrao` (todos
    texto) e `padrao` precisa compilar como regex. Item malformado é descartado
    com aviso dizendo o quê e por quê — sem derrubar os demais itens da lista.
    """
    if not isinstance(valor, list):
        avisos.append(
            f"{nome}: 'travado_extra' precisa ser uma lista, veio {type(valor).__name__}; "
            "valor ignorado"
        )
        return []
    validos: list = []
    for indice, item in enumerate(valor):
        problema = _problema_do_item_travado(item)
        if problema is not None:
            avisos.append(
                f"{nome}: item {indice} de 'travado_extra' ignorado ({problema})"
            )
            continue
        validos.append(item)
    return validos


def _problema_do_item_travado(item) -> str | None:
    """Descreve o defeito de um item de `travado_extra`, ou `None` se ele é válido."""
    if not isinstance(item, dict):
        return f"não é um objeto, é {type(item).__name__}"
    faltando = [chave for chave in _CHAVES_TRAVADO_EXTRA if chave not in item]
    if faltando:
        return f"faltam as chaves {faltando}"
    nao_texto = [chave for chave in _CHAVES_TRAVADO_EXTRA if not isinstance(item[chave], str)]
    if nao_texto:
        return f"as chaves {nao_texto} precisam ser texto"
    try:
        re.compile(item["padrao"])
    except re.error as erro:
        return f"'padrao' não é uma regex compilável: {erro}"
    return None


def _acrescentar(cfg: dict, chave: str, valor, nome: str) -> None:
    if not isinstance(valor, list):
        cfg["_avisos"].append(
            f"{nome}: {chave!r} não é uma lista; mantendo só o default"
        )
        return
    for item in valor:
        if item not in cfg[chave]:
            cfg[chave].append(item)
