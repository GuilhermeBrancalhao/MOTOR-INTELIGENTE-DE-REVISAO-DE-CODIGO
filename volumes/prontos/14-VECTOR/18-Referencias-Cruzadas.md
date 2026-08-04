---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é independente de `11-KNOWLEDGE` na leitura, embora na prática
receba documento já validado por aquele; a leitura não exige ter lido `11` primeiro.

| Volume vizinho | Relação |
|---|---|
| `11-KNOWLEDGE` | Fornece documento validado para indexação; este volume nunca questiona se o documento deveria existir |
| `13-RAG` | Consome resultado de busca deste volume; depende deste volume e de 11 |
| `15-CONTEXT` | Independente — orçamento de janela vale mesmo sem índice vetorial nenhum |
| `27-LLM-ROUTER` | Decide qual modelo de embedding usar; este volume versiona e isola por modelo, não escolhe |

## Links que resolvem hoje

- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../ROADMAP.md`](../ROADMAP.md) — grupo 2 (conhecimento e contexto), fronteiras decididas em 2026-07-29

## Navegação interna

Para entender o critério central: `01-Introducao.md` seguido de `07-Regras.md`. Para a
reindexação atômica: `05-Diagramas.md` seguido de `12-Exemplos.md` (Caso 3).
