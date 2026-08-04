---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

## Estratégia

Testar este pipeline exige simular os dois pontos de recusa do fluxograma (`06-Fluxogramas`)
separadamente — recusa por falta de fonte e recusa por fidelidade insuficiente — porque são
causas distintas que a suíte precisa distinguir, não apenas confirmar que "algo foi recusado".

## O que a suíte precisa cobrir

Ordem de reordenação: um teste com candidatos de proximidade e relevância divergentes,
confirmando que o resultado final segue relevância, não proximidade (R3). Revalidação: um teste
que confirma validade de documento no momento da consulta, não no momento da indexação simulada
anteriormente (R6). Recusa por fonte insuficiente: um teste com zero candidato válido após
confirmação, verificando recusa explícita com motivo (R4). Medição de fidelidade: um teste que
injeta afirmação não sustentada por nenhuma citação e confirma que a fidelidade calculada reflete
isso proporcionalmente, não como 0 ou 1 absolutos quando o suporte é parcial.

## Prova por mutação

Um teste forte para R6 é um que falha se `confirmar_validade` for removido do pipeline — um
documento expirado entre indexação e consulta seria citado como se ainda fosse válido, e o teste
que simula exatamente essa expiração no meio do fluxo capturaria a regressão.

## Testes de integração com volumes vizinhos

Um teste relevante verifica que a tradução de `ResultadoBusca` de `14-VECTOR` para `Candidato`
deste volume preserva o `score` original como `score_proximidade`, sem perda nem confusão com
`score_relevancia`, que só existe depois da reordenação.
