---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este é o primeiro volume do grupo conhecimento/contexto a ser lido; `13-RAG`
depende dele e de `14-VECTOR`, não o inverso.

| Volume vizinho | Relação |
|---|---|
| `14-VECTOR` | Recebe documento validado deste volume para indexação; não decide validade, só armazena |
| `13-RAG` | Consulta autoridade e ciclo de vida deste volume antes de incluir documento numa resposta; depende deste volume e de 14 |
| `15-CONTEXT` | Independente deste volume — orçamento de janela vale mesmo sem base de conhecimento nenhuma |
| `30-AI-GOVERNANCE` | Consultado quando documento envolve dado sensível; este volume garante que a origem está registrada para essa consulta ser possível |

## Links que resolvem hoje

- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../ROADMAP.md`](../ROADMAP.md) — grupo 2 (conhecimento e contexto), fronteiras decididas em 2026-07-29

## Navegação interna

Para entender o critério central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo de
vida em detalhe: `05-Diagramas.md` (o `stateDiagram-v2`) seguido de `06-Fluxogramas.md`.
