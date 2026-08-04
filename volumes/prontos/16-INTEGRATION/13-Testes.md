---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

## Estratégia

Testar este gateway exige simular falha do sistema externo explicitamente — timeout, resposta
incompatível, degradação sustentada — não só o caminho de chamada bem-sucedida com contrato
compatível.

## O que a suíte precisa cobrir

Verificação de versão: um teste com resposta de `major` incompatível, confirmando rejeição
explícita (I1). Idempotência: um teste que chama duas vezes com a mesma chave e confirma que o
efeito colateral simulado só acontece uma vez (I2). Circuit breaker: um teste que simula falhas
consecutivas até o limiar e confirma que chamadas subsequentes falham imediatamente, sem tentar
contra o sistema externo simulado (I4). Retry: um teste que simula timeout na primeira tentativa
e sucesso na segunda, confirmando que a mesma chave de idempotência é usada nas duas.

## Prova por mutação

Um teste forte para I2 é um que falha se a geração de chave de idempotência for trocada para
incluir timestamp — a mutação faria cada retry gerar chave nova, e o teste que conta quantas
vezes o efeito colateral simulado foi de fato aplicado (esperado: uma vez, mesmo com retry)
capturaria isso.

## Testes de integração com volumes vizinhos

Um teste relevante verifica que uma integração de exemplo com `27-LLM-ROUTER` (chamada a provedor
de modelo) aplica a mesma disciplina de timeout e circuit breaker deste volume, sem que o volume
de roteamento precise reimplementar essa lógica de robustez por conta própria.
