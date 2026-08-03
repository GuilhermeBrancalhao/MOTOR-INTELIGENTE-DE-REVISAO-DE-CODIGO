---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: PRONTO
atualizado_em: 2026-08-03
---

# Referências Cruzadas

## Vizinhança de assunto

`depende_de` está vazio de propósito — a fronteira com os volumes abaixo é lateral, não
pré-requisito de leitura.

| Volume vizinho | Relação |
|---|---|
| `09-ORCHESTRATOR` | Fronteira central deste volume: sequência declarada com início e fim (workflow) versus coordenação de agentes sem sequência fixa a priori (orquestração); um passo de workflow pode conter um grafo de `09` internamente |
| `08-AGENT-ENGINE` | Um passo de IA que invoca agente delega a execução para aquele motor; este volume só valida a saída, não conhece o loop interno |
| `19-DEVOPS` / `20-CLOUD` | Tratam onde o checkpoint é armazenado fisicamente; este volume define o contrato do checkpoint, não sua infraestrutura de persistência |

## Links que resolvem hoje

- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — contrato deste acervo
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../09-ORCHESTRATOR/08-Modelos.md`](../09-ORCHESTRATOR/08-Modelos.md) — o conceito de grafo de dependência reaproveitado por este volume para ramificação condicional

## Navegação interna

Para entender o contrato do checkpoint: `04-Arquitetura.md` seguido de `08-Modelos.md`. Para a
fronteira com orquestração, que é a confusão mais comum de terminologia fora deste acervo:
`01-Introducao.md` (que já detalha a distinção) seguido desta seção.
