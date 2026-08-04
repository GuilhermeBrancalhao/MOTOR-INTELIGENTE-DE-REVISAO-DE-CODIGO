---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Toda chamada a um modelo de linguagem tem um limite de tokens que cabem na janela, e esse limite
não é uma restrição rara — é a condição normal de operação de qualquer sistema que acumula
histórico, documentos recuperados, e instruções ao longo de uma sessão. O que diferencia um
sistema bem desenhado de um que degrada silenciosamente não é ter ou não esse limite — é o que
acontece quando o conteúdo desejado excede o que cabe.

Este volume trata do orçamento da janela de contexto como recurso finito e gerenciado
explicitamente: o que entra, em que ordem de prioridade, o que é descartado quando o limite é
atingido, e quando a compactação (resumir ou remover parte do histórico) é acionada. A analogia
com orçamento financeiro é deliberada — assim como dinheiro, tokens de contexto precisam de
prioridade declarada antes de escassear, não decidida às pressas quando o limite já foi atingido.

A independência deste volume em relação a `13-RAG` é a decisão mais importante do grupo: o
orçamento de janela vale para qualquer sistema com modelo de linguagem, com ou sem recuperação de
conhecimento. Um agente que só processa histórico de conversa, sem nenhum documento recuperado,
ainda precisa decidir o que descartar quando a conversa cresce além do limite — e essa decisão é
deste volume, não de um pipeline de RAG que talvez nem exista no sistema.
