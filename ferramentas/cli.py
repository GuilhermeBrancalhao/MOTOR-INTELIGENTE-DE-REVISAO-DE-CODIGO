"""Interface de linha de comando do ENGINE, usada pela skill /engine.

A raiz do projeto hospedeiro vem de ENGINE_RAIZ quando definida; senão, do diretório
corrente. Isso mantém a CLI testável sem depender de onde ela é executada.

Nenhum verbo pode terminar em traceback: erro de uso ou de estado sai com mensagem
legível e código 1. `principal` tem uma rede de segurança final para qualquer exceção
que os `except` específicos não previrem — melhor uma mensagem genérica do que um
stack trace no terminal do usuário.

Roda das DUAS formas, de propósito:

    py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" status   # script, de qualquer lugar
    python -m ferramentas.cli status                       # módulo, da raiz do plugin

A forma de script é a que a skill usa, porque o diretório corrente é sempre o do
projeto hospedeiro — e ali `python -m ferramentas.cli` dá `ModuleNotFoundError`, já
que o pacote `ferramentas` não está no `sys.path`. Executado como script, o Python
põe `ferramentas/` no `sys.path` (não a raiz do plugin), então `from ferramentas
import estado` também falharia: por isso a inserção explícita da raiz abaixo, feita
só quando não há pacote (`__package__` vazio), isto é, só no caminho de script.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

if not __package__:  # executado como script: a raiz do plugin não está no sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import config, detectar, estado, relatorio, trilha  # noqa: E402

USO = (
    'uso: py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" '
    "{ligar <objetivo> [--forcar] [--dry]|desligar|status|fase <DESTINO>|"
    "retomar|relatorio [ciclo|fase <FASE>]}"
)


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
        f"**Cartões detectados:** {', '.join(dados.get('cartoes') or []) or '(nenhum)'}",
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
    dry = "--dry" in resto
    objetivo = " ".join(
        palavra for palavra in resto if palavra not in ("--forcar", "--dry")
    ).strip()
    if not objetivo:
        print("ENGINE: 'ligar' exige o objetivo do ciclo em uma frase.")
        return 1
    modo = "dry" if dry else "normal"
    try:
        dados = estado.novo_ciclo(raiz, objetivo, _agora(), modo=modo, forcar=forcar)
    except estado.CicloJaAtivo as erro:
        print(f"ENGINE: {erro}")
        return 1
    dados["cartoes"] = _detectar_cartoes(raiz)
    estado.gravar(raiz, dados)
    print(_relatar(dados))
    return 0


def _detectar_cartoes(raiz: Path) -> list[str]:
    """Detecta as tecnologias do projeto hospedeiro para gravar em `estado.cartoes`.

    A detecção é acessória a `ligar`: uma falha nela (cartão malformado fora do
    contrato, projeto ilegível) não pode impedir a abertura do ciclo — avisa e
    segue com lista vazia.
    """
    try:
        return detectar.cartoes_do_projeto(raiz, config.raiz_plugin())
    except Exception as erro:  # noqa: BLE001 — detecção nunca pode derrubar 'ligar'
        print(
            f"ENGINE: aviso — detecção de cartões falhou "
            f"({erro.__class__.__name__}): {erro}"
        )
        return []


def _verbo_desligar(raiz: Path) -> int:
    """Desliga o ciclo — e não CRIA estado num projeto que nunca teve ciclo.

    Antes, `desligar` num projeto alheio gravava `.engine/estado.json` com
    `{"ativo": false}`, e a partir dali `status` imprimia o relatório verboso para
    sempre naquele projeto. Sem estado em disco não há o que desligar: imprime a
    mesma linha limpa que `status` usa nesse caso e sai 0 sem gravar nada.

    (A guarda `if not dados` que existia depois de `estado.desligar` era código morto:
    `desligar` sempre devolve um dicionário com `ativo`, nunca um vazio.)
    """
    if not estado.caminho(raiz).is_file():
        print(_relatar_desligado())
        return 0
    print(_relatar(estado.desligar(raiz)))
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


def _relatar_retomada(raiz: Path, dados: dict) -> str:
    """Resumo de reentrada para uma sessão nova sobre um ciclo já existente.

    Diferente de `_relatar` (usado por ligar/desligar/status/fase, que é o retrato
    do estado), este é pensado para orientar quem está chegando agora: além de
    fase/objetivo/modo/decisões, traz as últimas 5 ações da trilha — o que
    aconteceu de concreto antes da compactação ou do fim da sessão anterior.
    """
    ciclo = dados.get("ciclo", {})
    linhas = [
        "# Retomada de ciclo",
        "",
        f"**Fase:** {dados.get('fase', '?')}",
        f"**Objetivo:** {ciclo.get('objetivo', '(nenhum)')}",
        f"**Modo:** {ciclo.get('modo', 'normal')}",
        "",
        "## Decisões",
        "",
    ]
    decisoes = dados.get("decisoes") or []
    if not decisoes:
        linhas.append("(nenhuma decisão registrada)")
    else:
        for item in decisoes:
            if not isinstance(item, dict):
                continue
            linhas.append(f"- {item.get('o_que', '?')} — {item.get('porque', '?')}")

    linhas += ["", "## Últimas ações", ""]
    dados_trilha = trilha.ler(raiz)
    ultimas = (dados_trilha.get("linhas") or [])[-5:]
    if not ultimas:
        linhas.append("(nenhuma ação registrada na trilha)")
    else:
        for item in ultimas:
            if not isinstance(item, dict):
                continue
            # `trilha.redigir` aqui é defesa em profundidade: `trilha.registrar` já
            # redige antes de gravar, mas uma trilha escrita antes dessa correção
            # ainda tem credencial em claro no arquivo — e é esta impressão que
            # levaria o texto de volta para o contexto do modelo.
            alvo = trilha.redigir(str(item.get("alvo", "?")))
            linhas.append(
                f"- {item.get('quando', '?')} · {item.get('ferramenta', '?')} · "
                f"{alvo} · {item.get('risco', '?')}"
            )

    linhas += ["", "## Diffs por apresentar", ""]
    diffs = dados.get("diffs_pendentes") or []
    if diffs:
        linhas += [f"- {item}" for item in diffs]
    else:
        linhas.append("(nenhum diff pendente)")

    linhas += ["", "## Pendências abertas", ""]
    pendencias = dados.get("pendencias") or []
    if pendencias:
        linhas += [f"- {item}" for item in pendencias]
    else:
        linhas.append("(nenhuma pendência aberta)")

    return "\n".join(linhas)


def _verbo_retomar(raiz: Path) -> int:
    try:
        dados = estado.carregar_estrito(raiz)
    except estado.EstadoCorrompido as erro:
        print(f"ENGINE: {erro}")
        return 1
    if not dados:
        print("ENGINE: nenhum ciclo neste projeto; use 'ligar' para começar um.")
        return 1
    print(_relatar_retomada(raiz, dados))
    return 0


def _verbo_relatorio(raiz: Path, resto: list[str]) -> int:
    if not resto or resto[0] == "ciclo":
        print(relatorio.de_ciclo(raiz))
        return 0
    if resto[0] == "fase":
        fase = resto[1] if len(resto) > 1 else None
        print(relatorio.de_fase(raiz, fase))
        return 0
    print(USO)
    return 1


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
        if verbo == "retomar":
            return _verbo_retomar(raiz)
        if verbo == "relatorio":
            return _verbo_relatorio(raiz, resto)
        print(USO)
        return 1
    except Exception as erro:  # rede de segurança: nenhum verbo termina em traceback
        print(f"ENGINE: erro inesperado ({erro.__class__.__name__}): {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
