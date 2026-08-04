---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — candidato aprovado após avaliação acima do limiar

Um candidato atende o requisito de capacidade e tem `ResultadoDeAvaliacao` com 92% de casos de
ouro aprovados, acima do limiar de 90%. `aprovado()` retorna `True`.

## Caso 2 — candidato não avaliado levanta exceção, nunca é presumido aprovado

O mesmo candidato, mas sem `ResultadoDeAvaliacao` associado. Chamar `aprovado()` levanta
`ModeloNaoAvaliado` — nunca retorna `False` silenciosamente, que poderia ser confundido com
"avaliado e reprovado".

## Caso 3 — plano sem fallback é rejeitado

Um `PlanoDeTarefa` declarado apenas com modelo principal, sem fallback, é rejeitado por
`validar_plano` antes de a tarefa poder depender dele.

## Caso 4 — comparação de custo por tarefa inverte a intuição de preço por token

Um modelo A tem preço por token menor, mas exige mais tokens de saída e uma tentativa adicional
para o mesmo resultado; um modelo B tem preço por token maior, mas resolve em menos tokens e
sem retry. `comparar_custo_por_tarefa` calcula o total de cada um e pode apontar B como mais
barato na prática, mesmo com preço unitário maior.

## Caso 5 — troca de modelo sempre registrada

Uma tarefa que usava o modelo X passa a usar o modelo Y. `registrar_troca` grava data, motivo e
o resultado de avaliação que justificou a troca — o histórico nunca fica incompleto.


Os cinco casos, lidos em sequência, formam a jornada completa de uma decisão de seleção: do
requisito declarado até a troca eventual de um modelo já em uso, cobrindo tanto o caminho de
sucesso quanto os dois pontos onde a decisão deveria falhar explicitamente (avaliação ausente,
fallback ausente) em vez de prosseguir sobre uma suposição não verificada.