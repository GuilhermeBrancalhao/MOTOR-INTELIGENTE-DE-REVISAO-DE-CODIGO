---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o método de seleção não exige ter lido
nenhum outro volume primeiro, embora reaproveite o mecanismo de casos de ouro do 07.

| Volume vizinho | Relação |
|---|---|
| `27-LLM-ROUTER` | Recebe a lista de candidatos aprovados por este volume; decide roteamento em tempo de execução |
| `07-PROMPT-ENGINE` | Fonte do mecanismo de casos de ouro, reaproveitado aqui para avaliar modelo em vez de prompt |
| `34-COST-OPTIMIZATION` | Otimização de custo agregado ao longo do tempo; este volume trata da decisão pontual de qual modelo usar |
| `28-PROMPT-COMPILER` | Compila prompt para o dialeto do modelo selecionado por este volume |

## Links que resolvem hoje

- [`../07-PROMPT-ENGINE/07-Regras.md`](../07-PROMPT-ENGINE/07-Regras.md) — mecanismo de casos de
  ouro reaproveitado por este volume
- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — regra 9, volume perecível

## Navegação interna

Para entender o método central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo de
vida de um candidato: `06-Fluxogramas.md` (o `stateDiagram-v2`).
