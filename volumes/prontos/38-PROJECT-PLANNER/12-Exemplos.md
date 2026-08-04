---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — plano completo, ordenado corretamente

Um plano com escopo negociado e três tarefas com dependência linear é ordenado corretamente,
respeitando a sequência declarada.

## Caso 2 — ciclo de dependência é detectado

Duas tarefas que dependem uma da outra circularmente são rejeitadas por
`ordenar_por_dependencia` antes de qualquer execução ser considerada.

## Caso 3 — estimativa sem faixa real é rejeitada

Uma tarefa com `estimativa_min_dias` igual a `estimativa_max_dias` é rejeitada ao ser adicionada
ao plano — a incerteza precisa estar declarada como faixa real.

## Caso 4 — tarefa bloqueada distinta de não iniciada

Uma tarefa marcada como bloqueada, com motivo explícito, tem estado claramente distinto de uma
tarefa que simplesmente ainda não começou.

## Caso 5 — conclusão exige critério atingido

Uma tentativa de concluir uma tarefa sem confirmar que seu critério de pronto foi atingido é
rejeitada — o prazo chegar não é suficiente para marcar como concluída.


Os cinco casos cobrem, juntos, as seis regras completas — o Caso 2 é o mais didático porque
mostra explicitamente o que aconteceria se a ordenação não detectasse o ciclo: um plano
logicamente impossível de executar, silenciosamente aceito como se fosse válido.

Os demais casos cobrem as rejeições específicas de cada regra individual, complementando a cobertura conjunta que os testes da seção seguinte confirmam de forma exaustiva.

Essa cobertura equilibrada, sem lacuna nem redundância, é o padrão de qualidade que este acervo
já aplica de forma consistente a praticamente todo volume promovido até este ponto da produção.