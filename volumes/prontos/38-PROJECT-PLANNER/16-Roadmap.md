---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Recalibração automática de estimativa futura baseada no histórico real de faixas anteriores —
hoje a métrica de calibração é acompanhada, mas não alimenta automaticamente a próxima
estimativa.

Priorização dentro do plano quando capacidade de execução é menor que o total de tarefas
planejadas — hoje o modelo assume que todas as tarefas do plano serão executadas, sem mecanismo
de corte explícito quando a capacidade real é insuficiente.

Dependência entre planos de ciclos diferentes (uma tarefa deste ciclo depende de entrega de um
ciclo anterior ou futuro) — hoje o grafo de dependência é interno a um único `PlanoDeCiclo`.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (decomposição por dependência, estimativa com incerteza,
escopo negociado, revisão explícita, bloqueio distinto, conclusão verificável), testado por
mutação nas seis regras. Depois, integração real com o backlog de longo prazo do `39-ROADMAP`.

## O que este volume assume que pode mudar

O modelo de dependência simples (lista de nomes de tarefa) é o mínimo suficiente hoje — um
esquema mais expressivo (dependência parcial, dependência opcional) pode ser necessário conforme
a complexidade dos ciclos planejados cresce, sem alterar o princípio central de ordenação por
dependência real e detecção de ciclo impossível.
