---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**Z1 — Tarefa é ordenada por dependência real, nunca por ordem arbitrária.** *Consequência:*
nenhuma tarefa é agendada antes de outra da qual ela de fato depende, e um ciclo de dependência
impossível é detectado antes de execução começar.

**Z2 — Toda estimativa é declarada com incerteza explícita, nunca número único de falsa
precisão.** *Consequência:* a incerteza real do trabalho fica visível para quem planeja em torno
dela, em vez de escondida atrás de uma precisão que a estimativa não sustenta.

**Z3 — Escopo de ciclo é negociado e registrado antes de execução começar.**
*Consequência:* nenhuma expansão de escopo acontece silenciosamente no meio do ciclo sem
renegociação explícita e visível.

**Z4 — Plano é revisado explicitamente, com motivo declarado, quando a realidade diverge dele.**
*Consequência:* nenhuma divergência é contornada silenciosamente fingindo que o plano original
ainda vale.

**Z5 — Tarefa bloqueada por impedimento externo é marcada como tal, distinta de tarefa
simplesmente não iniciada.** *Consequência:* as duas situações, que exigem ação completamente
diferente, nunca são confundidas uma com a outra.

**Z6 — Conclusão de tarefa é estado verificável contra critério de pronto próprio, nunca
presumida.** *Consequência:* "parece pronto" nunca substitui confirmação real contra o critério
que a própria tarefa declarou.

Juntas, as seis regras tratam planejamento com o mesmo rigor que este acervo já aplica a outros
processos — nenhuma delas exige ferramenta sofisticada, todas exigem apenas disciplina de
declarar explicitamente o que, de outra forma, ficaria implícito e sujeito a erro silencioso.