---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 06-Fluxogramas
status: PRONTO
atualizado_em: 2026-08-03
---

# Fluxogramas

O fluxo de decisão de alerta já está em `04-Arquitetura.md` (o `flowchart` que satisfaz a
exigência de diagrama do tipo `GOVERNANCA`). Esta seção detalha o processo de calibração de
limiar, que é o que decide, na prática, se um sinal específico cruza de "observar" para
"alertar".

## Calibração inicial

Um limiar novo nunca começa por adivinhação de valor absoluto — começa observando a distribuição
real do sinal por um período (dias a semanas, dependendo do volume de eventos) sem alertar,
apenas registrando. O limiar inicial é derivado dessa distribuição (por exemplo, um percentil
alto observado), não de uma meta abstrata definida antes de qualquer dado real existir.

## Recalibração

Um limiar que gera alerta com frequência muito maior que o esperado pela criticidade real do
sinal precisa de recalibração — mas recalibrar significa revisar se o limiar está errado ou se o
comportamento do sistema de fato mudou (nesse caso, o alerta estava certo em avisar, e o que
precisa de correção é o sistema, não o limiar). Recalibrar sem essa distinção corre o risco de
silenciar um sinal real ajustando o limiar para "parar de incomodar".

## O caminho que nunca deveria existir

Um sinal que cruza o limiar de alerta e não gera notificação — por bug no avaliador de limiar, por
canal de notificação falho, ou por supressão manual esquecida — é o cenário mais perigoso deste
volume, porque combina a detecção correta (o sistema sabia) com a falha de ação (ninguém foi
avisado). A matriz de controles de `07-Regras.md` trata esse caminho explicitamente como algo a
verificar, não a assumir que nunca acontece.
