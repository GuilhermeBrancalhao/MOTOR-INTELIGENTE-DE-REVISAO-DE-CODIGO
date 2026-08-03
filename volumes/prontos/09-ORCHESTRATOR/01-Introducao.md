---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-03
---

# Introdução

Uma tarefa complexa raramente é resolvida por uma única execução de agente ou uma única chamada
de função — normalmente é decomposta em várias etapas, algumas independentes entre si e
executáveis em paralelo, outras dependentes do resultado de etapas anteriores. Sem um motor que
coordena essa decomposição, cada aplicação reimplementa a mesma lógica de "espera isso terminar
antes de começar aquilo" com código ad-hoc, que tende a esconder duas classes de bug caras:
execução fora de ordem quando uma dependência é esquecida, e trabalho duplicado ou perdido
quando uma etapa falha no meio de um grupo paralelo.

Este volume descreve o motor que resolve esse problema como um grafo acíclico dirigido (DAG) de
nós, onde cada nó é uma unidade de trabalho — que pode ser uma execução de `08-AGENT-ENGINE`, uma
chamada de função determinística, ou outro workflow inteiro tratado como nó único. O motor decide
a ordem de execução por ordenação topológica, paralisa nós sem dependência pendente entre si, e
trata falha de um nó de acordo com a política declarada para aquele nó (abortar o grafo inteiro,
pular só os dependentes, ou tentar novamente com backoff).

A fronteira com `08-AGENT-ENGINE` é direta: aquele motor executa **uma** unidade de trabalho de
agente até seu próprio encerramento; este motor decide **quando** e **em que ordem** unidades de
trabalho (de agente ou não) executam entre si. A fronteira com `10-WORKFLOW` é mais sutil: este
volume trata da mecânica genérica de grafo de dependência — não importa o que cada nó faz;
`10-WORKFLOW` trata de workflows que misturam deliberadamente etapas de IA com etapas
determinísticas como um padrão de desenho específico, consumindo este motor como sua camada de
execução.
