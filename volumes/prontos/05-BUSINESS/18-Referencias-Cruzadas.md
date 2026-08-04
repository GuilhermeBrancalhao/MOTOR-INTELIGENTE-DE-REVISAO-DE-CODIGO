---
volume: "05"
volume_nome: BUSINESS
tipo: PROCESSO
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: ["01"]` — este volume usa o vocabulário de procedência do `01-FUNDACAO` (origem da
resposta, decisão aberta) aplicado a objetivo de negócio, não o redefine.

| Volume vizinho | Relação |
|---|---|
| `03-DISCOVERY` | Consome o objetivo validado por este processo como ponto de partida da especificação técnica |
| `04-REQUIREMENTS` | Consome o objetivo validado como critério de sucesso que todo requisito deveria, em última instância, servir |
| `38-PROJECT-PLANNER` | Consumiria o objetivo validado para sequenciamento de entrega — integração ainda não especificada, ver `16-Roadmap.md` |
| `02-CORE` | Não consome nem é consumido por este volume — a fronteira é deliberada: este volume nunca prescreve arquitetura técnica |

## Links que resolvem hoje

- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../04-REQUIREMENTS/01-Introducao.md`](../04-REQUIREMENTS/01-Introducao.md) — o mesmo teste de falsificabilidade, aplicado uma camada abaixo

## Navegação interna

Para entender o critério central: `01-Introducao.md` seguido de `07-Regras.md`. Para aplicar o
processo: `06-Fluxogramas.md` seguido de `15-Checklist.md`.
