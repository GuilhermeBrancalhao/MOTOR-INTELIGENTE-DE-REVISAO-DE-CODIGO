---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — chamada bem-sucedida com contrato compatível

Uma integração com um fornecedor de pagamento é chamada com chave de idempotência derivada do
número do pedido, versão mínima esperada 2.0. O fornecedor responde com versão 2.3 (compatível,
mudança apenas em `minor`), dentro do timeout configurado. A resposta é verificada e repassada ao
consumidor normalmente.

## Caso 2 — retry seguro por timeout de rede

A mesma chamada, mas a primeira tentativa expira por timeout de rede antes de resposta chegar.
A política de retry permite uma nova tentativa; a segunda chamada usa a mesma chave de
idempotência. Se a primeira tentativa de fato tinha processado o pagamento do lado do fornecedor
(a resposta só se perdeu na volta), o fornecedor reconhece a chave repetida e devolve o mesmo
resultado, sem cobrar duas vezes — a idempotência protege mesmo quando não se sabe se a primeira
tentativa teve efeito ou não.

## Caso 3 — circuito aberto após degradação sustentada

O mesmo fornecedor começa a falhar consistentemente (acima do limiar configurado de falhas
consecutivas). O circuit breaker abre, e chamadas subsequentes falham imediatamente, sem tentar
contra o fornecedor degradado — o sistema interno continua respondendo rapidamente aos próprios
consumidores, mesmo que a funcionalidade de pagamento específica esteja temporariamente
indisponível, em vez de todo o sistema ficar lento esperando timeouts repetidos.

## Caso 4 — falha de rede intermitente sem duplicação

Uma chamada de pagamento falha por timeout de rede na primeira tentativa, mas o sistema externo
de fato processou a operação — só a resposta de confirmação se perdeu no caminho de volta. A
segunda tentativa, com a mesma chave de idempotência, é reconhecida pelo sistema externo como
repetição da mesma operação, e ele devolve a confirmação original sem cobrar novamente — o
consumidor nunca sabe que houve uma falha de rede no meio do processo, só recebe a resposta
correta ao final.
