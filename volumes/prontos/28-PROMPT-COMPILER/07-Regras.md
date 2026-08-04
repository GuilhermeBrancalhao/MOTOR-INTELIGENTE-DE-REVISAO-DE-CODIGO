---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**Q1 — O compilador só aceita prompt no estado PROMOVIDO do 07.** *Consequência:* nenhum prompt
em rascunho ou ainda em avaliação chega a produzir payload usado em chamada real.

**Q2 — A mesma combinação de prompt, variáveis e dialeto sempre produz o mesmo payload.**
*Consequência:* dois payloads diferentes da mesma origem seriam uma divergência impossível de
rastrear — determinismo é o que torna a compilação auditável.

**Q3 — Orçamento de tokens é verificado contra o payload já compilado, nunca assumido; excesso
falha explicitamente.** *Consequência:* nenhum conteúdo é truncado silenciosamente para caber —
quem excede o orçamento sabe disso antes de qualquer chamada real acontecer.

**Q4 — Toda lógica de dialeto de provedor é isolada atrás de um adaptador explícito, nunca
condicional espalhada no núcleo do compilador.** *Consequência:* trocar de provedor significa
trocar o adaptador, nunca reescrever a lógica central de compilação.

**Q5 — Ponto de cache só é posicionado em conteúdo estável entre chamadas, nunca dentro de
variável que muda a cada chamada.** *Consequência:* cache mal posicionado nunca desperdiça a
oportunidade de reaproveitamento que ele deveria oferecer.

**Q6 — Variável declarada no contrato do prompt sem valor fornecido é erro de compilação
explícito, nunca substituição silenciosa.** *Consequência:* um payload nunca é enviado com
placeholder não resolvido ou conteúdo vazio que ninguém pretendia.
