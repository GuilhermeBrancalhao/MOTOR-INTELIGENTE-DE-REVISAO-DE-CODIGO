---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de responsabilidade nomeada,
classificação de risco e trilha de auditoria é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `17-SECURITY` | Defesa técnica contra ataque; este volume trata de governança de decisão, complementar não substituta |
| `18-DEVSECOPS` | Enforça controle técnico no pipeline; este volume trata de aprovação de caso de uso, gate anterior |
| `26-AI-MODELS` | Seleção técnica de modelo; este volume trata de quem é responsável pelo caso de uso que o usa |
| `21-OBSERVABILITY` | Sinal operacional pode informar quando um caso de uso mudou de escala, motivando revisão periódica (G6) |

## Links que resolvem hoje

- [`../17-SECURITY/07-Regras.md`](../17-SECURITY/07-Regras.md) — regras de defesa técnica,
  complementares à governança organizacional deste volume
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para a matriz de
controles: `05-Diagramas.md`.
