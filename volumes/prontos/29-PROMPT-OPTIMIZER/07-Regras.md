---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**O1 — Toda variante candidata é avaliada contra exatamente a mesma amostra de casos de ouro
usada para o baseline.** *Consequência:* a comparação entre versões nunca é distorcida por
amostras diferentes — só a variação do próprio corpo do prompt explica a diferença de resultado.

**O2 — Uma variante só é considerada candidata a substituir o baseline quando a melhoria supera
uma margem mínima, nunca uma diferença marginal dentro do ruído esperado.** *Consequência:* a
busca não confunde variação estatística normal da amostra com melhoria real do prompt.

**O3 — O otimizador nunca promove uma variante; apenas propõe.** *Consequência:* toda variante
candidata, gerada por busca automática ou escrita manualmente, atravessa a mesma barreira de
revisão e avaliação formal do 07 antes de chegar a produção.

**O4 — Toda busca respeita um orçamento de tentativas declarado antecipadamente.**
*Consequência:* nenhuma busca roda indefinidamente sem critério de parada — o custo de avaliação
é sempre limitado por uma decisão explícita, não por acidente de implementação.

**O5 — Toda tentativa avaliada é registrada, mesmo quando rejeitada.** *Consequência:* o espaço
de busca já explorado permanece visível — uma busca futura, ou uma pessoa revisando o histórico,
não precisa reexplorar às cegas o que já foi tentado sem sucesso.

**O6 — A função objetivo (casos de ouro) nunca é ajustada pelo próprio processo de busca.**
*Consequência:* a busca não pode "melhorar" seu resultado movendo o próprio critério de
avaliação — a única forma de melhorar o resultado é melhorar o prompt.
