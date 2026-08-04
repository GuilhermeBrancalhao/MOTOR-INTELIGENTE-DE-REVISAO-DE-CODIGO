---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de SLO, medição sob carga e
regressão é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `25-API-ARCHITECT` | Orçamento de latência por endpoint síncrono é uma das entradas deste processo mais amplo |
| `32-QUALITY` | Dimensão independente de qualidade (correção verificada vs. desempenho medido) |
| `23-BACKEND-ARCHITECT` | Backpressure de trabalho assíncrono relacionada à degradação graciosa deste volume |
| `21-OBSERVABILITY` | Fonte real de medição sob carga de produção que alimenta a detecção de regressão deste volume |

## Links que resolvem hoje

- [`../25-API-ARCHITECT/07-Regras.md`](../25-API-ARCHITECT/07-Regras.md) — regra T6, orçamento de
  latência por endpoint que este volume formaliza como processo
- [`../32-QUALITY/07-Regras.md`](../32-QUALITY/07-Regras.md) — disciplina de investigação de
  regressão reaproveitada aqui para desempenho

## Navegação interna

Para entender o processo central: `01-Introducao.md` seguido de `07-Regras.md`. Para validação de
otimização em detalhe: `06-Fluxogramas.md` seguido de `13-Testes.md`.
