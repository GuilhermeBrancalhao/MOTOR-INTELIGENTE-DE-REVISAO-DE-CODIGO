---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a camada de lógica de negócio e orquestração de trabalho dentro do mesmo
produto: modelagem de trabalho assíncrono, workers sem estado, backpressure, idempotência de
processamento, e ciclo de vida de estado do trabalho.

**Fronteira com `24-DATABASE-ARCHITECT`.** Onde e como o estado de um trabalho é persistido — em
qual tipo de armazenamento, com qual estratégia de consistência — é daquele volume. Este volume
define o modelo lógico do trabalho e suas transições de estado, independente de qual tecnologia
de persistência as implementa por baixo.

**Fronteira com `25-API-ARCHITECT`.** O contrato que expõe o status de um trabalho ao cliente —
formato de resposta, endpoint de consulta — é daquele volume. Este volume garante que existe um
estado consultável para expor; a forma exata de expô-lo é decisão do 25.

**Fronteira com `16-INTEGRATION`.** A robustez da chamada de IA em si — versionamento de
contrato, idempotência da chamada externa específica, circuit breaker — é daquele volume. Este
volume trata da idempotência do trabalho de backend como um todo, que pode envolver uma ou mais
chamadas do tipo que o 16 descreve, mas não redefine a robustez de cada chamada individual.

Não cobre escolha de tecnologia de fila de mensagens nem de runtime de execução assíncrona — os
princípios deste volume (trabalho com estado explícito, worker sem estado, backpressure,
idempotência) valem independentemente da tecnologia escolhida para implementá-los.
