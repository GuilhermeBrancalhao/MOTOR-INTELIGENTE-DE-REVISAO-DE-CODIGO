"""Interface de linha de comando do ENGINE, usada pela skill /engine.

A raiz do projeto hospedeiro vem de ENGINE_RAIZ quando definida; senão, do diretório
corrente. Isso mantém a CLI testável sem depender de onde ela é executada.

Nenhum verbo pode terminar em traceback: erro de uso ou de estado sai com mensagem
legível e código 1. `principal` tem uma rede de segurança final para qualquer exceção
que os `except` específicos não previrem — melhor uma mensagem genérica do que um
stack trace no terminal do usuário.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

from ferramentas import estado

USO = "uso: python -m ferramentas.cli {ligar <objetivo> [--forcar]|desligar|status|fase <DESTINO>}"


def _forcar_utf8() -> None:
    """Reconfigura stdout/stderr para UTF-8 (mesma tática de `hooks/_comum.py`).

    Sem isso, a acentuação que a CLI imprime sai como mojibake no console do
    Windows (cp1252 por padrão) — e essa mensagem é o que a skill lê para decidir
    o que reportar ao usuário.
    """
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def _raiz() -> Path:
    return Path(os.environ.get("ENGINE_RAIZ") or Path.cwd())


def _agora() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _relatar(dados: dict) -> str:
    ciclo = dados.get("ciclo", {})
    linhas = [
        f"**ENGINE:** {'ativo' if dados.get('ativo') else 'desligado'}",
        f"**Fase:** {dados.get('fase', '?')}  ·  **Modo:** {ciclo.get('modo', 'normal')}",
        f"**Objetivo:** {ciclo.get('objetivo', '(nenhum)')}",
        f"**Fases concluídas:** {', '.join(dados.get('fases_concluidas') or []) or '(nenhuma)'}",
        f"**Diffs por apresentar:** {len(dados.get('diffs_pendentes') or [])}",
        f"**Pendências:** {len(dados.get('pendencias') or [])}",
    ]
    for item in dados.get("decisoes") or []:
        linhas.append(f"- decisão: {item.get('o_que')} — {item.get('porque')}")
    return "\n".join(linhas)


def _relatar_desligado() -> str:
    return "**ENGINE:** desligado (nenhum ciclo neste projeto)."


def _verbo_ligar(raiz: Path, resto: list[str]) -> int:
    forcar = "--forcar" in resto
    objetivo = " ".join(palavra for palavra in resto if palavra != "--forcar").strip()
    if not objetivo:
        print("ENGINE: 'ligar' exige o objetivo do ciclo em uma frase.")
        return 1
    try:
        dados = estado.novo_ciclo(raiz, objetivo, _agora(), forcar=forcar)
    except estado.CicloJaAtivo as erro:
        print(f"ENGINE: {erro}")
        return 1
    print(_relatar(dados))
    return 0


def _verbo_desligar(raiz: Path) -> int:
    dados = estado.desligar(raiz)
    if not dados:
        print(_relatar_desligado())
        return 0
    print(_relatar(dados))
    return 0


def _verbo_status(raiz: Path) -> int:
    try:
        dados = estado.carregar_estrito(raiz)
    except estado.EstadoCorrompido as erro:
        print(f"ENGINE: {erro}")
        return 1
    if not dados:
        print(_relatar_desligado())
        return 0
    print(_relatar(dados))
    return 0


def _verbo_fase(raiz: Path, resto: list[str]) -> int:
    if not resto:
        print(USO)
        return 1
    try:
        dados = estado.carregar_estrito(raiz)
    except estado.EstadoCorrompido as erro:
        print(f"ENGINE: {erro}")
        return 1
    if not dados:
        print("ENGINE: desligado; não há fase para mudar.")
        return 1
    try:
        dados = estado.transicionar(dados, resto[0].upper())
    except estado.TransicaoInvalida as erro:
        print(f"ENGINE: {erro}")
        return 1
    estado.gravar(raiz, dados)
    print(_relatar(dados))
    return 0


def principal(argumentos: list[str]) -> int:
    _forcar_utf8()
    if not argumentos:
        print(USO)
        return 1
    verbo, *resto = argumentos
    raiz = _raiz()

    try:
        if verbo == "ligar":
            return _verbo_ligar(raiz, resto)
        if verbo == "desligar":
            return _verbo_desligar(raiz)
        if verbo == "status":
            return _verbo_status(raiz)
        if verbo == "fase":
            return _verbo_fase(raiz, resto)
        print(USO)
        return 1
    except Exception as erro:  # rede de segurança: nenhum verbo termina em traceback
        print(f"ENGINE: erro inesperado ({erro.__class__.__name__}): {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
