---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Uma requisição de backend que dispara uma chamada de IA tem uma característica que uma requisição
CRUD tradicional raramente tem: a duração é variável e pode facilmente exceder o timeout normal de
uma requisição HTTP síncrona. Tratar essa chamada como se fosse instantânea — bloquear a
requisição até a IA responder — funciona até o momento em que não funciona: um pico de latência do
provedor, uma fila de processamento maior que o normal, e a requisição expira antes da resposta
chegar, mesmo que o trabalho em si estivesse progredindo normalmente por trás.

Este volume trata da camada de lógica de negócio e orquestração dentro do mesmo produto — como o
backend modela um trabalho que pode levar segundos ou minutos, como múltiplos workers processam
esses trabalhos sem depender de estado exclusivo de um worker específico, e o que acontece quando
a demanda por processamento de IA excede a capacidade disponível.

`24-DATABASE-ARCHITECT` trata de onde e como o dado persiste; `25-API-ARCHITECT` trata do
contrato exposto ao cliente; `16-INTEGRATION` trata da robustez da chamada externa em si. Este
volume trata da camada que fica entre os três: a lógica que decide como um trabalho é
enfileirado, processado, e o que acontece quando ele falha ou quando não há capacidade
disponível para processá-lo agora.
