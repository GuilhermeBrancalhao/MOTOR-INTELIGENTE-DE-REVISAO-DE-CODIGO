---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: ["02"]` — este volume assume a fronteira determinístico/probabilístico de
`02-CORE` como vocabulário já resolvido, para poder tratar da fronteira seguinte (onde o sistema
se encaixa na empresa) sem redefinir a primeira.

| Volume vizinho | Relação |
|---|---|
| `02-CORE` | Decide a fronteira interna de um sistema; este volume decide a fronteira do sistema dentro da empresa — as duas são independentes |
| `16-INTEGRATION` | Consome achado de duplicação deste volume para decidir contrato técnico de integração entre sistemas consolidados |
| `27-LLM-ROUTER` | Decisão técnica pontual de modelo continua sendo do projeto; este volume só entra quando a escolha cria dependência de fornecedor repetida |
| `30-AI-GOVERNANCE` | Recebe sinal deste volume quando dependência cruza fronteira de governança de dado sensível |

## Links que resolvem hoje

- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../02-CORE/01-Introducao.md`](../02-CORE/01-Introducao.md) — a fronteira interna que este volume não redefine

## Navegação interna

Para entender o critério central: `01-Introducao.md` seguido de `07-Regras.md`. Para aplicar o
processo: `06-Fluxogramas.md` seguido de `15-Checklist.md`.
