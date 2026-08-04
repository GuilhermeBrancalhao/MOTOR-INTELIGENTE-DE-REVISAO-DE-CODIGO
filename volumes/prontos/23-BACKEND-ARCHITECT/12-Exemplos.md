---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — trabalho enfileirado e processado com sucesso

Um trabalho é enfileirado, um worker o retira (transição para EXECUTANDO), processa, e é marcado
como concluído com o resultado. O cliente pôde consultar o estado a qualquer momento durante o
processamento, sem bloquear.

## Caso 2 — solicitação repetida não duplica trabalho

O mesmo trabalho é enfileirado uma segunda vez com a mesma chave de idempotência, antes de o
primeiro terminar. `enfileirar` retorna a instância existente em vez de criar uma nova — apenas
um trabalho é de fato processado.

## Caso 3 — falha com retry disponível

O trabalho falha durante o processamento, mas ainda não esgotou as tentativas. Ele volta para o
estado ENFILEIRADO, elegível para ser retirado por qualquer worker disponível na próxima
iteração — não necessariamente o mesmo que falhou.

## Caso 4 — falha permanente após esgotar tentativas

O mesmo trabalho falha repetidamente até esgotar `max_tentativas`. Ele transiciona para
FALHOU_PERMANENTEMENTE — um estado terminal que continua consultável, nunca removido da fila.

## Caso 5 — backpressure rejeita nova retirada quando o limite é atingido

Com `limite_concorrente` já atingido por trabalhos em EXECUTANDO, uma nova tentativa de
`retirar_proximo` é rejeitada explicitamente, em vez de permitir que mais trabalhos comecem a
processar do que a capacidade declarada suporta.


Os cinco casos cobrem, juntos, o ciclo de vida completo de um trabalho — do enfileiramento bem
sucedido até os três desvios que mais diferenciam uma fila de trabalho robusta de uma que só
funciona sob condição ideal: solicitação duplicada, falha recuperável, e falha permanente.