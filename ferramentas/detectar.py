"""Detecção de stack tecnológica do ENGINE.

Lê o `detectar:` do front-matter de cada cartão em `cartoes/` e varre o projeto
hospedeiro para decidir quais tecnologias estão presentes.

**Parser próprio, sem PyYAML.** O front-matter dos cartões é um subconjunto restrito
de YAML: quatro chaves fixas (`tecnologia`, `detectar`, `papeis`, `versao`), cada uma
numa única linha, e as duas listas sempre na forma `["a", "b"]` ou `[a, b]` — nunca o
estilo bloco (`- item` numa linha própria). Esse subconjunto é simples o bastante para
não precisar de dependência externa (biblioteca padrão apenas, igual ao resto do
projeto) e rígido o bastante para dar erro claro (`CartaoInvalido`) em vez de aceitar
silenciosamente algo fora do contrato.

**Casamento de padrão dual.** Um padrão com `/` (como `tests/**/test_*.py`) é casado
contra o caminho relativo INTEIRO do arquivo; um padrão sem `/` (como `pyproject.toml`
ou `*.py`) é casado só contra o NOME do arquivo, em qualquer profundidade — do
contrário `pyproject.toml` só bateria na raiz do projeto hospedeiro, e a maioria dos
cartões (que descreve arquivo de configuração por nome, não por caminho completo)
nunca casaria fora dela. `fnmatch` já trata `*` como "qualquer coisa, inclusive `/`",
então `**/*.py` funciona sem tratamento especial de duplo-asterisco: dois `*`
consecutivos viram só uma forma redundante do mesmo `.*` no regex traduzido.

**Padrão inválido nunca derruba a varredura.** `fnmatch` é tolerante à maior parte de
entrada malformada, mas a chamada fica em `try/except` mesmo assim — um cartão com um
padrão quebrado não pode impedir a detecção dos outros.
"""
from __future__ import annotations

import os
from fnmatch import fnmatch
from pathlib import Path

#: As quatro chaves do contrato do front-matter. Todas são obrigatórias.
_CHAVES_OBRIGATORIAS = ("tecnologia", "detectar", "papeis", "versao")

#: Chaves cujo valor é sempre lista (`[...]`), nunca string solta.
_CHAVES_LISTA = ("detectar", "papeis")

#: Diretórios em que a varredura nunca entra, custe o que custar.
_DIRETORIOS_IGNORADOS = {".git", "node_modules", "__pycache__", ".venv", ".engine"}

#: Quantos níveis de subdiretório a varredura desce a partir da raiz do projeto.
_PROFUNDIDADE_MAXIMA = 6


class CartaoInvalido(Exception):
    """O cartão não tem front-matter, o front-matter não fecha, ou falta chave
    obrigatória (`tecnologia`, `detectar`, `papeis` ou `versao`)."""


def ler_cartao(caminho: Path) -> dict:
    """Parseia o front-matter restrito de um cartão e devolve as quatro chaves.

    `detectar` e `papeis` viram `list[str]`; `tecnologia` e `versao` viram `str`.
    Levanta `CartaoInvalido` se o arquivo não começa com `---`, se o front-matter
    nunca fecha, ou se falta alguma das quatro chaves.
    """
    caminho = Path(caminho)
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    if not linhas or linhas[0].strip() != "---":
        raise CartaoInvalido(f"{caminho}: sem front-matter (o arquivo não começa com '---')")

    fim = None
    for indice in range(1, len(linhas)):
        if linhas[indice].strip() == "---":
            fim = indice
            break
    if fim is None:
        raise CartaoInvalido(f"{caminho}: front-matter nunca fecha (falta o '---' final)")

    campos: dict = {}
    for linha in linhas[1:fim]:
        bruta = linha.strip()
        if not bruta or ":" not in bruta:
            continue
        chave, _, valor = bruta.partition(":")
        chave = chave.strip()
        valor = valor.strip()
        if chave not in _CHAVES_OBRIGATORIAS:
            continue
        if chave in _CHAVES_LISTA:
            campos[chave] = _parsear_lista(valor, caminho, chave)
        else:
            campos[chave] = _tirar_aspas(valor)

    faltando = [chave for chave in _CHAVES_OBRIGATORIAS if chave not in campos]
    if faltando:
        raise CartaoInvalido(
            f"{caminho}: campo(s) obrigatório(s) ausente(s) no front-matter: {faltando}"
        )
    return campos


