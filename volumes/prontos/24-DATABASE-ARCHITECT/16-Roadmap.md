---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Exclusão em cascata explícita e auditável, para o caso em que propagar a exclusão é de fato a
decisão correta (hoje o modelo só rejeita; não oferece um caminho estruturado para "excluir e
também excluir o que referencia, com registro de que isso foi decidido assim").

Reconciliação automática de conflito de concorrência para casos onde a mudança é comutativa
(por exemplo, dois incrementos concorrentes do mesmo contador) — hoje todo conflito é tratado
identicamente, sem distinguir casos onde a resolução poderia ser automática e segura.

Verificação automática de compatibilidade de migração (hoje `compativel_com_versao_anterior` é
uma declaração manual, sem verificação estrutural contra o schema real anterior e posterior).

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (migração, proveniência, concorrência otimista,
retenção, leitura tolerante), testado por mutação nas seis regras. Depois, integração real com o
fluxo de gravação do `23-BACKEND-ARCHITECT`.

## O que este volume assume que pode mudar

O modelo de concorrência otimista por número de versão inteiro é o mínimo suficiente hoje — um
esquema mais expressivo (vetor de versão distribuído, timestamp lógico) pode ser necessário
conforme a escala de escrita concorrente cresce, sem alterar o princípio central de detecção
explícita de conflito antes de qualquer sobrescrita.
