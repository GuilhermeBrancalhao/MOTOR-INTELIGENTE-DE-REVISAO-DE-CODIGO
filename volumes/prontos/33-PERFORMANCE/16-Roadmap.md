---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Ajuste automático de SLO baseado em tendência histórica observada, em vez de valor declarado
estaticamente uma vez — hoje o SLO é uma decisão manual, sem realimentação automática do
comportamento real medido ao longo do tempo.

Simulação de sobrecarga automatizada como parte do processo de validação de operação crítica —
hoje a boa prática recomenda testar a estratégia de degradação sob condição real, mas não há
mecanismo formal que force essa validação antes de produção.

Correlação automática entre regressão de desempenho e mudança de código específica que a causou —
hoje a investigação de regressão (J3) é um processo manual, sem ferramenta de correlação
automática integrada a este volume.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (SLO declarado, medição sob carga, regressão, otimização
validada), testado por mutação nas seis regras. Depois, integração real com o orçamento de
latência do `25-API-ARCHITECT` e a backpressure do `23-BACKEND-ARCHITECT`.

## O que este volume assume que pode mudar

O modelo de dois percentis (p95, p99) é o mínimo suficiente hoje — um esquema mais granular
(p50, p99.9, latência máxima absoluta) pode ser necessário conforme a criticidade de operações
específicas cresce, sem alterar o princípio central de SLO declarado e medido sob carga real.
