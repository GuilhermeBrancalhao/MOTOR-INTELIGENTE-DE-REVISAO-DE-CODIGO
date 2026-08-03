---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 01-Introducao
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Introdução

Um agente de IA, na prática de engenharia, não é o modelo — é o loop em torno dele: receber um
objetivo, decidir uma ação (chamar uma ferramenta, gerar texto, encerrar), observar o resultado
e decidir a próxima ação, até um critério de parada. Sem um motor que orquestra esse loop, cada
funcionalidade "com agente" reimplementa a mesma máquina de estados do zero — e reimplementações
diferentes divergem exatamente nos pontos mais caros de acertar: quando parar (custo, tempo,
número de passos), como tratar erro de ferramenta (retry? falha? pergunta ao usuário?), e como
auditar o que o agente decidiu e por quê.

Este volume descreve o motor que resolve esse problema uma vez: o ciclo de vida de uma execução
de agente, o contrato do loop de tool-calling, e o orçamento (passos, tokens, tempo) que
impede uma execução de nunca terminar. Ele não descreve nenhum modelo de linguagem específico
nem nenhuma ferramenta específica — descreve a máquina que os conecta de forma auditável e
limitada.

A fronteira mais importante deste volume é com `09-ORCHESTRATOR`: este volume trata de **uma**
execução de agente, do início ao fim; `09` trata de **múltiplas** execuções coordenadas — vários
agentes, ou várias etapas que podem envolver agentes diferentes. Confundir os dois produz um
motor que tenta fazer as duas coisas ao mesmo tempo e não faz nenhuma delas com uma interface
limpa. A distinção prática: se a pergunta é "como este agente decide o próximo passo", é `08`;
se a pergunta é "qual agente roda depois de qual", é `09`.

O motor descrito aqui assume que a decisão de *quando* invocar um agente já foi tomada por quem
o chama — ele não decide se um agente deveria rodar, só executa o loop depois que a decisão foi
tomada, do primeiro passo até o critério de parada.
