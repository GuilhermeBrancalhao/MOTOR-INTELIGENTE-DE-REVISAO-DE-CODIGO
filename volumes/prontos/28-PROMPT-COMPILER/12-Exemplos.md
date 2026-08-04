---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — compilação bem-sucedida

Um prompt PROMOVIDO, com todas as variáveis fornecidas, dialeto válido e payload dentro do
orçamento, compila normalmente e retorna `PayloadCompilado` com `hash_origem` rastreável ao
prompt.

## Caso 2 — prompt em rascunho é rejeitado

O mesmo prompt, mas ainda no estado `RASCUNHO` (não promovido pelo 07), é rejeitado antes de
qualquer outra verificação acontecer.

## Caso 3 — variável ausente é rejeitada antes da renderização

Uma variável declarada no contrato do prompt não é fornecida na chamada de compilação — a
rejeição acontece antes de o corpo ser renderizado, nunca depois com um valor vazio silencioso.

## Caso 4 — orçamento excedido é rejeitado após renderização

Um prompt com corpo muito longo, mesmo com todas as variáveis corretas, produz payload que excede
o orçamento declarado — a rejeição acontece depois da renderização completa, com o número exato
de tokens estimados disponível no erro.

## Caso 5 — dois dialetos produzem formatações diferentes do mesmo prompt

O mesmo `PromptPromovido` e as mesmas variáveis, compilados com dois `Dialeto` diferentes,
produzem `mensagens` estruturadas de forma diferente — a lógica central de `compilar` não muda,
apenas o adaptador de dialeto injetado.


Os cinco casos, em conjunto, cobrem as quatro rejeições possíveis (prompt não promovido, variável
ausente, orçamento excedido, cache inválido) mais o caso de sucesso com dois dialetos diferentes,
formando a cobertura completa que os testes da seção seguinte verificam individualmente.

Essa cobertura deliberada, caso a caso, é o que permite a qualquer pessoa validar rapidamente que uma mudança futura no compilador não quebrou nenhuma das quatro garantias centrais.