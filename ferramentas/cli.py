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

import json
import os
import sys
from datetime import datetime
from pathlib import Path

if not __package__:  # executado como script: a raiz do plugin não está no sys.path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import config, detectar, estado, programa, relatorio, trilha  # noqa: E402

USO = (
    'uso: py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" '
    "{ligar <objetivo> [--forcar] [--dry]|desligar|status|fase <DESTINO>|"
    "retomar|relatorio [ciclo|fase <FASE>]|programa <subverbo>}"
)

USO_PROGRAMA = (
    'uso: py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" programa '
    "{<objetivo> [--forcar]|plano <arquivo.json>|status|aprovar|proximo|"
    "aceite <CICLO> {ok|falhou}|"
    "reabrir <CICLO>|desviar <MOTIVO> <detalhe>|retomar|sistema {ok|falhou}|"
    "relatorio|abortar}"
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
    except estado.EstadoOcupado as erro:
        print(f"ENGINE: {erro}")
        return 1

    cartoes = _detectar_cartoes(raiz)

    # Segunda mutação, e por isso sob cadeado próprio: entre `novo_ciclo` e aqui a
    # detecção de cartões roda (varre o projeto, pode demorar), e nesse intervalo
    # outra sessão pode ter tocado o estado. Gravar o `dados` que voltou de
    # `novo_ciclo` apagaria o que ela escreveu.
    def _gravar_cartoes(atual: dict | None) -> dict | None:
        if atual is None:
            return None
        atual["cartoes"] = cartoes
        return atual

    try:
        dados = estado.atualizar(raiz, _gravar_cartoes) or dados
    except estado.EstadoOcupado as erro:
        print(f"ENGINE: aviso — cartões não gravados ({erro})")
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
    try:
        print(_relatar(estado.desligar(raiz)))
    except estado.EstadoOcupado as erro:
        print(f"ENGINE: {erro}")
        return 1
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
    """Transição de fase — a mutação que mais doía perder.

    Antes, `carregar_estrito` … `transicionar` … `gravar` eram três passos soltos:
    outra sessão que gravasse no meio via a sua escrita apagada, e o usuário desta
    sessão já tinha visto a transição confirmada na tela. Agora a leitura e a
    gravação acontecem dentro do mesmo cadeado, e `transicionar` valida o grafo
    contra a fase que está no disco AGORA, não contra a que se leu antes.
    """
    if not resto:
        print(USO)
        return 1
    destino = resto[0].upper()
    falha: list[str] = []

    def _mutar(dados: dict | None) -> dict | None:
        if not dados:
            falha.append("ENGINE: desligado; não há fase para mudar.")
            return None
        return estado.transicionar(dados, destino)

    try:
        dados = estado.atualizar(raiz, _mutar)
    except estado.EstadoCorrompido as erro:
        print(f"ENGINE: {erro}")
        return 1
    except estado.TransicaoInvalida as erro:
        print(f"ENGINE: {erro}")
        return 1
    except estado.EstadoOcupado as erro:
        print(f"ENGINE: {erro}")
        return 1
    if dados is None:
        print(falha[0])
        return 1
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


def _prog_trilha(raiz: Path, acao: str, alvo: str, agora: str) -> None:
    """Registra um passo do programa na trilha, marcado como `do_motor`.

    A marca é obrigatória aqui pelo mesmo motivo que existe no ciclo: sem ela, o
    gate leria como evidência do trabalho uma linha que o próprio motor acabou de
    escrever — foi exatamente esse o defeito encontrado na revisão de 2026-07-31.
    """
    trilha.registrar(
        raiz,
        {
            "quando": agora,
            "fase": "PROGRAMA",
            "ferramenta": "cli.py",
            "alvo": f"{acao} {alvo}".strip(),
            "risco": "rastreado",
            "regra": "",
            "do_motor": True,
        },
    )


def _prog_carregar(raiz: Path) -> dict | None:
    """Lê o programa e reclama em vez de estourar quando não existe."""
    try:
        return programa.carregar_estrito(raiz)
    except programa.ProgramaCorrompido as erro:
        print(f"ENGINE: {erro}")
        return None


def _prog_exigir(raiz: Path) -> dict | None:
    dados = _prog_carregar(raiz)
    if dados is None:
        print("ENGINE: nenhum programa neste projeto. Use `programa <objetivo>` primeiro.")
    return dados


def _prog_imprimir(dados: dict) -> None:
    r = programa.resumo(dados)
    print(f"**PROGRAMA:** {r['programa']}  ·  **Estado:** {r['estado']}")
    print(f"**Objetivo:** {r['objetivo']}")
    print(f"**Ciclos:** {r['concluidos']}/{r['total']} concluídos")
    for c in dados["ciclos"]:
        marca = {
            "CONCLUIDO": "[x]",
            "ATIVO": "[>]",
            "REPROVADO": "[!]",
            "PENDENTE": "[ ]",
        }.get(c["status"], "[?]")
        deps = f"  (depende de {', '.join(c['depende_de'])})" if c["depende_de"] else ""
        print(f"  {marca} {c['id']}: {c['objetivo']}{deps}")
    if r["desvio"]:
        print(f"**DESVIO:** {r['desvio']['motivo']} — {r['desvio']['detalhe']}")
    if dados["estado"] == "PLANO_MESTRE":
        print(
            "\n**Porta do plano-mestre.** Nada executa até o usuário rodar "
            "`programa aprovar`."
        )
    elif r["proximo"]:
        print(f"**Próximo ciclo elegível:** {r['proximo']}")


def _verbo_programa(raiz: Path, resto: list[str]) -> int:
    """Verbos da camada de PROGRAMA (Fase 4).

    `aprovar` é o único verbo do motor que o modelo não pode executar por conta
    própria: é a porta P1 materializada. A skill declara essa regra; aqui a CLI
    apenas a torna um passo explícito e auditável na trilha.
    """
    if not resto:
        print(USO_PROGRAMA)
        return 1

    sub, *args = resto
    agora = _agora()

    if sub == "status":
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        _prog_imprimir(dados)
        return 0

    if sub == "plano":
        # A decomposição vem de um JSON em arquivo, não da linha de comando: um
        # plano de 20 ciclos com objetivos e critérios de aceite não cabe em
        # argumentos, e passá-lo como string escapada seria frágil justamente onde
        # o conteúdo importa mais.
        if not args:
            print(
                "ENGINE: `programa plano <arquivo.json>` — o arquivo deve ter "
                '{"aceite_de_sistema": "...", "ciclos": [{"id","objetivo",'
                '"depende_de","aceite"}]}'
            )
            return 1
        origem = Path(args[0])
        if not origem.is_file():
            print(f"ENGINE: arquivo de plano não encontrado: {origem}")
            return 1
        try:
            bruto = json.loads(origem.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError, OSError) as erro:
            print(f"ENGINE: plano ilegível ({origem}): {erro}")
            return 1
        if not isinstance(bruto, dict):
            print("ENGINE: o plano deve ser um objeto JSON")
            return 1
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        try:
            novo = programa.propor_plano(
                dados,
                bruto.get("ciclos") or [],
                bruto.get("aceite_de_sistema", ""),
            )
        except (programa.PlanoInvalido, programa.TransicaoInvalida) as erro:
            print(f"ENGINE: {erro}")
            return 1
        programa.gravar(raiz, novo)
        _prog_trilha(raiz, "plano-mestre-proposto", novo["programa"], agora)
        print("**Plano-mestre registrado e validado** (DAG e critérios de aceite).")
        _prog_imprimir(novo)
        return 0

    if sub == "aprovar":
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        try:
            novo = programa.aprovar(dados, agora)
        except programa.TransicaoInvalida as erro:
            print(f"ENGINE: {erro}")
            return 1
        programa.gravar(raiz, novo)
        _prog_trilha(raiz, "programa-aprovado", novo["programa"], agora)
        print("**Plano-mestre aprovado.** O programa entra em EXECUCAO.")
        _prog_imprimir(novo)
        return 0

    if sub == "proximo":
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        if dados["estado"] != "EXECUCAO":
            print(
                f"ENGINE: o programa está em {dados['estado']}; ciclos só ligam em "
                "EXECUCAO (o plano-mestre precisa ter sido aprovado)"
            )
            return 1
        alvo = programa.proximo_elegivel(dados)
        if alvo is None:
            if programa.pronto_para_aceite(dados):
                print("Todos os ciclos concluídos. Rode `programa sistema {ok|falhou}`.")
                return 0
            print(
                "ENGINE: nenhum ciclo elegível. Há ciclo REPROVADO bloqueando "
                "dependentes — use `programa reabrir <CICLO>`."
            )
            return 1
        print(f"**Próximo ciclo:** {alvo['id']} — {alvo['objetivo']}")
        print(f"**Aceite:** {alvo['aceite']}")
        return 0

    if sub == "aceite":
        if len(args) < 2 or args[1] not in ("ok", "falhou"):
            print(USO_PROGRAMA)
            return 1
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        try:
            novo = programa.registrar_aceite(dados, args[0], passou=args[1] == "ok")
        except KeyError as erro:
            print(f"ENGINE: {erro}")
            return 1
        programa.gravar(raiz, novo)
        _prog_trilha(raiz, f"aceite-de-ciclo-{args[1]}", args[0], agora)
        _prog_imprimir(novo)
        return 0

    if sub == "reabrir":
        if not args:
            print(USO_PROGRAMA)
            return 1
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        try:
            novo = programa.reabrir(dados, args[0])
        except (KeyError, programa.TransicaoInvalida) as erro:
            print(f"ENGINE: {erro}")
            return 1
        programa.gravar(raiz, novo)
        _prog_imprimir(novo)
        return 0

    if sub == "desviar":
        if len(args) < 2:
            print(
                "ENGINE: motivos válidos: " + ", ".join(programa.MOTIVOS_DESVIO)
            )
            return 1
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        try:
            novo = programa.desviar(dados, args[0], " ".join(args[1:]))
        except (programa.DesvioInvalido, programa.TransicaoInvalida) as erro:
            print(f"ENGINE: {erro}")
            return 1
        programa.gravar(raiz, novo)
        print("**Execução parada por desvio.** Apresente o conflito ao usuário.")
        _prog_imprimir(novo)
        return 0

    if sub == "retomar":
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        if dados["estado"] == "DESVIO":
            try:
                dados = programa.retomar_apos_desvio(dados)
            except programa.TransicaoInvalida as erro:
                print(f"ENGINE: {erro}")
                return 1
            programa.gravar(raiz, dados)
        _prog_imprimir(dados)
        return 0

    if sub == "sistema":
        if not args or args[0] not in ("ok", "falhou"):
            print(USO_PROGRAMA)
            return 1
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        try:
            if dados["estado"] == "EXECUCAO":
                dados = programa.entrar_em_aceite(dados)
            novo = programa.concluir(dados, passou=args[0] == "ok", agora=agora)
        except programa.TransicaoInvalida as erro:
            print(f"ENGINE: {erro}")
            return 1
        programa.gravar(raiz, novo)
        _prog_trilha(raiz, f"aceite-de-sistema-{args[0]}", novo["programa"], agora)
        if novo["estado"] == "CONCLUIDO":
            print("**PROGRAMA CONCLUÍDO.** Aceite de sistema verde.")
        else:
            print(
                "**Aceite de sistema REPROVOU.** O programa volta a EXECUCAO — "
                "nada é dado como concluído."
            )
        _prog_imprimir(novo)
        return 0

    if sub == "relatorio":
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        _prog_imprimir(dados)
        print(f"\n**Aceite de sistema declarado:** {dados['aceite_de_sistema']}")
        return 0

    if sub == "abortar":
        dados = _prog_exigir(raiz)
        if dados is None:
            return 1
        novo = dict(dados)
        novo["estado"] = "CONCLUIDO"
        novo["abortado_em"] = agora
        programa.gravar(raiz, novo)
        print("Programa abortado. A trilha e a decomposição ficam preservadas.")
        return 0

    # Sem subverbo reservado: o resto é o objetivo de um programa novo.
    forcar = "--forcar" in resto
    objetivo = " ".join(a for a in resto if a != "--forcar").strip()
    if not objetivo:
        print(USO_PROGRAMA)
        return 1
    try:
        dados = programa.novo(raiz, objetivo, agora, forcar=forcar)
    except (programa.ProgramaJaAtivo, programa.ProgramaCorrompido) as erro:
        print(f"ENGINE: {erro}")
        return 1
    _prog_trilha(raiz, "programa-aberto", objetivo, agora)
    print(f"**PROGRAMA aberto:** {dados['programa']}  ·  **Estado:** CONCEPCAO")
    print(f"**Objetivo:** {objetivo}")
    print(
        "\nConduza a macro-DESCOBERTA e o PLANO_MESTRE. A decomposição precisa de "
        "um critério de aceite falsificável por ciclo, e de um aceite de sistema."
    )
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
        if verbo == "retomar":
            return _verbo_retomar(raiz)
        if verbo == "relatorio":
            return _verbo_relatorio(raiz, resto)
        if verbo == "programa":
            return _verbo_programa(raiz, resto)
        print(USO)
        return 1
    except Exception as erro:  # rede de segurança: nenhum verbo termina em traceback
        print(f"ENGINE: erro inesperado ({erro.__class__.__name__}): {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
