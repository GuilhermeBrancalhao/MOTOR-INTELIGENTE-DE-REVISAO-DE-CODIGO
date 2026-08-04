---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de trabalho assíncrono, worker
sem estado, backpressure e idempotência é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `24-DATABASE-ARCHITECT` | Onde e como o estado do trabalho persiste; este volume define o modelo lógico independente da tecnologia |
| `25-API-ARCHITECT` | O contrato que expõe o estado do trabalho ao cliente; este volume garante que existe um estado consultável para expor |
| `16-INTEGRATION` | A robustez da chamada de IA específica dentro de um trabalho; este volume trata da idempotência do trabalho como um todo |
| `22-FRONTEND-ARCHITECT` | Consome o estado consultável deste volume para decidir estado de carregamento, streaming e fallback na interface |

## Links que resolvem hoje

- [`../16-INTEGRATION/07-Regras.md`](../16-INTEGRATION/07-Regras.md) — regras da chamada externa
  que um trabalho pode envolver
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para a política de
retry em detalhe: `06-Fluxogramas.md` seguido de `13-Testes.md`.
