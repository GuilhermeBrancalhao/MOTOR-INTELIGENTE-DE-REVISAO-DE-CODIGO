---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de especificação versionada,
código marcado e revisão obrigatória é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `28-PROMPT-COMPILER` | Compila prompt em payload para chamar modelo; este volume trata do código que a chamada produz como saída |
| `35-DOCUMENTATION` | Disciplina de conteúdo gerado nunca editado manualmente (W5), aplicada aqui especificamente a código |
| `30-AI-GOVERNANCE` | Revisão humana obrigatória para decisão de alto risco (G3); este volume trata revisão como obrigatória para todo código gerado |
| `19-DEVOPS` | Pipeline de validação (compilação, teste) que código gerado atravessa, igual a código humano |

## Links que resolvem hoje

- [`../35-DOCUMENTATION/07-Regras.md`](../35-DOCUMENTATION/07-Regras.md) — regra W5, disciplina
  de conteúdo gerado reaproveitada aqui para código
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo
completo de validação e revisão: `06-Fluxogramas.md` (o `stateDiagram-v2`).
