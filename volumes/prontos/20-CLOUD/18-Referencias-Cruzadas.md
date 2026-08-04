---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; o modelo de recurso declarado,
redundância e drift é conceito autocontido.

| Volume vizinho | Relação |
|---|---|
| `19-DEVOPS` | O pipeline implanta artefato sobre a infraestrutura que este volume declara; aquele é o caminho, este é o destino |
| `06-ENTERPRISE-ARCHITECTURE` | Consome custo e concentração de recurso deste volume para decisão de portfólio sobre fornecedor |
| `18-DEVSECOPS` / `17-SECURITY` | Política de acesso e segredo em si é daqueles volumes; este garante que segredo nunca é declarado em texto plano na configuração |
| `21-OBSERVABILITY` | Sinal de saúde de um recurso complementa a verificação estrutural de redundância deste volume |

## Links que resolvem hoje

- [`../19-DEVOPS/07-Regras.md`](../19-DEVOPS/07-Regras.md) — regras do pipeline que implanta
  sobre esta infraestrutura
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o modelo central: `01-Introducao.md` seguido de `07-Regras.md`. Para a detecção de
divergência em detalhe: `06-Fluxogramas.md` seguido de `13-Testes.md`.
