---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-04
---

# Referências Cruzadas

## Vizinhança e pré-requisito

`depende_de: []` — este volume é lido independentemente; a relação com o 16 é lateral (fronteira
de produto), não pré-requisito de leitura.

| Volume vizinho | Relação |
|---|---|
| `16-INTEGRATION` | A robustez da chamada que cruza a fronteira do produto é daquele volume; este trata do que a interface faz com o resultado |
| `23-BACKEND-ARCHITECT` | Onde e como o dado persiste no servidor; este volume trata apenas do lado do cliente |
| `25-API-ARCHITECT` | O contrato entre frontend e backend; este volume assume que ele existe e reage à variabilidade de resposta de IA dentro dele |
| `27-LLM-ROUTER` | A escolha de provedor/modelo que produz a resposta; este volume garante que a interface não depende do formato específico dessa escolha |

## Links que resolvem hoje

- [`../16-INTEGRATION/07-Regras.md`](../16-INTEGRATION/07-Regras.md) — regras da chamada que
  cruza a fronteira do produto
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a
  este volume

## Navegação interna

Para entender o ciclo de vida central: `01-Introducao.md` seguido de `07-Regras.md`. Para o
cancelamento em detalhe: `06-Fluxogramas.md` seguido de `13-Testes.md`.
