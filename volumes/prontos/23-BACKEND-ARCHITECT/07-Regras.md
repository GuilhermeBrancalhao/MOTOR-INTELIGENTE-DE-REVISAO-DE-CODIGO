---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**S1 — Operação que dispara chamada de IA potencialmente longa é modelada como trabalho com
estado explícito e consultável, nunca como requisição síncrona bloqueada até a resposta.**
*Consequência:* a duração real do processamento de IA nunca fica limitada pelo timeout de uma
requisição HTTP síncrona.

**S2 — Worker que processa trabalho é sem estado entre requisições; qualquer worker disponível
pode processar qualquer trabalho pendente.** *Consequência:* a perda de um worker específico
nunca é ponto único de falha para um trabalho que só ele "conhecia".

**S3 — Quando a capacidade de processamento é menor que a demanda, backpressure é aplicada
explicitamente.** *Consequência:* trabalhos não se acumulam sem limite até o sistema ficar sem
recurso — o limite é uma decisão de design, não uma consequência acidental de esgotamento.

**S4 — Trabalho com a mesma chave de idempotência, já em andamento ou concluído, nunca é
duplicado por uma nova solicitação.** *Consequência:* uma requisição repetida (retry de cliente,
por exemplo) nunca produz dois trabalhos processando o mesmo efeito colateral em paralelo.

**S5 — Transição de estado de trabalho é explícita e segue a política de retry declarada; nunca
acontece fora de uma operação nomeada da fila.** *Consequência:* o estado de um trabalho nunca
muda de forma que não possa ser rastreada a uma operação específica e testável.

**S6 — Trabalho que esgota as tentativas de retry termina em estado permanente consultável,
nunca é descartado silenciosamente.** *Consequência:* falha permanente é sempre encontrável por
quem precisa investigar ou tratar manualmente, em vez de desaparecer sem deixar rastro.
