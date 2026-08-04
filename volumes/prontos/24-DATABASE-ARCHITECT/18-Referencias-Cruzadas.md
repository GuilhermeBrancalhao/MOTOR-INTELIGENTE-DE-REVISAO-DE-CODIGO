---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de migração compatível,
proveniência, concorrência e retenção é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `14-VECTOR` | Índice vetorial e embedding; coexiste com este volume sem depender dele |
| `23-BACKEND-ARCHITECT` | Decide quando e o quê gravar; este volume define como a gravação preserva schema, proveniência e consistência |
| `25-API-ARCHITECT` | O formato exposto ao cliente pode divergir do formato de persistência interno definido aqui |
| `16-INTEGRATION` | Proveniência de conteúdo obtido de fornecedor externo se apoia na idempotência de chamada daquele volume |

## Links que resolvem hoje

- [`../23-BACKEND-ARCHITECT/07-Regras.md`](../23-BACKEND-ARCHITECT/07-Regras.md) — regras da
  orquestração que decide quando gravar
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para controle de
concorrência em detalhe: `05-Diagramas.md` seguido de `13-Testes.md`.
