"""Valida os metadados dos volumes (`_VOLUME.yml`) sob `volumes/prontos/`.

Cada `_VOLUME.yml` deste repositório promete, no próprio comentário, ser lido por
este módulo e por `status.py`. Atenção: esse `status.py` é o da plataforma
(`acervo/ferramentas/status.py`), que opera sobre a FONTE em `acervo/NN-NOME/`;
não existe `ferramentas/status.py` no lado do motor. São dois pacotes homônimos
e separados de propósito (ver `pytest.ini`). A checagem central é
`depende-de-inexistente`: um volume não pode declarar `depende_de` apontando para
um número que não existe como diretório em `volumes/prontos/` — isso criaria um
pré-requisito de leitura que não pode ser lido, e é exatamente o cenário que os
comentários dos `_VOLUME.yml` reais descrevem como razão de manterem `depende_de`
vazio.

Sem dependência de PyYAML: o plugin não a declara, e o formato real (pares
`chave: valor` de uma linha, sem mapas/listas aninhadas — só uma lista inline
para `depende_de`) não precisa de um parser completo.
"""
from __future__ import annotations

import sys
from pathlib import Path

#: Campos que todo `_VOLUME.yml` real declara (ver os três volumes existentes em
#: `volumes/prontos/`). Ausência de qualquer um é violação, não aviso — sem eles
#: o volume não é identificável nem verificável.
CAMPOS_OBRIGATORIOS = ("volume", "nome", "tipo", "status", "perecivel", "depende_de")


def ler_metadados(caminho: Path) -> dict:
    """Lê `_VOLUME.yml`: pares `chave: valor` de uma linha, comentários com `#`,
    e uma lista inline para `depende_de` (`[]` ou `["07", "12"]`).

    Um arquivo ilegível (permissão negada, encoding inválido) vira
    `_erro_leitura` em vez de subir a exceção — `validar` transforma isso numa
    violação relatada, em vez do processo quebrar com traceback no meio do que é,
    justamente, a ferramenta que existe para reportar volume com problema.
    """
    metadados: dict = {}
    if not caminho.exists():
        return metadados
    try:
        conteudo = caminho.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as erro:
        return {"_erro_leitura": f"{erro.__class__.__name__}: {erro}"}
    for linha in conteudo.split("\n"):
        linha = linha.strip()
        if not linha or linha.startswith("#") or ":" not in linha:
            continue
        chave, _, valor = linha.partition(":")
        chave = chave.strip()
        valor = valor.strip()
        if chave == "depende_de":
            interior = valor.strip("[]").strip()
            metadados[chave] = (
                [item.strip().strip('"').strip("'") for item in interior.split(",")]
                if interior
                else []
            )
        elif valor:
            metadados[chave] = valor.strip('"').strip("'")
    return metadados


def descobrir_volumes(raiz_volumes: Path) -> dict[str, dict]:
    """Descobre volumes em `raiz_volumes` (ex.: `volumes/prontos/`), indexados
    pelo campo `volume` — o número (ex.: `"07"`), não o nome do diretório, porque
    é esse número que `depende_de` referencia."""
    volumes: dict[str, dict] = {}
    if not raiz_volumes.exists():
        return volumes
    for item in sorted(raiz_volumes.iterdir()):
        if not item.is_dir():
            continue
        metadados = ler_metadados(item / "_VOLUME.yml")
        if not metadados:
            continue
        metadados["_diretorio"] = item.name
        numero = metadados.get("volume") or f"_ilegivel:{item.name}"
        volumes[numero] = metadados
    return volumes


def validar(raiz_volumes: Path) -> list[str]:
    """Valida todos os volumes descobertos em `raiz_volumes`.

    Devolve a lista de violações — vazia significa validação limpa. Um diretório
    sem `_VOLUME.yml` é simplesmente ignorado, não é uma violação — a ausência do
    arquivo é o caso comum (diretório que não segue essa convenção). Um
    `_VOLUME.yml` que existe mas está ilegível ou incompleto, isso sim, é violação.
    """
    volumes = descobrir_volumes(raiz_volumes)
    violacoes: list[str] = []

    for metadados in volumes.values():
        diretorio = metadados["_diretorio"]
        if "_erro_leitura" in metadados:
            violacoes.append(f"{diretorio}: _VOLUME.yml ilegível ({metadados['_erro_leitura']})")
            continue
        for campo in CAMPOS_OBRIGATORIOS:
            if campo not in metadados:
                violacoes.append(
                    f"{diretorio}: campo obrigatório '{campo}' ausente em _VOLUME.yml"
                )

        for dependencia in metadados.get("depende_de", []):
            if dependencia not in volumes:
                violacoes.append(
                    f"{diretorio}: depende-de-inexistente — depende_de aponta para "
                    f"o volume '{dependencia}', que não existe em {raiz_volumes}"
                )

    return violacoes


def _forcar_utf8() -> None:
    """Reconfigura stdout para UTF-8 (mesma tática de `ferramentas/cli.py`).

    Sem isso, ✓/✗ saem como `UnicodeEncodeError` no console do Windows (cp1252
    por padrão) em vez de imprimir o relatório.
    """
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass


def principal(argumentos: list[str]) -> int:
    _forcar_utf8()
    raiz_volumes = (
        Path(argumentos[0]) if argumentos else Path.cwd() / "volumes" / "prontos"
    )
    violacoes = validar(raiz_volumes)
    if not violacoes:
        print(f"✓ {raiz_volumes}: nenhuma violação encontrada")
        return 0
    print(f"✗ {raiz_volumes}: {len(violacoes)} violação(ões)")
    for violacao in violacoes:
        print(f"  - {violacao}")
    return 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
