---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: ["11", "14"]` — este volume consome os dois como infraestrutura já correta; a leitura
pressupõe entender curadoria (`11`) e índice (`14`) antes de ler como os dois se juntam numa
resposta.

| Volume vizinho | Relação |
|---|---|
| `11-KNOWLEDGE` | Fornece validade de documento, consultada no momento da citação, não herdada da indexação |
| `14-VECTOR` | Fornece candidatos por proximidade vetorial; este volume reordena por relevância específica |
| `15-CONTEXT` | Decide quantos documentos cabem na janela; este volume decide quais são candidatos relevantes |
| `08-AGENT-ENGINE` | Pode consumir este pipeline como uma ferramenta dentro do loop de agente |

## Links que resolvem hoje

- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../11-KNOWLEDGE/01-Introducao.md`](../11-KNOWLEDGE/01-Introducao.md) — a fonte que este volume consulta
- [`../14-VECTOR/01-Introducao.md`](../14-VECTOR/01-Introducao.md) — o índice que este volume consulta

## Navegação interna

Para entender o critério central: `01-Introducao.md` seguido de `07-Regras.md`. Para o pipeline
completo: `05-Diagramas.md` (sequência) seguido de `06-Fluxogramas.md` (os dois pontos de
recusa).