def _tirar_aspas(valor: str) -> str:
    if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in ("'", '"'):
        return valor[1:-1]
    return valor


def _parsear_lista(valor: str, caminho: Path, chave: str) -> list[str]:
    """Parseia `["a", "b"]` ou `[a, b]`, numa linha só.

    Varredura caractere a caractere (não `split(",")` direto) porque um item entre
    aspas pode não ter vírgula dentro, mas a vírgula entre dois itens não pode ser
    confundida com uma dentro de aspas — nenhum dos padrões reais tem isso hoje, mas
    o parser não pode depender de sorte.
    """
    if not valor.startswith("[") or not valor.endswith("]"):
        raise CartaoInvalido(f"{caminho}: {chave!r} não está na forma [a, b]: {valor!r}")
    interior = valor[1:-1]
    itens: list[str] = []
    atual: list[str] = []
    aspas: str | None = None
    for ch in interior:
        if aspas:
            if ch == aspas:
                aspas = None
            else:
                atual.append(ch)
            continue
        if ch in ("'", '"'):
            aspas = ch
            continue
        if ch == ",":
            item = "".join(atual).strip()
            if item:
                itens.append(item)
            atual = []
            continue
        atual.append(ch)
    ultimo = "".join(atual).strip()
    if ultimo:
        itens.append(ultimo)
    return itens


def cartoes_do_projeto(raiz_projeto: Path, raiz_plugin: Path) -> list[str]:
    """Devolve, ordenada e sem duplicata, a lista de tecnologias detectadas.

    Lê todos os `cartoes/*.md` de `raiz_plugin` (ignorando os que começam com `_`,
    como `_catalogo.md`, que é documentação e não um cartão) e casa o `detectar` de
    cada um contra os arquivos de `raiz_projeto`. Um cartão malformado é ignorado
    (não interrompe a detecção dos demais) — a validação de que os cartões reais do
    plugin estão todos bem formados é responsabilidade de `ler_cartao` e do teste que
    varre `cartoes/` diretamente, não desta função.
    """
    raiz_projeto = Path(raiz_projeto)
    diretorio_cartoes = Path(raiz_plugin) / "cartoes"
    if not diretorio_cartoes.is_dir():
        return []

    caminhos_relativos = list(_caminhos_relativos(raiz_projeto))

    detectadas: set[str] = set()
    for caminho_cartao in sorted(diretorio_cartoes.glob("*.md")):
        if caminho_cartao.name.startswith("_"):
            continue
        try:
            cartao = ler_cartao(caminho_cartao)
        except CartaoInvalido:
            continue
        padroes = cartao["detectar"]
        if any(
            _casa(relativo, padrao) for relativo in caminhos_relativos for padrao in padroes
        ):
            detectadas.add(cartao["tecnologia"])
    return sorted(detectadas)


def _caminhos_relativos(raiz_projeto: Path):
    """Gera o caminho relativo de todo arquivo sob `raiz_projeto`, respeitando o
    limite de profundidade e os diretórios ignorados."""
    for atual, subdiretorios, arquivos in os.walk(raiz_projeto):
        atual_path = Path(atual)
        profundidade = len(atual_path.relative_to(raiz_projeto).parts)
        subdiretorios[:] = [
            nome
            for nome in subdiretorios
            if nome not in _DIRETORIOS_IGNORADOS and profundidade < _PROFUNDIDADE_MAXIMA
        ]
        for nome_arquivo in arquivos:
            yield (atual_path / nome_arquivo).relative_to(raiz_projeto)


def _casa(relativo: Path, padrao: str) -> bool:
    try:
        if "/" in padrao:
            return fnmatch(relativo.as_posix(), padrao)
        return fnmatch(relativo.name, padrao)
    except Exception:  # noqa: BLE001 — padrão inválido não pode derrubar a varredura
        return False
