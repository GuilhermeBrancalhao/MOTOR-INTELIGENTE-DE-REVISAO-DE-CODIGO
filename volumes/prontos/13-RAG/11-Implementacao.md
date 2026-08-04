---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/13-rag/pipeline.py -->

`pipeline.py`, citado acima, formaliza R1-R6: `reordenar` produz `score_relevancia` distinto de
`score_proximidade` (R3); `confirmar_validade` roda depois da reordenação, nunca antes (R6);
`compor_resposta` recusa explicitamente quando não há candidato válido suficiente (R4); toda
`Citacao` carrega `valido_no_momento_da_citacao` calculado no momento da consulta, não herdado.

## Como o motor real aplicaria isto

A implementação mínima trata os quatro passos (recuperar, reordenar, confirmar validade, medir
fidelidade) como funções puras encadeadas, cada uma testável isoladamente com entrada fake das
anteriores — não é preciso um índice vetorial real nem um modelo de geração real para testar a
lógica de reordenação ou a lógica de medição de fidelidade, só a entrada e saída esperadas de
cada etapa.

## Onde a integração com outros volumes acontece

A consulta a `14-VECTOR` acontece na etapa de recuperação, recebendo `ResultadoBusca` daquele
volume e traduzindo para `Candidato` deste. A consulta a `11-KNOWLEDGE` acontece na etapa de
confirmação de validade, chamando `consultar_valido` daquele volume para cada candidato
sobrevivente da reordenação — nunca antes, pelos motivos descritos em `06-Fluxogramas.md`.

A ordem de implementação recomendada é: `Candidato`, `Citacao` e `RespostaComFidelidade` primeiro,
como estruturas de dado puras. `reordenar` e `confirmar_validade` depois, cada uma testável com
entrada fake das etapas anteriores. `medir_fidelidade` por último, porque depende de um extrator
de afirmações que pode evoluir independentemente do resto do pipeline sem quebrar as etapas
anteriores.
