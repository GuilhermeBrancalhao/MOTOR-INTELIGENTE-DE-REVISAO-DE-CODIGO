---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Medir cobertura pela taxa de prova por mutação — proporção de regras declaradas com teste que de
fato falha quando a regra é violada — nunca apenas pela proporção de linha executada, que não
prova nada sobre verificação real.

Bloquear release quando o indicador agregado cai abaixo de um piso declarado, nunca liberar "só
desta vez" sem uma exceção explicitamente registrada e rastreável.

Registrar dívida técnica como item explícito e datado — o quê, por que foi adiado, custo estimado
de deixar como está — nunca como julgamento implícito que só existe na memória de quem decidiu
adiar.

Acompanhar tendência do indicador ao longo de múltiplas medições, nunca julgar qualidade a partir
de uma única fotografia isolada que não distingue queda pontual de regressão real.

Investigar toda regressão do indicador entre duas medições antes de aceitá-la como novo normal —
nunca normalizar silenciosamente uma queda sem entender a causa.

Os cinco objetivos formam uma sequência: medir corretamente (H1) é pré-requisito para bloquear
corretamente (H2), e ambos são inúteis sem registro de dívida honesto (H3) e visão de tendência
real (H4/H5) — um sistema que mede bem mas nunca investiga queda, ou que investiga mas não
registra o que decidiu adiar, perde metade do valor de ter um indicador em primeiro lugar.