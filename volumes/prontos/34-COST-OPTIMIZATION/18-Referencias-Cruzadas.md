---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de custo por tarefa,
atribuição, orçamento e tendência é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `26-AI-MODELS` | Comparação de custo no momento de selecionar candidato (M4); este volume trata do acompanhamento contínuo depois da seleção |
| `27-LLM-ROUTER` | Roteia por saúde, nunca por custo; este volume é onde a dimensão de custo de fato é tratada |
| `32-QUALITY` | Mesma estrutura de indicador (medição, tendência, regressão/otimização validada), dimensão de qualidade em vez de custo |
| `33-PERFORMANCE` | Mesma estrutura de indicador, dimensão de desempenho em vez de custo |

## Links que resolvem hoje

- [`../26-AI-MODELS/07-Regras.md`](../26-AI-MODELS/07-Regras.md) — regra M4, comparação de custo
  por tarefa na seleção de modelo
- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — regra 9, volume perecível

## Navegação interna

Para entender o método central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo de
orçamento e alerta: `05-Diagramas.md`.
