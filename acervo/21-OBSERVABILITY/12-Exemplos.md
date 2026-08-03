---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 12-Exemplos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Exemplos

## Caso 1 — sucesso técnico mascarando falha de qualidade

Um passo de IA em `10-WORKFLOW` chama o modelo para classificar um documento; a chamada devolve
sucesso técnico (sem erro de rede, formato válido), mas a categoria atribuída está errada, dado
que só é descoberto quando um humano revisa o resultado dias depois. Sem instrumentação que
distinga "sucesso de chamada" de "correção de resultado", nenhum sinal automático teria capturado
esse caso — é exatamente a lacuna que motiva a invariante central deste volume em `07-Regras.md`.

## Caso 2 — limiar mal calibrado gerando fadiga de alerta

Um limiar de taxa de encerramento por orçamento excedido em `08-AGENT-ENGINE` é fixado em "mais
de 5% das execuções" sem observação prévia, quando a taxa normal real do sistema, uma vez
observada por semanas, se mostra estar entre 8% e 12% para o tipo de tarefa mais comum. O alerta
dispara quase todo dia, e a equipe começa a ignorá-lo — até um pico real (30%) passar
despercebido no meio do ruído. A recalibração correta, feita depois com base na distribuição
real observada, eleva o limiar para um valor acima da variação normal e restaura a utilidade do
alerta.

## Caso 3 — canal de notificação falho por três dias sem detecção

Um sinal de segurança de `17-SECURITY` cruza o limiar de alerta corretamente, mas o canal de
notificação (um serviço de mensagem externo) está fora do ar por três dias sem que ninguém saiba
— o sistema "acha" que avisou, mas nenhuma mensagem chegou. Um heartbeat periódico do canal, que
este volume trata como controle obrigatório (`07-Regras.md`), teria detectado a indisponibilidade
no primeiro ciclo de verificação, muito antes de qualquer sinal real precisar passar por ele.
