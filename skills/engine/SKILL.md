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
| `/engine <pedido>` | rode `ENGINE_RAIZ="$(pwd)" py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" ligar "<objetivo em uma frase>"` e entre em DESCOBERTA |
| `/engine off` | rode `ENGINE_RAIZ="$(pwd)" py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" desligar` e apresente o resumo do ciclo |
| `/engine status` | rode `ENGINE_RAIZ="$(pwd)" py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" status` e apresente a saída |
| `/engine <pedido> --dry` | rode `ENGINE_RAIZ="$(pwd)" py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" ligar "<objetivo em uma frase>" --dry` — use para um ciclo que só planeja e relata, sem escrever |
| `/engine retomar` | rode `ENGINE_RAIZ="$(pwd)" py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" retomar` e apresente o resumo de reentrada — use quando a sessão é nova mas o ciclo já existe |
| `/engine relatorio` | rode `ENGINE_RAIZ="$(pwd)" py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" relatorio ciclo` (ou `relatorio fase <FASE>`) e apresente a saída |

Essa é a forma que funciona **de qualquer diretório**, e é a única que se deve usar. O
diretório corrente é o do projeto do usuário, não o do plugin: ali `python -m
ferramentas.cli` falha com `ModuleNotFoundError: No module named 'ferramentas'`, porque o
pacote do plugin não está no `sys.path`. `${CLAUDE_PLUGIN_ROOT}` é expandido pelo Claude
Code para a raiz do plugin instalado, e `ENGINE_RAIZ` diz à CLI qual é o projeto
hospedeiro — o diretório corrente. Nunca troque de diretório para rodar a CLI.

Se `ligar` recusar porque já existe um ciclo ativo, apresente o objetivo do ciclo em
andamento ao usuário e pergunte se quer retomá-lo ou recomeçar. Só acrescente `--forcar`
ao fim do comando de `ligar` se o usuário confirmar explicitamente que quer descartar o
ciclo em andamento.

## O ciclo

`DESCOBERTA → ANALISE → [EVOLUCAO, se o projeto já existe] → PLANO → ⟨porta⟩ → BUILD ⇄
TESTE → REVISAO → DOC → ENTREGA`

Avance de fase com `ENGINE_RAIZ="$(pwd)" py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" fase
<DESTINO>`. A CLI recusa transição fora do grafo — se ela recusar, a fase pretendida está
errada, não a máquina.

**Porta do plano.** Ao terminar PLANO, apresente arquitetura, stack, estrutura e a
justificativa de cada decisão, e **espere** o usuário. É a única parada por fase.

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
