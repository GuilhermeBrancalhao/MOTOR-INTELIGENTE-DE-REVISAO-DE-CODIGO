---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-03
---

# Anti-Patterns

**Usar `AbortarDependentes` como política padrão universal "para simplificar".** Isso transforma
qualquer falha isolada em falha total do grafo, mesmo quando ramos independentes teriam sucesso
— desperdiça exatamente o trabalho que a estrutura de DAG existe para preservar (paralelismo e
independência entre ramos).

**Reexecutar dependências já resolvidas a cada retry de um nó dependente**, em vez de reusar o
resultado já obtido. Isso não só desperdiça trabalho — se a dependência não é idempotente, pode
produzir um resultado diferente a cada retry, corrompendo a suposição de que o nó dependente está
operando sobre entrada estável.

**Deixar o número de nós de um fan-out crescer sem limite superior conhecido a partir de dado de
entrada externo.** Um grafo cujo tamanho depende inteiramente de uma lista de tamanho não
controlado pode saturar o executor concorrente de forma imprevisível — o limite de concorrência
protege contra excesso de execução simultânea, mas não protege contra excesso de nós no grafo em
si.

**Tratar o resultado do grafo como booleano de sucesso/falha em código que consome este motor.**
Isso descarta a granularidade por nó que `08-Modelos.md` define deliberadamente — um consumidor
que só olha "deu certo?" perde a informação de qual ramo específico falhou, que é exatamente o
que orienta a ação de correção.

**Detectar ciclo tarde, durante a execução, em vez de na validação do grafo.** Um motor que só
percebe ciclo quando dois nós ficam mutuamente esperando um pelo outro em tempo de execução
desperdiça o tempo até o timeout ser detectado — a validação antecipada em `03-Escopo.md` e
`06-Fluxogramas.md` existe exatamente para eliminar essa classe de erro antes que custe tempo
real.
