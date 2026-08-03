---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 02-Objetivos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Descrever o ciclo de vida de uma execução de agente** em estados nomeados (iniciado,
executando passo, aguardando ferramenta, encerrado por objetivo atingido, encerrado por
orçamento excedido, encerrado por erro) e dizer qual transição é permitida a partir de qual
estado — não como fluxo livre, mas como máquina de estados fechada.

**Definir o contrato do loop de tool-calling**: o que o motor envia ao modelo em cada passo
(histórico, ferramentas disponíveis, orçamento restante), o que espera de volta (uma ação
única por passo — chamada de ferramenta ou resposta final), e o que faz quando a resposta do
modelo não obedece ao contrato (formato inválido, ferramenta inexistente).

**Aplicar orçamento em três dimensões independentes** — passos, tokens, tempo de parede — e
explicar por que as três são necessárias e nenhuma substitui as outras: um agente pode estourar
tempo sem estourar passos (uma ferramenta lenta), ou estourar tokens sem estourar tempo (contexto
grande, resposta rápida do modelo).

**Diferenciar encerramento por objetivo atingido de encerramento por orçamento excedido**, e
explicar por que essa distinção precisa estar na trilha de auditoria — um chamador que trata os
dois como "terminou" perde a informação de que o agente pode não ter completado a tarefa.

**Traçar a fronteira com `09-ORCHESTRATOR`** de forma concreta: este volume owns a execução de
um agente; `09` owns a coordenação entre execuções (sequenciais, paralelas, condicionais).
