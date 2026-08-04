---
volume: "05"
volume_nome: BUSINESS
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — objetivo válido, autoridade clara

Um projeto de automação de suporte tem um único patrocinador com autoridade de decisão, três
gerentes de área como consultados, e a equipe de atendimento como informada. O patrocinador
propõe: "reduzir o tempo médio de primeira resposta de 4 horas para 30 minutos, medido no
trimestre seguinte ao lançamento". O objetivo passa o teste de falsificabilidade (o número existe
e é auditável) e vem de quem tem autoridade — captura completa, libera para `03-DISCOVERY`.

## Caso 2 — discordância entre dois stakeholders com autoridade

O mesmo projeto, mas com dois patrocinadores de áreas diferentes, ambos classificados como
`DECIDE` por financiarem partes distintas do orçamento. Um propõe reduzir tempo de resposta; o
outro propõe reduzir custo de operação do time de suporte, e os dois objetivos competem pelo mesmo
recurso técnico (automatizar mais casos reduz tempo, mas aumenta custo de manutenção da
automação). O processo registra a discordância explicitamente e força os dois patrocinadores a
decidir prioridade antes de qualquer requisito técnico ser escrito — não decide por eles.

## Caso 3 — objetivo rejeitado por não ser falsificável

Um stakeholder propõe "melhorar a experiência do cliente com o suporte" como objetivo. O
processo pergunta: que fato observável provaria isso não cumprido? A resposta inicial —
"as pessoas vão gostar mais" — não é observável. Devolvido para refinamento, o objetivo vira
"reduzir a taxa de reabertura de chamado de 18% para 8% no trimestre seguinte", que passa o
teste porque a taxa de reabertura é medida e o valor-alvo é falsificável.
