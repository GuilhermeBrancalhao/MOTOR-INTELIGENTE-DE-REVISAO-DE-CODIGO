---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

O componente central é `Trabalho` — representa uma unidade de processamento potencialmente longa,
com estado explícito (`EstadoDoTrabalho`), contagem de tentativas, e uma chave de idempotência que
o identifica de forma estável através de reenfileiramentos. `FilaDeTrabalhos` é o único ponto que
gerencia transição de estado e a política de retry — nenhum trabalho muda de estado fora dessa
camada, o que torna cada transição auditável e testável isoladamente.

`retirar_proximo` não recebe identificador de worker como parâmetro — deliberadamente, porque
qualquer chamada a esse método deveria poder retirar qualquer trabalho disponível, sem afinidade
implícita entre worker e trabalho. Essa ausência de parâmetro é a garantia estrutural de que
nenhum worker específico é ponto único de falha para um trabalho que só ele conhece.

`enfileirar` verifica a chave de idempotência antes de aceitar um trabalho novo — um trabalho já
em andamento ou concluído com a mesma chave é retornado em vez de duplicado, o que garante que
uma requisição repetida (por retry de cliente, por exemplo) não produz dois trabalhos processando
o mesmo efeito colateral em paralelo.

`marcar_falha` implementa a política de retry: incrementa tentativas e reenfileira até o limite
configurado, e só então transiciona para o estado terminal `FALHOU_PERMANENTEMENTE` — um estado
que permanece consultável, nunca removido da estrutura de dados.
