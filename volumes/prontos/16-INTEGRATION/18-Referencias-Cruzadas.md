---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; a fronteira que ele define (produto
versus fora do produto) é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `22-25 (arquitetura de camada)` | Chamada entre camadas do mesmo produto é daqueles volumes; chamada que cruza a fronteira do produto é deste |
| `06-ENTERPRISE-ARCHITECTURE` | Consome achado de duplicação de integração deste volume para decisão de portfólio sobre concentração de fornecedor |
| `27-LLM-ROUTER` | Uma chamada a provedor de modelo é integração externa; este volume garante robustez da chamada, aquele decide qual provedor |
| `17-SECURITY` | Decide o que pode cruzar a fronteira em termos de sensibilidade de dado; este volume garante que a chamada em si é robusta |

## Links que resolvem hoje

- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../ROADMAP.md`](../ROADMAP.md) — grupo 4 (camadas contra integração), fronteira decidida em 2026-07-29

## Navegação interna

Para entender o critério central: `01-Introducao.md` seguido de `07-Regras.md`. Para o circuit
breaker em detalhe: `05-Diagramas.md` (o `flowchart` de estados) seguido de `06-Fluxogramas.md`.
