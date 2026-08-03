---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 02-Objetivos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Modelar uma tarefa complexa como DAG de nós e arestas de dependência**, identificando quais
nós podem executar em paralelo (sem aresta entre si, direta ou transitiva) e quais precisam
esperar o resultado de outro nó.

**Explicar por que o grafo precisa ser acíclico** e o que acontece se um ciclo for introduzido
por engano — o motor precisa detectar o ciclo antes de iniciar qualquer execução, porque um
grafo cíclico não tem ordenação topológica válida.

**Descrever fan-out e fan-in de forma precisa**: fan-out é um nó que produz múltiplos nós
dependentes independentes entre si (dispara N execuções paralelas); fan-in é um nó que só
executa depois que todos os seus predecessores terminam (agrega N resultados em um).

**Aplicar uma política de falha por nó**, escolhendo entre abortar o grafo inteiro, pular apenas
os nós que dependem do nó falho (deixando ramos independentes continuarem), ou tentar novamente
com backoff — e explicar o custo de cada escolha em termos de trabalho desperdiçado versus
tempo total.

**Diferenciar retry de nó de retry de grafo inteiro**: retry de nó tenta de novo a mesma unidade
de trabalho; retry de grafo (menos comum, mais caro) reexecuta desde o início, incluindo nós que
já tinham sucesso — decisão que só faz sentido quando o estado entre nós não é idempotente.

**Traçar a fronteira com `08-AGENT-ENGINE` e `10-WORKFLOW`** de forma concreta, sem depender de
memorização: este volume não sabe o que um nó faz por dentro, só como nós se relacionam entre si.
