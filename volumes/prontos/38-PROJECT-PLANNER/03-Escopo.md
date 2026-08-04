---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o processo de planejamento de um ciclo de trabalho: decomposição por
dependência, estimativa com incerteza, negociação de escopo, replanejamento explícito, distinção
entre bloqueio e não-início, e conclusão verificável.

**Fronteira com `39-ROADMAP`.** Backlog de longo prazo e priorização entre iniciativas
concorrentes — o que vem antes do quê, em que trimestre — é daquele volume. Este volume trata do
processo de decompor um objetivo já priorizado em tarefas executáveis dentro de um ciclo
específico, não de decidir qual objetivo merece atenção primeiro.

**Fronteira com `35-DOCUMENTATION`.** Registro de decisão arquitetural com consequência duradoura
(ADR) é daquele volume. Negociação de escopo de ciclo, aqui, é uma decisão de menor duração e
granularidade mais fina, mas segue o mesmo princípio de registro explícito antes de agir — nunca
decisão implícita reconstruída de memória depois.

**Fronteira com `32-QUALITY`.** O indicador agregado de qualidade de código é daquele volume.
Este volume trata de planejamento de trabalho, não de medição de qualidade do resultado — mas
reaproveita o mesmo princípio de "conclusão verificável, nunca presumida" que também sustenta a
disciplina de teste daquele volume.

Não cobre ferramenta específica de gestão de projeto (quadro Kanban, gráfico de Gantt) — os
princípios deste volume valem independentemente de qual ferramenta representa o plano visualmente.
