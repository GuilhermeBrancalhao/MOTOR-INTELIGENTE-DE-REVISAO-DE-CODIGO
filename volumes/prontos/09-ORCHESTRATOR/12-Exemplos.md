---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-03
---

# Exemplos

## Caso 1 — fan-out de três buscas paralelas com fan-in de agregação

Um grafo com um nó inicial que dispara três nós de busca independentes (por exemplo, três fontes
de dados diferentes para o mesmo tipo de informação), seguidos de um nó de agregação que só
executa depois que as três buscas terminam. Se as três têm sucesso, o nó de agregação recebe as
três saídas e produz o resultado combinado — o grafo termina com todos os nós em `Sucesso`. O
tempo total de execução é limitado pela busca mais lenta, não pela soma das três, porque
executam em paralelo.

## Caso 2 — falha parcial com política mista

O mesmo grafo do caso 1, mas uma das três buscas falha de forma não recuperável, e sua política é
`AbortarDependentes`. O nó de agregação, que depende das três, nunca executa — transita para
`Abortado`. As outras duas buscas, que não dependem da que falhou e não têm dependente em comum
além do nó de agregação já abortado, permanecem em `Sucesso`. O resultado final do grafo lista:
duas buscas com `Sucesso`, uma com `FalhaDefinitiva`, o nó de agregação com `Abortado` — o
chamador recebe informação suficiente para decidir se tenta reexecutar só o ramo que falhou (sem
repetir as duas buscas que já tiveram sucesso) ou trata o resultado parcial como insuficiente.

## Caso 3 — retry com backoff resolvendo falha transitória

Um nó de chamada a um serviço externo falha com erro marcado recuperável (timeout). A política é
`RetryComBackoff(tentativas=3, backoff_inicial_s=2, fator=2)`. Primeira tentativa falha, motor
espera 2s e tenta de novo; segunda tentativa falha, motor espera 4s; terceira tentativa tem
sucesso. O nó termina em `Sucesso`, e a trilha registra as duas falhas intermediárias com seus
motivos — informação que, agregada ao longo de várias execuções do mesmo grafo, alimenta a
métrica de taxa de recuperação por retry descrita em `14-Metricas.md`.
