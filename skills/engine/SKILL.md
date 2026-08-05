---
name: engine
description: Liga o modo ENGINE — motor de engenharia com ciclo em fases, elenco de agentes por papel e portas de segurança graduadas por risco. Use quando o pedido for "/engine", "/engine off", "/engine status", "ligar o motor", "desligar o motor", ou quando o usuário pedir para conduzir um trabalho de engenharia de ponta a ponta.
---

# ENGINE

Motor de engenharia persistente. O ciclo é sempre do motor: ferramenta externa (ECC,
superpowers) executa **dentro** de uma fase; nenhuma decide qual é a fase seguinte nem
quando o ciclo termina. Instrução direta do usuário sempre vence o motor.

## Verbos

| Pedido do usuário | O que fazer |
|---|---|
| `/engine <pedido>` | rode `ENGINE_RAIZ="$(pwd)" bash "${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh" "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" ligar "<objetivo em uma frase>"` e entre em DESCOBERTA |
| `/engine off` | rode `ENGINE_RAIZ="$(pwd)" bash "${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh" "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" desligar` e apresente o resumo do ciclo |
| `/engine status` | rode `ENGINE_RAIZ="$(pwd)" bash "${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh" "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" status` e apresente a saída |
| `/engine <pedido> --dry` | rode `ENGINE_RAIZ="$(pwd)" bash "${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh" "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" ligar "<objetivo em uma frase>" --dry` — use para um ciclo que só planeja e relata, sem escrever |
| `/engine retomar` | rode `ENGINE_RAIZ="$(pwd)" bash "${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh" "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" retomar` e apresente o resumo de reentrada — use quando a sessão é nova mas o ciclo já existe |
| `/engine relatorio` | rode `ENGINE_RAIZ="$(pwd)" bash "${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh" "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" relatorio ciclo` (ou `relatorio fase <FASE>`) e apresente a saída |
| `/engine programa <objetivo>` | conduz um **sistema inteiro** como sequência de ciclos — ver a seção "O programa" |

Essa é a forma que funciona **de qualquer diretório e em qualquer plataforma**, e é a
única que se deve usar. O diretório corrente é o do projeto do usuário, não o do plugin:
ali `python -m ferramentas.cli` falha com `ModuleNotFoundError: No module named
'ferramentas'`, porque o pacote do plugin não está no `sys.path`. E o interpretador nunca
é invocado por nome fixo: `hooks/engine.sh` — o mesmo lançador dos cinco hooks — detecta
em runtime `py` (Windows), `python3` ou `python`, o que existir no PATH; chamar `py`
direto quebraria em macOS/Linux, onde o Python Launcher não existe. (Não passe
`--travar-sem-python` aqui: essa flag é exclusiva do hook `PreToolUse`; para a CLI, o
lançador sem Python sai 0 em silêncio, que é o certo.) `${CLAUDE_PLUGIN_ROOT}` é
expandido pelo Claude Code para a raiz do plugin instalado, e `ENGINE_RAIZ` diz à CLI
qual é o projeto hospedeiro — o diretório corrente. Nunca troque de diretório para rodar
a CLI.

Se `ligar` recusar porque já existe um ciclo ativo, apresente o objetivo do ciclo em
andamento ao usuário e pergunte se quer retomá-lo ou recomeçar. Só acrescente `--forcar`
ao fim do comando de `ligar` se o usuário confirmar explicitamente que quer descartar o
ciclo em andamento.

## O ciclo

`DESCOBERTA → ANALISE → [EVOLUCAO, se o projeto já existe] → PLANO → ⟨porta⟩ → BUILD ⇄
TESTE → REVISAO → DOC → ENTREGA`

Avance de fase com `ENGINE_RAIZ="$(pwd)" bash "${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh" "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" fase
<DESTINO>`. A CLI recusa transição fora do grafo — se ela recusar, a fase pretendida está
errada, não a máquina.

**Porta do plano.** Ao terminar PLANO, apresente arquitetura, stack, estrutura e a
justificativa de cada decisão, e **espere** o usuário. É a única parada por fase.

## O programa — sistemas inteiros, não um ciclo

