---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Estado de "cancelado" ou "pausado" para um trabalho ainda em andamento (hoje o modelo só cobre o
ciclo enfileirado-executando-concluído/falho, sem um caminho explícito para o cliente desistir de
um trabalho já em processamento).

Priorização entre trabalhos na fila (hoje `retirar_proximo` pega o próximo disponível em ordem
simples, sem modelar prioridade por tipo de trabalho ou por cliente).

Backpressure adaptativa que ajusta `limite_concorrente` automaticamente com base em sinal de
capacidade real observada, em vez de um valor configurado estaticamente.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (trabalho com estado, fila com backpressure e
idempotência), testado por mutação nas seis regras. Depois, integração real com o contrato de
consulta de status do `25-API-ARCHITECT`.

## O que este volume assume que pode mudar

O modelo de retry com contagem simples de tentativas é o mínimo suficiente hoje — uma política
mais sofisticada (backoff exponencial entre tentativas, categorização de erro retryable vs. não
retryable) pode ser necessária conforme a variedade de falhas observadas cresce, sem alterar o
princípio central de transição explícita e estado terminal consultável.
