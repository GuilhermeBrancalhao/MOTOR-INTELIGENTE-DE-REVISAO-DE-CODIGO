---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de indicador agregado é
conceito autocontido, mesmo reaproveitando a tese central do 31.

| Volume vizinho | Relação |
|---|---|
| `31-TESTING` | A prática de escrever e organizar teste; este volume trata do indicador agregado que resulta dela |
| `33-PERFORMANCE` | Dimensão independente de qualidade (desempenho vs. correção verificada) |
| `18-DEVSECOPS` | Gate paralelo e independente no mesmo pipeline do 19-DEVOPS |
| `19-DEVOPS` | O pipeline onde o gate de qualidade deste volume é uma etapa, ao lado do gate de segurança |

## Links que resolvem hoje

- [`../31-TESTING/07-Regras.md`](../31-TESTING/07-Regras.md) — regras da prática de teste que
  alimenta o indicador deste volume
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o indicador central: `01-Introducao.md` seguido de `07-Regras.md`. Para o gate e a
detecção de regressão em detalhe: `05-Diagramas.md` seguido de `06-Fluxogramas.md`.
