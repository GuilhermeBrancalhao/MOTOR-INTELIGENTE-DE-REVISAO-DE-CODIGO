---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`PlanoDeCiclo.__post_init__` recusa criação sem `escopo_negociado` preenchido — nenhum ciclo de
planejamento começa a existir sem que o escopo já tenha sido negociado e registrado.

`PlanoDeCiclo.adicionar_tarefa` recusa uma `Tarefa` sem `criterio_de_pronto` declarado, e recusa
uma estimativa sem incerteza real (`estimativa_min_dias` igual a `estimativa_max_dias`) — as duas
verificações acontecem no momento de adicionar a tarefa ao plano, antes de qualquer execução
começar.

`ordenar_por_dependencia` implementa ordenação topológica simples sobre o grafo de dependência
declarado em cada `Tarefa.depende_de`, detectando ciclo de dependência explicitamente em vez de
produzir uma ordem inválida silenciosamente.

`AndamentoDaTarefa.bloquear` exige motivo explícito antes de transicionar para o estado
`BLOQUEADA` — distinto de `NAO_INICIADA`, porque as duas exigem ação completamente diferente de
quem gerencia o plano. `AndamentoDaTarefa.concluir` recusa transição para `CONCLUIDA` sem
confirmação explícita de que o critério de pronto da tarefa foi atingido.


Cada uma dessas quatro verificações acontece no momento da operação correspondente — adicionar
tarefa, criar plano, registrar revisão, transicionar estado — nunca como validação posterior
opcional que poderia ser esquecida sob pressão de prazo apertado no meio de um ciclo real de
trabalho.

Essa disciplina de verificação imediata, em vez de posterior, segue o mesmo padrão já estabelecido consistentemente em outros volumes de processo deste acervo.

Isso também simplifica testar cada verificação isoladamente, sem precisar simular um ciclo completo de planejamento apenas para exercitar uma única regra específica.