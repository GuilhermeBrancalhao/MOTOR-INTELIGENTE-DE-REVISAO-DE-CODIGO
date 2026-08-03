---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 07-Regras
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Regras

## Invariantes

**O grafo é validado por completo antes de qualquer nó executar.** Detecção de ciclo, referência
a nó inexistente numa aresta, e nó sem entrada declarada são erros de definição, não erros de
execução — o motor rejeita o grafo inteiro na submissão, nunca deixa metade dos nós rodarem antes
de descobrir que o grafo era inválido.

**Um nó só entra em `Pronto` quando todas as suas dependências chegam a `Sucesso`.** Não existe
execução parcial de dependência — se um nó depende de três outros, os três precisam ter sucesso,
não apenas a maioria. Falha de qualquer dependência aciona a política de falha do nó dependente,
nunca uma execução "otimista" com dependência incompleta.

**A ordem de execução entre nós paralelos (sem aresta entre si) não é garantida determinística.**
O motor garante ordem de dependência, não ordem de execução dentro do mesmo nível de
paralelismo — um chamador que precisa de ordem específica entre dois nós tem que declarar uma
aresta de dependência entre eles, não confiar em ordem observada empiricamente.

**Retry de nó nunca reexecuta dependências já resolvidas.** Um nó que falha e é tentado de novo
usa o mesmo resultado das dependências que já tiveram sucesso — reexecutar dependências a cada
retry de um nó dependente desperdiçaria trabalho e, se as dependências não forem idempotentes,
poderia produzir resultado inconsistente entre tentativas.

**Todo resultado final do grafo lista o status de cada nó individualmente**, nunca um booleano
agregado de sucesso/falha do grafo inteiro — falha parcial é um resultado de primeira classe, não
um caso degenerado tratado como falha total.

## Matriz de controles

| Controle | Risco mitigado | Como é verificado |
|---|---|---|
| Detecção de ciclo antes de qualquer execução | Deadlock de dependência circular consumindo recursos indefinidamente | Teste que submete grafo cíclico e verifica rejeição sem nenhum nó executado |
| Fan-in só libera com todas as dependências em Sucesso | Execução com dado parcial/inconsistente de agregação | Teste que falha uma de três dependências de um fan-in e verifica que o nó de agregação nunca executa |
| Resultado final sempre granular por nó | Falha parcial mascarada como sucesso ou como falha total indiferenciada | Teste que verifica presença do status de cada nó individual no resultado devolvido ao chamador |
