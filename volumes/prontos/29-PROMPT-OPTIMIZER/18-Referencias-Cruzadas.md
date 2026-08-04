---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: ["07"]` — este volume propõe variante usando os casos de ouro definidos naquele
volume como função objetivo; não faz sentido lido sem o conceito de caso de ouro e estado
PROMOVIDO que o 07 define.

| Volume vizinho | Relação |
|---|---|
| `07-PROMPT-ENGINE` | Fonte dos casos de ouro usados como função objetivo; único lugar onde uma proposta deste volume pode ser promovida |
| `28-PROMPT-COMPILER` | Compila a versão promovida em payload real; nunca compila a proposta diretamente deste volume |
| `26-AI-MODELS` | Avaliação de candidato pode envolver chamada a modelo selecionado por aquele volume |
| `31-TESTING` | Prova por mutação e disciplina de teste reaproveitadas aqui seguem a mesma prática daquele volume |

## Links que resolvem hoje

- [`../07-PROMPT-ENGINE/07-Regras.md`](../07-PROMPT-ENGINE/07-Regras.md) — regras do contrato de
  prompt e casos de ouro reaproveitados como função objetivo
- [`../ROADMAP.md`](../ROADMAP.md) — grupo 1 (prompts: 07, 28, 29), fronteira decidida em
  2026-07-29

## Navegação interna

Para entender o mecanismo central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo de
vida de uma proposta: `06-Fluxogramas.md` (o `stateDiagram-v2`).
