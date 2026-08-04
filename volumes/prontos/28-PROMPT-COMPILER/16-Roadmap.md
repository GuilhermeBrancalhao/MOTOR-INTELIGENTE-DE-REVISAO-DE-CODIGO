---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Compressão automática de prompt quando o orçamento é excedido, com estratégia declarada de o quê
comprimir primeiro (hoje o excesso de orçamento é apenas rejeitado, sem caminho de correção
automática).

Contagem de token real por dialeto/provedor específico, em vez da estimativa simplificada usada
no modelo mínimo — cada provedor tokeniza de forma ligeiramente diferente.

Cache multi-nível (mais de um ponto de cache com precedência entre eles) — hoje o modelo aceita
múltiplos pontos de cache sem modelar relação de precedência ou dependência entre eles.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (compilação com as quatro verificações em ordem, dialeto
como adaptador), testado por mutação nas seis regras. Depois, integração real com o contrato do
`07-PROMPT-ENGINE` e com um dialeto de provedor real.

## O que este volume assume que pode mudar

A estimativa simplificada de tokens (contagem de palavras) é o mínimo suficiente hoje — um
tokenizador real e específico por provedor deve substituí-la antes de uso em produção, sem
alterar o princípio central de verificação explícita contra orçamento declarado.
