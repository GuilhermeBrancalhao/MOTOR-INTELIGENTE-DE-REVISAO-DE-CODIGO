---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/38-project-planner/planejamento.py -->

`planejamento.py`, citado acima, formaliza Z1-Z6: `ordenar_por_dependencia` detecta ciclo
explicitamente via `DependenciaForaDeOrdem` (Z1); `PlanoDeCiclo.adicionar_tarefa` recusa
estimativa sem faixa real (Z2); `PlanoDeCiclo.__post_init__` recusa plano sem
`escopo_negociado` (Z3); `registrar_revisao` recusa `RevisaoDePlano` sem motivo (Z4);
`AndamentoDaTarefa.bloquear` exige motivo explícito, mantendo `BLOQUEADA` distinto de
`NAO_INICIADA` (Z5); `AndamentoDaTarefa.concluir` recusa transição sem `criterio_atingido=True`
(Z6).

`ordenar_por_dependencia` usa uma busca em profundidade clássica com detecção de ciclo via
conjunto de nós "em visita" — uma técnica padrão de ordenação topológica, escolhida por
simplicidade e por já ser suficientemente eficiente para o tamanho típico de um plano de ciclo de
trabalho, sem exigir uma biblioteca externa de grafo para esse propósito específico e limitado.

Para o tamanho típico de um plano real, com dezenas de tarefas, o custo computacional dessa abordagem é irrelevante frente à clareza que ela oferece na implementação.

Uma implementação real, com milhares de tarefas, provavelmente se beneficiaria de uma biblioteca
de grafo dedicada para melhor desempenho, mas o princípio central de detecção de ciclo antes de
execução permaneceria idêntico ao que este exemplo mínimo já demonstra com clareza suficiente para os
propósitos didáticos e de verificação exigidos por este volume específico deste mesmo acervo,
sem qualquer necessidade de otimização prematura que só complicaria a leitura do código de exemplo.