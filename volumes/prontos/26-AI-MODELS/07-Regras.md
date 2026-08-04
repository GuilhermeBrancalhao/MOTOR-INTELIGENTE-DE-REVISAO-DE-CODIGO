---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**M1 — Seleção de modelo é orientada por requisito de capacidade declarado explicitamente pela
tarefa, nunca por preferência de novidade sem verificação.** *Consequência:* a escolha de modelo é
justificável por critério verificável, não por impressão de qual é "o mais avançado do momento".

**M2 — Todo modelo é validado contra casos de ouro antes de ser confiado a uma tarefa.**
*Consequência:* "nunca avaliado" é estruturalmente distinto de "avaliado e aprovado" — nenhum
modelo entra em uso presumido como bom o suficiente.

**M3 — Toda tarefa que depende de um único modelo tem fallback explícito definido.**
*Consequência:* indisponibilidade do modelo principal nunca se torna, sem alternativa, a
indisponibilidade da tarefa inteira.

**M4 — Custo é comparado pela tarefa completa, nunca por preço unitário isolado.**
*Consequência:* um modelo mais barato por token que precisa de mais tokens ou mais tentativas
para o mesmo resultado não é automaticamente a opção mais barata.

**M5 — Nenhum preço, limite ou nome de modelo entra como fato duradouro; todo número é ilustração
datada de método.** *Consequência:* o volume não envelhece mal — o método continua válido mesmo
quando os números específicos de hoje deixarem de ser verdade.

**M6 — Toda troca de modelo é registrada com data, motivo e avaliação que a justificou.**
*Consequência:* nenhuma substituição de modelo acontece sem rastro — quem investiga uma mudança
de comportamento consegue encontrar exatamente quando e por que o modelo mudou.
