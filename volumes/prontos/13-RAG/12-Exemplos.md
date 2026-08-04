---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — resposta com fidelidade alta

Uma pergunta sobre política de reembolso recupera três candidatos de `14-VECTOR`, reordena para
um único documento claramente mais relevante, confirma que ele continua válido em
`11-KNOWLEDGE`, e gera resposta citando exatamente o trecho que sustenta a afirmação. Fidelidade
medida em 1.0 — toda afirmação da resposta rastreia à citação.

## Caso 2 — recusa por falta de fonte válida

A mesma pergunta, mas o único documento relevante expirou entre a indexação original e esta
consulta (confirmado por `11-KNOWLEDGE` na etapa de validação). Sem candidato válido restante, o
pipeline recusa explicitamente, em vez de gerar resposta a partir de um documento que já não é
confiável — o usuário recebe "sem fonte válida disponível", não uma resposta desatualizada
apresentada como atual.

## Caso 3 — fidelidade parcial detectada

Um documento válido é citado corretamente, mas a resposta gerada inclui uma afirmação adicional
que extrapola o conteúdo do documento (o modelo "completou" a informação com algo plausível mas
não presente na fonte). A medição de fidelidade detecta que essa afirmação específica não rastreia
a nenhuma citação, e a resposta é sinalizada como fidelidade parcial — a afirmação extra é
removida ou marcada, em vez de entregue com a mesma confiança que o restante da resposta.

## Caso 4 — reordenação inverte a ordem de proximidade

Cinco candidatos são recuperados por proximidade vetorial, mas o terceiro colocado por
proximidade é o único que de fato responde à pergunta específica (os outros quatro são
semanticamente próximos mas tratam de um aspecto diferente do tema). A reordenação move esse
candidato para o topo do ranking final — o `score_proximidade` original permanece registrado
para auditoria, mas não determina a ordem que a etapa seguinte do pipeline consome.
