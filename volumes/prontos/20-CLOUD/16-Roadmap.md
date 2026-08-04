---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Correção automática de drift para uma categoria restrita e explicitamente segura de divergência
(hoje toda divergência é apenas reportada, nunca corrigida automaticamente, mesmo quando o caso
seria trivialmente seguro de reconciliar).

Alvo de disponibilidade composto, combinando múltiplos recursos interdependentes (hoje a
verificação de redundância trata cada recurso isoladamente, sem modelar quando a
indisponibilidade de um recurso não-redundante é mitigada pela redundância de outro que o
substitui funcionalmente).

Integração com a métrica de concentração de fornecedor do `06-ENTERPRISE-ARCHITECTURE` — hoje o
custo e a redundância são visíveis por recurso individual, mas não agregados automaticamente por
fornecedor para alimentar aquela decisão de portfólio.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (recurso declarado, redundância, isolamento de ambiente,
drift), testado por mutação nas seis regras. Depois, integração real com o pipeline do
`19-DEVOPS` como consumidor da infraestrutura declarada aqui.

## O que este volume assume que pode mudar

O modelo de redundância binária (`redundante: bool`) é o mínimo suficiente hoje — um esquema mais
expressivo (grau de redundância, zona de disponibilidade específica) pode ser necessário conforme
a complexidade da infraestrutura cresce, sem alterar o princípio central de verificação explícita
contra um alvo declarado.
