---
volume: "39"
volume_nome: ROADMAP
tipo: PROCESSO
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de priorização, escopo e
autoridade é conceito autocontido, mesmo inspirado na prática real do `ROADMAP.md` deste acervo.

| Volume vizinho | Relação |
|---|---|
| `38-PROJECT-PLANNER` | Decompõe um objetivo já priorizado em tarefas de um ciclo; este volume decide o que entra no backlog e em que ordem |
| `35-DOCUMENTATION` | Registro de decisão arquitetural (ADR); uma decisão de autoridade sinalizada aqui pode gerar um ADR quando de fato decidida |
| `30-AI-GOVERNANCE` | Aprovação de caso de uso antes de produção; priorização de roadmap pode incluir quando um caso de uso é proposto, sem substituir a aprovação de governança |

## Links que resolvem hoje

- [`../ROADMAP.md`](../ROADMAP.md) — exemplo real e vivo deste acervo das práticas que este
  volume formaliza (seção "Fora de escopo" e "Decisão que permanece com o autor")
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para a distinção
entre horizonte comprometido e direcional: `05-Diagramas.md` seguido de `13-Testes.md`.
