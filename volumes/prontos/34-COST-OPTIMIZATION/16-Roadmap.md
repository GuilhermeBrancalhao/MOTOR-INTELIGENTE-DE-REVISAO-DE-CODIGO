---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Alerta automático de tendência de custo, além do alerta de orçamento por escopo — hoje a
detecção de tendência (U4) produz um resultado consultável, mas sem gatilho automático de
notificação quando o crescimento ultrapassa um ritmo esperado.

Alocação de custo compartilhado entre múltiplos escopos por uma mesma tarefa — hoje o modelo
assume atribuição a um único escopo por registro, sem mecanismo de divisão proporcional entre
escopos que compartilham o benefício de uma mesma tarefa.

Projeção de custo futuro baseada em tendência histórica — hoje o volume detecta tendência
passada, sem produzir uma estimativa de gasto esperado para o período seguinte.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (custo por tarefa, atribuição a escopo, orçamento com
alerta, tendência, otimização validada), testado por mutação nas seis regras. Depois, integração
real com o registro de trabalho do `23-BACKEND-ARCHITECT` como fonte de tarefas concluídas.

## O que este volume assume que pode mudar

O modelo de três estados de orçamento (OK, ALERTA, ESTOURADO) é o mínimo suficiente hoje — um
esquema com múltiplos degraus de alerta pode ser necessário conforme a criticidade de escopos
específicos cresce, sem alterar o princípio central de custo por tarefa, atribuído, com alerta
antecipado.