Um ciclo entrega **um** trabalho de engenharia. Um sistema de alta complexidade é uma
**sequência** de ciclos com dependências, e é isso que o modo PROGRAMA conduz.

`CONCEPCAO → PLANO_MESTRE → ⟨porta⟩ → EXECUCAO → ACEITE_SISTEMA → CONCLUIDO`

Todos os comandos abaixo usam o mesmo prefixo dos demais verbos
(`ENGINE_RAIZ="$(pwd)" bash "${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh"
"${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" …`), aqui abreviado como `CLI`.

| Pedido | O que fazer |
|---|---|
| `/engine programa <objetivo>` | `CLI programa "<objetivo em uma frase>"` — abre em CONCEPCAO |
| decompor | escreva o plano num JSON e rode `CLI programa plano <arquivo.json>` |
| `/engine programa status` | `CLI programa status` |
| `/engine programa retomar` | `CLI programa retomar` — sessão nova, programa que já existe |

**Como conduzir a EXECUCAO.** Em laço, até não haver mais ciclo elegível:

1. `CLI programa proximo` — diz qual ciclo ligar e qual é o critério de aceite dele.
2. `CLI ligar "<objetivo daquele ciclo>"` e conduza o ciclo **normalmente**, com todas as
   fases, papéis e gates de sempre. O programa não muda nada dentro do ciclo.
3. Ao chegar em ENTREGA, **rode o critério de aceite declarado** e olhe a saída.
4. `CLI programa aceite <CICLO> ok` — ou `falhou`. Nunca informe `ok` sem ter rodado o
   critério e visto o resultado: é a invariante 1 aplicada ao encadeamento.
5. `CLI desligar` e volte ao passo 1.

Quando `proximo` disser que todos concluíram, rode o aceite de sistema declarado no plano,
e então `CLI programa sistema ok` (ou `falhou`). Aceite vermelho devolve o programa para
EXECUCAO — nada é dado como concluído.

**A porta do plano-mestre.** Ao terminar o PLANO_MESTRE, apresente a decomposição inteira,
com dependências e critérios de aceite, e **espere**. `programa aprovar` é o único verbo do
motor que **você nunca roda por conta própria** — só o usuário autoriza, dizendo-o
explicitamente. É a única parada garantida do programa: depois dela os ciclos encadeiam
sozinhos.

**Quando parar no meio.** Só por desvio, e só por um destes quatro motivos:
`stack-fora-do-plano`, `dependencia-nao-prevista`, `aceite-inalcancavel`,
`escopo-fora-do-declarado`. Rode `CLI programa desviar <motivo> "<detalhe>"`, apresente o
conflito e espere. Fora disso não pergunte: parada que sempre acontece deixa de ser sinal.

**Um ciclo reprovado bloqueia os dependentes** — é o desenho, não um defeito. Corrija e
rode `CLI programa reabrir <CICLO>`.

Os gates de risco R1–R9 valem **idênticos** em modo programa. Autonomia de processo não é
autonomia de risco: com ninguém olhando, o gate vale mais, não menos.

## Papéis

Despache o subagente do papel correspondente à fase (`agents/`). Antes de despachar, leia
os cartões de `cartoes/` relevantes à stack e passe o conteúdo ao subagente.

| Fase | Papel |
|---|---|
| DESCOBERTA | `descobridor` |
| ANALISE / EVOLUCAO | `cartografo` |
| PLANO | `arquiteto` (e `designer`, quando houver direção visual a decidir) |
| BUILD | `implementador` |
| TESTE | `testador` |
| REVISAO | `revisor` e `sentinela` |
| DOC | `documentador` |

## Quando o hook travar uma ação

O hook de risco devolve `[R<n>] ação travada`. Não tente de novo por outro caminho, não
contorne com outra ferramenta. Apresente ao usuário **o que pretende fazer e o impacto**, e
peça confirmação com opções clicáveis.

## Invariantes

Valem em toda fase, e o hook de contexto os relembra a cada turno:

1. Nunca afirmar sucesso sem ter olhado.
2. Nunca ajustar o teste para o código passar.
3. Nunca inventar arquivo, API, número ou regra de negócio.
4. Nunca tocar em item fora do escopo declarado do ciclo.
5. Toda decisão técnica sai com a justificativa junto.
