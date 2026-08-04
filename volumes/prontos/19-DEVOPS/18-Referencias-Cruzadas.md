---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; a sequência de estágios que define é
conceito autocontido, mesmo que o estágio de segurança referencie o 18 para detalhe.

| Volume vizinho | Relação |
|---|---|
| `18-DEVSECOPS` | O gate de segurança é uma etapa deste pipeline, na posição que a ordem de estágios determina |
| `20-CLOUD` | A infraestrutura que hospeda o sistema em execução; este volume trata de como uma mudança chega até ela |
| `21-OBSERVABILITY` | Sinal de degradação frequentemente motiva a decisão de reverter; este volume define o mecanismo de reversão em si |
| `32-QUALITY` | Política de quando um deploy exige aprovação humana é daquele volume, não deste |

## Links que resolvem hoje

- [`../18-DEVSECOPS/07-Regras.md`](../18-DEVSECOPS/07-Regras.md) — regras do gate executado no
  estágio de segurança
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender a sequência central: `01-Introducao.md` seguido de `07-Regras.md`. Para a
imutabilidade do artefato em detalhe: `04-Arquitetura.md` seguido de `13-Testes.md`.
