---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: ["26"]` — este volume roteia entre candidatos que só existem depois da seleção
descrita naquele volume; não faz sentido lido sem o conceito de candidato aprovado e fallback
declarado que o 26 define.

| Volume vizinho | Relação |
|---|---|
| `26-AI-MODELS` | Fornece a lista de candidatos aprovados e fallback declarado; este volume decide qual deles atende cada chamada |
| `34-COST-OPTIMIZATION` | Otimização de custo agregado; este volume roteia por saúde, não por preço |
| `16-INTEGRATION` | Robustez de cada chamada individual a um provedor; este volume decide qual provedor recebe a chamada |
| `21-OBSERVABILITY` | Fonte real do sinal de saúde que alimenta a detecção de degradação deste volume |

## Links que resolvem hoje

- [`../26-AI-MODELS/07-Regras.md`](../26-AI-MODELS/07-Regras.md) — regras de seleção que
  produzem os candidatos roteados aqui
- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — regra 9, volume perecível

## Navegação interna

Para entender o mecanismo central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo de
degradação e recuperação: `06-Fluxogramas.md` (o `stateDiagram-v2`).
