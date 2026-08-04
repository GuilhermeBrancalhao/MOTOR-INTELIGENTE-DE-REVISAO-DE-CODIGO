---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**J1 — Toda operação exposta a cliente declara SLO explícito antes de ser considerada pronta para
produção.** *Consequência:* o alvo de latência nunca é inferido depois, a partir do que o sistema
já faz — é uma decisão declarada antecipadamente.

**J2 — Desempenho é medido sob carga realista, nunca apenas em ambiente isolado.**
*Consequência:* contenção de recurso sob concorrência real, que uma medição isolada nunca
revelaria, é capturada antes de chegar à produção.

**J3 — Regressão de desempenho é investigada com o mesmo rigor que regressão de qualidade.**
*Consequência:* uma queda de desempenho nunca é descartada como "provavelmente ruído" sem
verificação — a mesma disciplina de H5 (`32-QUALITY`) se aplica aqui.

**J4 — Sob sobrecarga, o sistema degrada graciosamente, nunca falha catastroficamente para toda
requisição.** *Consequência:* toda operação declara estratégia de sobrecarga antes de entrar em
produção — rejeitar, aplicar backpressure, ou responder parcialmente, mas sempre uma decisão
explícita.

**J5 — Toda otimização é validada por medição antes e depois, nunca assumida como funcionando.**
*Consequência:* uma mudança "obviamente mais rápida" que não melhora o percentil medido é
rejeitada como otimização, mesmo que pareça razoável em teoria.

**J6 — SLO de operação que envolve chamada de IA reconhece explicitamente a variabilidade dessa
chamada, nunca tratada com o mesmo orçamento fixo de uma operação determinística.**
*Consequência:* a margem entre percentis reflete a variabilidade real, em vez de um alvo que a
chamada de IA violaria estruturalmente com frequência.
