---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — controle automatizado, verificação passa

O controle "isolamento de dado processado e instrução" (do 17) tem check automatizado
correspondente. A verificação passa para o commit em avaliação. O gate aprova sem exceção.

## Caso 2 — falha com waiver ativo

O controle "lista de destinos autorizados" falha porque uma nova integração ainda não foi
adicionada à lista. Existe um waiver nomeado ("aguardando revisão de destino, ticket SEC-142"),
com expiração em sete dias. O gate registra a exceção e permite que a mudança prossiga, com o
waiver visível no resultado.

## Caso 3 — waiver expirado, gate volta a bloquear

O mesmo waiver do Caso 2, mas a data atual já passou dos sete dias. O controle continua falhando
(a lista de destinos ainda não foi atualizada). O gate trata o waiver como inexistente e bloqueia
a mudança — sem que ninguém precise revogar o waiver manualmente para isso acontecer.

## Caso 4 — controle sem verificação automatizada

Um controle novo foi declarado no 17 ("nenhuma categoria de comando de shell classificada como
livre"), mas ainda não tem identificador de verificação neste processo. O gate reporta essa
ausência como lacuna explícita, distinta de um controle que passou — sinalizando que a automação
ainda precisa ser escrita, em vez de presumir cobertura que não existe.

Os quatro casos cobrem as três saídas possíveis para um controle avaliado (aprovado, bloqueado,
lacuna) mais a transição de estado do waiver entre ativo e expirado — juntos, formam a matriz
completa de comportamento que os testes da seção seguinte verificam individualmente.