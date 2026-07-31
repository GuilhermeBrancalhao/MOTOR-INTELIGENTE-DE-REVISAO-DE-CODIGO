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
| `/engine <pedido>` | rode `python -m ferramentas.cli ligar "<objetivo em uma frase>"` e entre em DESCOBERTA |
| `/engine off` | rode `python -m ferramentas.cli desligar` e apresente o resumo do ciclo |
| `/engine status` | rode `python -m ferramentas.cli status` e apresente a saída |

Rode sempre a partir da raiz do plugin, com `ENGINE_RAIZ` apontando para a raiz do projeto
em que se está trabalhando.

Se `ligar` recusar porque já existe um ciclo ativo, apresente o objetivo do ciclo em
andamento ao usuário e pergunte se quer retomá-lo ou recomeçar. Só use
`python -m ferramentas.cli ligar "<objetivo>" --forcar` se o usuário confirmar
explicitamente que quer descartar o ciclo em andamento.

## O ciclo

`DESCOBERTA → ANALISE → [EVOLUCAO, se o projeto já existe] → PLANO → ⟨porta⟩ → BUILD ⇄
TESTE → REVISAO → DOC → ENTREGA`

Avance de fase com `python -m ferramentas.cli fase <DESTINO>`. A CLI recusa transição fora
do grafo — se ela recusar, a fase pretendida está errada, não a máquina.

**Porta do plano.** Ao terminar PLANO, apresente arquitetura, stack, estrutura e a
justificativa de cada decisão, e **espere** o usuário. É a única parada por fase.

## Papéis

Despache o subagente do papel correspondente à fase (`agents/`): `arquiteto` no PLANO,
`implementador` no BUILD, `revisor` na REVISAO, `documentador` no DOC. Antes de despachar,
leia os cartões de `cartoes/` relevantes à stack e passe o conteúdo ao subagente.

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
