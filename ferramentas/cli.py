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
    "retomar|relatorio [ciclo|fase <FASE>]|descoberta <subverbo>|programa <subverbo>}"
)

USO_DESCOBERTA = (
    'uso: py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" descoberta '
    "{<pedido> [--intencao <INTENCAO>] [--forcar]|status|responder <ID> <resposta>}"
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


def _texto_do_erro(erro: BaseException) -> str:
    """A mensagem da exceção, sem as aspas que `KeyError` acrescenta.

    `str(KeyError("faltou isto"))` devolve `"'faltou isto'"` — com as aspas dentro do
    texto, porque `KeyError.__str__` usa o `repr` do argumento. Metade das exceções do
    caminho da descoberta (`DescobertaAusente`, `LacunaDesconhecida`) herda de `KeyError`
    de propósito, e a mensagem delas é escrita para ser lida por gente: a aspa solta no
    meio da frase é o tipo de detalhe que faz parecer traceback vazado.
    """
    if erro.args and isinstance(erro.args[0], str):
        return erro.args[0]
    return str(erro)


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


#: A única aresta do grafo do CICLO com gate de CONTEÚDO, e não só de forma.
#: `transicionar` valida o desenho ("existe DESCOBERTA -> ANALISE?"); este par diz que,
#: além de existir, a passagem exige a entrevista de descoberta fechada. As outras
#: arestas seguem valendo só pelo grafo — acrescentar uma segunda linha aqui é uma
#: decisão de produto, não um ajuste de código.
ARESTA_COM_GATE_DE_DESCOBERTA = ("DESCOBERTA", "ANALISE")

#: A aresta gêmea, um andar acima: no grafo do PROGRAMA, `CONCEPCAO` é declarada pela
#: spec da Fase 4 como a **macro-DESCOBERTA** ("objetivo real do sistema, requisitos,
#: restrições, riscos. Papel `descobridor`"). Declarado por escrito e, até este ciclo,
#: nunca verificado: `propor_plano` transicionava exigindo só aceite de sistema e DAG
#: válido. O par abaixo é o que torna a declaração falsificável.
ARESTA_DO_PROGRAMA_COM_GATE = ("CONCEPCAO", "PLANO_MESTRE")


def _gate_descoberta(
    dados: dict | None,
    *,
    transicao: str = "DESCOBERTA -> ANALISE",
    antes_de: str = "mudar de fase",
) -> str | None:
    """A recusa de uma transição protegida pela descoberta, ou `None` para seguir.

    **Um só gate, duas arestas.** Serve tanto `DESCOBERTA -> ANALISE` (grafo do ciclo)
    quanto `CONCEPCAO -> PLANO_MESTRE` (grafo do programa, onde a CONCEPCAO é a
    macro-DESCOBERTA). São a mesma pergunta em escalas diferentes — "a entrevista está
    fechada?" — e por isso `transicao` e `antes_de` são só rótulos da mensagem: o
    predicado, a política de falha e o texto da recusa são um só. Uma segunda cópia
    divergiria no primeiro ajuste, e a divergência apareceria como um gate mais frouxo
    que o outro sem ninguém decidir isso.

    **Falha FECHADO.** Qualquer coisa que dê errado ao calcular o veredito — estado
    sem o bloco de descoberta, bloco de versão desconhecida, eixo fora da taxonomia,
    `ferramentas/descoberta.py` ausente numa instalação capenga, exceção que ninguém
    previu — devolve mensagem de recusa, nunca liberação. É o oposto deliberado de
    `hooks/engine_gate.py`, que engole erro e deixa o turno passar: aquele é rede
    secundária no evento Stop, e derrubar o turno do usuário por um defeito do motor
    seria pior do que deixar uma cobrança escapar. Este aqui é o caminho REAL da
    transição, e o custo do erro é invertido — liberar por engano deixa o plano ser
    escrito sobre suposição, que é exatamente o defeito que a elicitação existe para
    não ter. "Não sei" e "está livre" não são a mesma coisa.

    O `import` mora dentro da função, e dentro do `try`, pelo mesmo motivo: importado
    no topo, um `ferramentas/descoberta.py` quebrado estouraria na carga do módulo —
    antes de `principal` existir para segurar a exceção — e derrubaria a CLI inteira
    com traceback, inclusive `status` e `desligar`, que nada têm com este gate. Aqui
    dentro, o defeito fecha o portão e não contamina o resto.

    Recebe o estado já lido (nunca o caminho da pasta) porque quem chama está com o
    cadeado do estado na mão, e ler o disco de novo aqui tentaria retomar um cadeado
    que não é reentrante. `None` é aceito e vale como "não há estado nesta pasta" — que
    é ausência de descoberta, e portanto recusa.
    """
    try:
        from ferramentas import descoberta  # noqa: PLC0415 — ver docstring

        avaliacao = descoberta.avaliar(dados)
        if avaliacao.liberado_para_planejar:
            return None
        if not avaliacao.registrada:
            cabecalho = (
                f"ENGINE: transição {transicao} recusada — a descoberta não "
                "foi registrada neste ciclo."
            )
        else:
            cabecalho = (
                f"ENGINE: transição {transicao} recusada — "
                f"{len(avaliacao.bloqueantes)} lacuna(s) bloqueante(s) aberta(s)."
            )
        return (
            f"{cabecalho}\n\n{avaliacao.resumo()}\n\n"
            f"Responda as bloqueantes acima antes de {antes_de}. "
            "Nada foi gravado no estado."
        )
    except Exception as erro:  # noqa: BLE001 — predicado que libera portão falha fechado
        return (
            f"ENGINE: transição {transicao} recusada — não foi possível "
            f"avaliar a descoberta ({erro.__class__.__name__}): {erro}\n\n"
            "O gate falha FECHADO de propósito: sem veredito confiável, a passagem "
            "não abre. Nada foi gravado no estado."
        )


def _exigir_descoberta_para_o_plano(raiz: Path, dados_do_programa: dict) -> None:
    """Gate gêmeo do C4, um andar acima: `CONCEPCAO -> PLANO_MESTRE`.

    Levanta `programa.DescobertaIncompleta` — exceção nomeada, subclasse de
    `PlanoInvalido` — quando a macro-DESCOBERTA não está fechada. Levantar em vez de
    devolver mensagem é o que faz a recusa ser um contrato: quem chamar este caminho
    programaticamente amanhã não tem como confundir recusa com sucesso por esquecer de
    olhar um valor de retorno.

    **Só a aresta protegida.** O gate roda apenas quando o programa está em CONCEPCAO.
    Rodar sempre trocaria a mensagem de erro de quem pede `programa plano` com o
    programa já em EXECUCAO: aquilo é erro de grafo, `transicionar` já diz isso com
    precisão, e o gate mentiria dizendo que o problema é a descoberta. É a mesma regra
    que `ARESTA_COM_GATE_DE_DESCOBERTA` aplica no ciclo.

    **Aqui a leitura do disco é legítima**, ao contrário de dentro de
    `_gate_descoberta`: o veredito sai do `.engine/estado.json`, e neste ponto nenhum
    cadeado está tomado — nem o do estado (só `estado.atualizar` o toma) nem o do
    programa (o sub-verbo `plano` lê e grava `programa.json` direto, como todos os
    outros sub-verbos). Não há cadeado para retomar, então não há o travamento não
    reentrante que o C4 proíbe. O que continua valendo é a proibição de o **gate** ler:
    ele recebe o dicionário, e quem lê é este chamador.
    """
    if dados_do_programa.get("estado") != ARESTA_DO_PROGRAMA_COM_GATE[0]:
        return
    recusa = _gate_descoberta(
        estado.carregar_estrito(raiz),
        transicao=" -> ".join(ARESTA_DO_PROGRAMA_COM_GATE),
        antes_de="propor o plano-mestre",
    )
    if recusa is not None:
        raise programa.DescobertaIncompleta(recusa)


def _verbo_fase(raiz: Path, resto: list[str]) -> int:
    """Transição de fase — a mutação que mais doía perder.

    Antes, `carregar_estrito` … `transicionar` … `gravar` eram três passos soltos:
    outra sessão que gravasse no meio via a sua escrita apagada, e o usuário desta
    sessão já tinha visto a transição confirmada na tela. Agora a leitura e a
    gravação acontecem dentro do mesmo cadeado, e `transicionar` valida o grafo
    contra a fase que está no disco AGORA, não contra a que se leu antes.

    **O gate de descoberta é checado DE DENTRO do mutador, e não antes dele.** As duas
    posições recusam a transição; só uma decide sobre o estado que vai ser gravado.
    Consultando antes, a leitura aconteceria fora do cadeado e o veredito seria sobre
    um retrato velho: outra sessão pode registrar a descoberta (ou apagá-la) entre a
    consulta e a mutação, e o resultado seria transição liberada por uma bloqueante já
    aberta — ou barrada por uma que acabou de ser respondida. Aqui dentro, o mesmo
    dicionário que o gate leu é o que `transicionar` altera, e devolver `None` faz
    `atualizar` sair sem gravar: nem a fase, nem `fases_concluidas`, nem carimbo
    nenhum. É por isso que o `estado.json` sai byte-idêntico da recusa.
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
        if (dados.get("fase"), destino) == ARESTA_COM_GATE_DE_DESCOBERTA:
            recusa = _gate_descoberta(dados)
            if recusa is not None:
                falha.append(recusa)
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


# ---------------------------------------------------------------------------
# Descoberta — o caminho de SAÍDA do portão que `_gate_descoberta` fecha
# ---------------------------------------------------------------------------
#
# O gate recusa a transição e imprime as perguntas; até este ciclo, responder essas
# perguntas só existia como API Python (`descoberta.registrar` / `descoberta.responder`).
# Portão sem saída: a skill não tem como chamar Python direto, e a única forma de
# destravar era editar `.engine/estado.json` à mão — que é exatamente o que a mensagem
# de recusa manda não fazer. Os três verbos abaixo são a saída.


def _relatar_descoberta(avaliacao) -> str:
    """O retrato da entrevista: intenção, bloqueantes e assumíveis, com a pergunta inteira.

    O miolo é `Avaliacao.resumo()`, o **mesmo** texto que a recusa do gate imprime. Um
    formato próprio aqui divergiria do outro no primeiro ajuste, e a divergência
    apareceria da pior forma possível: `status` dizendo uma coisa e a recusa da transição
    dizendo outra sobre o mesmo estado.

    O que se acrescenta é o pedido (que o `resumo` não traz, e que é o texto sobre o qual
    a entrevista inteira foi montada) e a linha do veredito — quem leu "bloqueado" quer
    saber, na mesma tela, o comando que responde.
    """
    linhas = [
        "# Descoberta",
        "",
        f"**Pedido:** {avaliacao.pedido or '(nenhum)'}",
        "",
        avaliacao.resumo(),
        "",
    ]
    if avaliacao.liberado_para_planejar:
        linhas.append(
            "**Porta da descoberta ABERTA:** nenhuma bloqueante em aberto — "
            "`fase ANALISE` passa."
        )
    else:
        linhas.append(
            "**Porta da descoberta FECHADA.** Responda cada bloqueante com "
            '`descoberta responder <ID> "<resposta>"`.'
        )
    return "\n".join(linhas)


def _imprimir_descoberta(raiz: Path, descoberta) -> int:
    """Lê o estado, imprime o retrato da descoberta e devolve o código de saída.

    **A leitura do disco é legítima aqui**, ao contrário de dentro de
    `_gate_descoberta`: neste ponto nenhum cadeado está tomado — os três verbos leem e
    escrevem por `descoberta.registrar`/`descoberta.responder`, que tomam e soltam o
    cadeado por conta própria antes de voltar. O que continua proibido é o **gate** ler
    por caminho, porque ele roda com o cadeado na mão e ele não é reentrante.

    `carregar_estrito`, e não `avaliar_do_disco` (que usa o leniente): estado ilegível
    devolveria `None` no leniente e a avaliação sairia `registrada=False` — "o arquivo
    está corrompido" contado como "nunca houve descoberta". São diagnósticos opostos e o
    conserto de cada um é diferente.
    """
    try:
        avaliacao = descoberta.avaliar(estado.carregar_estrito(raiz))
    except estado.EstadoCorrompido as erro:
        print(f"ENGINE: {erro}")
        return 1
    except descoberta.DescobertaInvalida as erro:
        print(f"ENGINE: bloco de descoberta ilegível — {_texto_do_erro(erro)}")
        return 1
    if not avaliacao.registrada:
        print(
            "ENGINE: nenhuma descoberta registrada neste projeto. Rode "
            '`descoberta "<o que o usuário pediu>"` primeiro.'
        )
        return 1
    print(_relatar_descoberta(avaliacao))
    return 0


def _pedido_e_sinalizadores(resto: list[str]) -> tuple[str | None, str, str | None]:
    """Separa `--intencao` e `--forcar` do pedido. Devolve (intenção, pedido, erro de uso).

    As duas formas de `--intencao` são aceitas (`--intencao MATERIALIZAR` e
    `--intencao=MATERIALIZAR`) porque as duas são igualmente naturais para quem digita, e
    recusar uma delas seria um erro de uso onde não há ambiguidade nenhuma.

    O erro de uso volta como texto em vez de exceção porque este é o único caso em que
    não há o que fazer além de imprimir: `--intencao` sem valor depois não tem palpite
    razoável — o próximo argumento seria parte do pedido, e engoli-lo classificaria o
    trabalho por um pedaço de frase.
    """
    intencao: str | None = None
    palavras: list[str] = []
    indice = 0
    while indice < len(resto):
        palavra = resto[indice]
        if palavra == "--intencao":
            if indice + 1 >= len(resto):
                return (
                    None,
                    "",
                    "ENGINE: `--intencao` exige o nome da intenção logo depois.\n"
                    + USO_DESCOBERTA,
                )
            intencao = resto[indice + 1]
            indice += 2
            continue
        if palavra.startswith("--intencao="):
            intencao = palavra.split("=", 1)[1]
            indice += 1
            continue
        if palavra == "--forcar":
            indice += 1
            continue
        palavras.append(palavra)
        indice += 1
    return intencao, " ".join(palavras).strip(), None


def _pedir_a_intencao(erro, pedido: str, conhecidas: list[str]) -> str:
    """A pergunta de desempate — o único caminho em que a CLI devolve a decisão inteira.

    `classificar` levanta `IntencaoIndeterminada` em dois casos: sinal ausente/fraco e
    sinal empatado. Nos dois, a exceção carrega `candidatas` justamente para que quem
    chamou consiga **perguntar** em vez de apenas relatar o erro — e é isso que este
    texto faz. Escolher a primeira candidata aqui seria o `PADRAO_ASSUMIDO` de
    `deteccao.py` circulando como decisão, com o agravante de que a intenção decide
    *quais perguntas existem*: a errada não produz uma pergunta ruim no meio de vinte
    boas, produz uma entrevista inteira sobre outro trabalho, e a pessoa responde tudo
    antes de alguém notar.
    """
    candidatas = tuple(getattr(erro, "candidatas", ()) or ())
    linhas = [
        "ENGINE: descoberta NÃO registrada — não dá para dizer que tipo de trabalho "
        "este pedido pede.",
        "",
        _texto_do_erro(erro),
        "",
    ]
    if candidatas:
        linhas.append("Candidatas (o motor não escolhe entre elas):")
        linhas += [f"  - {getattr(alvo, 'value', alvo)}" for alvo in candidatas]
    else:
        linhas.append(
            "Nenhuma candidata: o texto não trouxe sinal de intenção nenhum."
        )
    linhas += [
        "",
        "**Diga qual é.** A intenção decide QUAIS perguntas existem, e por isso ela não "
        "é chutada aqui: a classe errada não produz uma pergunta ruim, produz uma "
        "entrevista inteira sobre outro trabalho.",
        "",
        f'  descoberta "{pedido}" --intencao <INTENCAO>',
        "",
        "Intenções conhecidas: " + ", ".join(conhecidas),
        "",
        "Nada foi gravado no estado.",
    ]
    return "\n".join(linhas)


def _verbo_descoberta(raiz: Path, resto: list[str]) -> int:
    """Registrar a entrevista, ver o que falta e responder — pela CLI, sem Python solto.

    Três sub-verbos, e o resto da linha é o pedido, na mesma forma de `_verbo_programa`:
    `status` e `responder` são palavras reservadas, e um pedido que comece por uma delas
    precisa vir depois de `--intencao` ou ser reescrito. É o mesmo acordo que `programa`
    já faz, e trocá-lo aqui daria duas gramáticas para a mesma CLI.

    O `import` mora dentro da função pelo mesmo motivo que dentro de `_gate_descoberta`:
    importado no topo, um `ferramentas/descoberta.py` quebrado estouraria na carga do
    módulo — antes de `principal` existir para segurar a exceção — e derrubaria com
    traceback a CLI inteira, inclusive `status` e `desligar`, que nada têm com a
    elicitação.

    **Nenhum destes verbos grava estado por conta própria.** Todos passam por
    `descoberta.registrar`/`descoberta.responder`, que mutam de dentro do cadeado por
    `estado.atualizar`. É a mesma trava textual que `test_nenhum_gravar_fora_do_estado`
    varre neste arquivo.
    """
    if not resto:
        print(USO_DESCOBERTA)
        return 1

    try:
        from ferramentas import descoberta  # noqa: PLC0415 — ver docstring
        from ferramentas.elicitacao import (  # noqa: PLC0415 — ver docstring
            Intencao,
            IntencaoIndeterminada,
        )
    except ImportError as erro:
        print(
            "ENGINE: instalação incompleta — a elicitação não pôde ser importada "
            f"({erro.__class__.__name__}): {erro}"
        )
        return 1

    sub, *args = resto
    agora = _agora()

    if sub == "status":
        return _imprimir_descoberta(raiz, descoberta)

    if sub == "responder":
        if len(args) < 2:
            print(USO_DESCOBERTA)
            return 1
        lacuna_id, *palavras = args
        valor = " ".join(palavras).strip()
        if not valor:
            print(
                "ENGINE: resposta em branco não é resposta — a lacuna continuaria "
                "aberta, agora com um vazio no lugar da pergunta. Nada foi gravado."
            )
            return 1
        try:
            descoberta.responder(raiz, lacuna_id, valor, agora=agora)
        except (descoberta.DescobertaAusente, descoberta.LacunaDesconhecida) as erro:
            # Id que não está ativo para este pedido não é aceito em silêncio: a
            # resposta iria para um balde que ninguém lê, a lacuna verdadeira
            # continuaria aberta e a pessoa lembraria de ter respondido.
            print(f"ENGINE: {_texto_do_erro(erro)}")
            return 1
        except descoberta.DescobertaInvalida as erro:
            print(f"ENGINE: bloco de descoberta ilegível — {_texto_do_erro(erro)}")
            return 1
        except (estado.EstadoCorrompido, estado.EstadoOcupado) as erro:
            print(f"ENGINE: {erro}")
            return 1
        print(f"**Respondida:** [{lacuna_id}] {valor}")
        print()
        return _imprimir_descoberta(raiz, descoberta)

    forcar = "--forcar" in resto
    intencao, pedido, erro_de_uso = _pedido_e_sinalizadores(resto)
    if erro_de_uso is not None:
        print(erro_de_uso)
        return 1
    if not pedido:
        print(
            "ENGINE: `descoberta <pedido>` exige o pedido do usuário, com as palavras "
            "dele. É sobre esse texto que a intenção é classificada."
        )
        return 1

    try:
        anterior = descoberta.do_estado(estado.carregar_estrito(raiz))
    except estado.EstadoCorrompido as erro:
        print(f"ENGINE: {erro}")
        return 1
    except descoberta.DescobertaInvalida as erro:
        print(f"ENGINE: bloco de descoberta ilegível — {_texto_do_erro(erro)}")
        return 1
    respostas = (anterior or {}).get("respostas") or {}
    if respostas and not forcar:
        # `registrar` reescreve o bloco inteiro, e com ele o mapa de respostas. Sem esta
        # guarda, um segundo `descoberta <pedido>` — para corrigir uma palavra do texto,
        # que é o motivo mais natural de repetir o verbo — apagaria a entrevista já
        # respondida sem dizer nada, e a pessoa lembra de ter respondido.
        print(
            f"ENGINE: já existe descoberta registrada neste ciclo, com {len(respostas)} "
            "resposta(s). Registrar de novo recomeça a entrevista do zero e apaga o que "
            "foi respondido. Use `descoberta status` para ver o que falta, ou repita com "
            "`--forcar` se a intenção é mesmo recomeçar. Nada foi gravado no estado."
        )
        return 1

    try:
        descoberta.registrar(raiz, pedido, intencao=intencao, agora=agora)
    except IntencaoIndeterminada as erro:
        # Antes de `ValueError` porque é subclasse dela: invertida, esta cláusula nunca
        # rodaria e a pergunta de desempate viraria uma mensagem de intenção inválida.
        print(_pedir_a_intencao(erro, pedido, [alvo.value for alvo in Intencao]))
        return 1
    except ValueError as erro:
        if intencao is None:
            print(f"ENGINE: descoberta não registrada ({erro.__class__.__name__}): {erro}")
        else:
            print(
                f"ENGINE: intenção {intencao!r} não existe na taxonomia. Conhecidas: "
                + ", ".join(alvo.value for alvo in Intencao)
            )
        return 1
    except descoberta.DescobertaAusente as erro:
        print(f"ENGINE: {_texto_do_erro(erro)}")
        return 1
    except (estado.EstadoCorrompido, estado.EstadoOcupado) as erro:
        print(f"ENGINE: {erro}")
        return 1

    print("**Descoberta registrada.**")
    print()
    return _imprimir_descoberta(raiz, descoberta)


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
            # O gate da macro-DESCOBERTA vem ANTES de `propor_plano`, e é por isso que
            # a recusa não deixa rastro: `propor_plano` sequer é chamada, então nada
            # transiciona, e `programa.gravar` lá embaixo não é alcançado. Se viesse
            # depois, `propor_plano` já teria devolvido o dicionário em PLANO_MESTRE, e
            # bastaria um `return` esquecido para gravá-lo — a mesma armadilha que o C4
            # fechou pondo o gate dentro do mutador em vez de depois de `transicionar`.
            _exigir_descoberta_para_o_plano(raiz, dados)
            novo = programa.propor_plano(
                dados,
                bruto.get("ciclos") or [],
                bruto.get("aceite_de_sistema", ""),
            )
        except programa.DescobertaIncompleta as erro:
            # Antes de `PlanoInvalido` porque é subclasse dela: invertida, esta cláusula
            # nunca rodaria. E a mensagem sai sem prefixo — ela já vem no formato do
            # gate de fase, com "ENGINE:" na frente e as perguntas inteiras dentro.
            print(erro)
            return 1
        except estado.EstadoCorrompido as erro:
            # O veredito da descoberta sai do `estado.json`; ilegível, ele não vira
            # "sem bloqueante". Falha FECHADA, com a mesma mensagem que os outros
            # verbos dão para estado corrompido.
            print(f"ENGINE: {erro}")
            return 1
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
        if verbo == "descoberta":
            return _verbo_descoberta(raiz, resto)
        if verbo == "programa":
            return _verbo_programa(raiz, resto)
        print(USO)
        return 1
    except Exception as erro:  # rede de segurança: nenhum verbo termina em traceback
        print(f"ENGINE: erro inesperado ({erro.__class__.__name__}): {erro}")
        return 1


if __name__ == "__main__":
    sys.exit(principal(sys.argv[1:]))
