---
volume: "09"
volume_nome: ORCHESTRATOR
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
| `08-AGENT-ENGINE` | Um nó deste grafo pode ser uma execução daquele motor; este motor não sabe o que acontece dentro do nó |
| `10-WORKFLOW` | Consome a mecânica de DAG deste motor, adicionando semântica de "quando uma etapa é IA e quando não é" |
| `01-FUNDACAO/11-Implementacao.md` | Descreve o mesmo algoritmo de detecção de ciclo aplicado a `depende_de` entre volumes — mesma técnica, domínio diferente |
| `19-DEVOPS` / `20-CLOUD` | Tratam persistência do estado do grafo entre reinícios, quando aplicável — fora do contrato deste volume |

## Links que resolvem hoje

- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — contrato deste acervo
- [`../01-FUNDACAO/07-Regras.md`](../01-FUNDACAO/07-Regras.md) — Definição de PRONTO aplicada a este volume
- [`../ROADMAP.md`](../ROADMAP.md) — decisão de escopo do ciclo atual

## Navegação interna

Para entender o contrato do grafo: `04-Arquitetura.md` seguido de `05-Diagramas.md` (sequência e
fan-out/fan-in) e `06-Fluxogramas.md` (estados por nó). Para implementar: `08-Modelos.md`
primeiro, depois `11-Implementacao.md`, que descreve a ordem recomendada de construção.
