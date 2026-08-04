---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de decomposição, estimativa e
plano é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `39-ROADMAP` | Backlog de longo prazo e priorização entre iniciativas; este volume decompõe um objetivo já priorizado em tarefas executáveis |
| `35-DOCUMENTATION` | Registro de decisão arquitetural (ADR); este volume aplica o mesmo princípio de registro explícito à negociação de escopo de ciclo |
| `32-QUALITY` | Reaproveita o princípio de conclusão verificável, nunca presumida, aplicado aqui a tarefa em vez de a regra de código |
| `30-AI-GOVERNANCE` | Trilha de auditoria de decisão automatizada; este volume trata de rastreabilidade de decisão de planejamento, um domínio relacionado |

## Links que resolvem hoje

- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO, a mesma
  disciplina de conclusão verificável que este volume aplica a tarefa
- [`../35-DOCUMENTATION/07-Regras.md`](../35-DOCUMENTATION/07-Regras.md) — regra W1, registro de
  decisão com contexto explícito, princípio reaproveitado para negociação de escopo

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para a distinção
entre bloqueio e não-início: `06-Fluxogramas.md` seguido de `13-Testes.md`.
