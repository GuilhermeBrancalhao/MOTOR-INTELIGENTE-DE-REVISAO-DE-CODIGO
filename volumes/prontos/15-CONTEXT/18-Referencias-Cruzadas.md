---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido de forma independente do resto do grupo conhecimento e
contexto; vale mesmo para sistema sem `11`, `13` ou `14` nenhum.

| Volume vizinho | Relação |
|---|---|
| `13-RAG` | Documento recuperado por aquele pipeline compete pelo mesmo orçamento deste volume, sem prioridade automática |
| `08-AGENT-ENGINE` | Trata orçamento de execução inteira (passos, tokens totais, tempo); este volume trata orçamento de uma janela específica dentro dessa execução |
| `07-PROMPT-ENGINE` | A instrução de sistema que este volume trata com prioridade máxima é tipicamente definida como prompt versionado por aquele volume |

## Links que resolvem hoje

- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../ROADMAP.md`](../ROADMAP.md) — grupo 2 (conhecimento e contexto), fronteiras decididas em 2026-07-29

## Navegação interna

Para entender o critério central: `01-Introducao.md` seguido de `07-Regras.md`. Para o gatilho de
compactação em detalhe: `05-Diagramas.md` (o `flowchart` de margem) seguido de `06-Fluxogramas.md`
(o `stateDiagram-v2` completo).
