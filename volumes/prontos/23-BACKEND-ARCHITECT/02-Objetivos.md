---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Modelar toda operação de backend que dispara chamada de IA potencialmente longa como um trabalho
com estado explícito e consultável, nunca como uma requisição síncrona bloqueada até a resposta
chegar quando essa resposta pode exceder um timeout razoável.

Garantir que workers que processam trabalhos sejam sem estado entre requisições — qualquer worker
disponível pode processar qualquer trabalho pendente, sem afinidade implícita que tornaria a
perda de um worker específico um ponto de falha para trabalhos que só ele "sabia" processar.

Aplicar backpressure explícita quando a capacidade de processamento de IA é menor que a demanda
recebida, em vez de deixar trabalhos se acumularem sem limite em memória até o sistema ficar sem
recurso.

Garantir que o processamento de um trabalho seja idempotente — reprocessar um trabalho que já
começou a executar, por retry ou por reinício de worker, nunca duplica o efeito colateral que
esse processamento produz.

Tornar toda transição de estado de um trabalho explícita e unidirecional dentro da política de
retry declarada, e garantir que falha permanente termine num estado consultável, nunca
silenciosamente descartado da fila.

Os cinco objetivos se apoiam numa sequência de dependência: modelar o trabalho como assíncrono
(S1) é o que torna possível ter workers sem estado (S2), porque só um trabalho com identidade e
estado persistente independente de um processo específico pode ser retomado por qualquer worker.
Backpressure (S3) e idempotência (S4) protegem essa mesma estrutura de dois lados diferentes: uma
contra sobrecarga vinda de fora, a outra contra duplicação vinda de dentro do próprio mecanismo de
retry que a fila implementa.