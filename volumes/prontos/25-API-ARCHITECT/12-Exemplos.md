---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — campo declarado e depois redeclarado com o mesmo tipo

Um endpoint declara o campo `status` como `str`. Uma redeclaração posterior, ainda como `str`, é
aceita normalmente — não há mudança de significado nem de tipo.

## Caso 2 — mudança de tipo do mesmo campo é rejeitada

A mesma redeclaração, mas agora com tipo `int`, é rejeitada — mudar o tipo de um campo já exposto
sob a mesma versão quebraria qualquer cliente que já espera o tipo anterior.

## Caso 3 — tradução nunca vaza campo interno

Um registro interno contém `versao_do_registro` e `chave_idempotencia`, campos de controle que
nunca deveriam ser visíveis ao cliente. `traduzir_para_resposta`, chamada apenas com os campos
permitidos (`id`, `conteudo`), produz uma resposta que não contém nenhum dos dois campos internos,
independente de eles existirem no registro de origem.

## Caso 4 — status de trabalho consultável em qualquer estado

Um trabalho em estado ENFILEIRADO e outro em estado FALHOU_PERMANENTEMENTE produzem, ambos, um
`RecursoDeStatusDeTrabalho` com a mesma estrutura — o cliente consulta da mesma forma
independente de o trabalho ainda estar em andamento ou já ter terminado, de um jeito ou de outro.

## Caso 5 — endpoint síncrono sem orçamento é rejeitado

Uma tentativa de declarar um endpoint síncrono sem `limite_ms` falha explicitamente — nenhum
endpoint entra em uso sem uma expectativa de latência declarada.


Os cinco casos cobrem, juntos, as seis regras completas — os Casos 1 e 2 formam um par que prova
T1/T5 nos dois sentidos (aceitar redeclaração idêntica, rejeitar mudança de tipo), enquanto os
Casos 3 a 5 cobrem tradução, status consultável e orçamento de latência isoladamente.