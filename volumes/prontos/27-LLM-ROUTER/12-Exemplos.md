---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — principal saudável, roteamento direto

Um sinal de saúde com amostra suficiente e taxa de falha baixa mantém o roteamento no candidato
principal, com motivo `"principal_saudavel"`.

## Caso 2 — falha isolada não dispara fallback

Um sinal com apenas uma chamada, que falhou, não atinge o mínimo de amostra — o roteamento
permanece no principal, porque uma falha isolada não prova degradação.

## Caso 3 — degradação sustentada aciona fallback

Um sinal com amostra suficiente e taxa de falha acima do limiar aciona fallback automaticamente,
com motivo `"fallback_por_degradacao"` — sem bloquear a chamada esperando o principal se
recuperar.

## Caso 4 — recuperação exige janela de estabilidade

Depois do fallback do Caso 3, sinais saudáveis consecutivos abaixo do tamanho da janela de
estabilidade mantêm o roteamento no fallback; só ao completar a janela o roteamento volta ao
principal.

## Caso 5 — candidato não aprovado é rejeitado antes de qualquer roteamento

Uma tentativa de rotear usando um candidato que não está em `candidatos_aprovados` é rejeitada
imediatamente, antes de qualquer consulta a sinal de saúde.


Os cinco casos, em sequência, formam o ciclo de vida completo de uma tarefa roteada: do
roteamento normal até a degradação, o período de instabilidade sob janela de estabilidade, e a
eventual recuperação — o Caso 5 isolado prova que nada disso acontece para um candidato que nunca
deveria ter sido considerado em primeiro lugar.

Essa progressão deliberada — dos cinco casos, cada um constrói sobre o estado deixado pelo anterior quando aplicável — espelha como uma tarefa real evolui ao longo de uma janela de tempo mais longa que uma única chamada isolada.