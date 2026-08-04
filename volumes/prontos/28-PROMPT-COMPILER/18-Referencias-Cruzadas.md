---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: ["07"]` — este volume compila um prompt cujo contrato só existe depois da máquina de
estados descrita naquele volume; não faz sentido lido sem o conceito de prompt promovido que o 07
define.

| Volume vizinho | Relação |
|---|---|
| `07-PROMPT-ENGINE` | Define o contrato e o estado PROMOVIDO consumidos por este volume |
| `29-PROMPT-OPTIMIZER` | Propõe variante de prompt usando os casos de ouro do 07; este volume compila uma variante já definida |
| `26-AI-MODELS` | Seleciona o modelo cujo dialeto este volume usa para compilar |
| `27-LLM-ROUTER` | Roteia a chamada que consome o payload produzido por este volume |

## Links que resolvem hoje

- [`../07-PROMPT-ENGINE/07-Regras.md`](../07-PROMPT-ENGINE/07-Regras.md) — regras do contrato de
  prompt consumido por este volume
- [`../ROADMAP.md`](../ROADMAP.md) — grupo 1 (prompts: 07, 28, 29), fronteira decidida em
  2026-07-29

## Navegação interna

Para entender o mecanismo central: `01-Introducao.md` seguido de `07-Regras.md`. Para a ordem de
verificação em detalhe: `06-Fluxogramas.md` seguido de `13-Testes.md`.
