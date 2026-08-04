---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de versão semântica, superfície
pública e depreciação é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `25-API-ARCHITECT` | Contrato de rede que o SDK encapsula; este volume trata da disciplina de pacote de software especificamente |
| `40-TEMPLATES` | Depreciação explícita de template (AB5); mesmo princípio aplicado aqui com risco mais imediato de quebrar código de terceiros |
| `37-CODE-GENERATION` | Validação de código antes de aceitar (Y1); reaproveitada aqui para exemplo de uso do SDK |
| `42-PLUGINS` | Extensão de terceiros sobre este sistema; SDK e plugin frequentemente compartilham a mesma disciplina de superfície pública estável |

## Links que resolvem hoje

- [`../25-API-ARCHITECT/07-Regras.md`](../25-API-ARCHITECT/07-Regras.md) — regras do contrato de
  rede que o SDK encapsula
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para o ciclo de
depreciação: `06-Fluxogramas.md` (o `stateDiagram-v2`).
