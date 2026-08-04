---
volume: "36"
volume_nome: DIAGRAMS
tipo: BIBLIOTECA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Este acervo já usa quatro tipos de diagrama de forma consistente em toda a sua extensão:
`C4Context` para visão de sistema e dependência externa, `sequenceDiagram` para interação ao
longo do tempo, `stateDiagram-v2` para ciclo de vida de uma entidade, e `flowchart` para
ramificação de decisão condicional. Este volume é o catálogo desse vocabulário — não introduz
tipo novo, formaliza o que já está em uso, declara o propósito específico de cada tipo, e
estabelece a disciplina que torna um diagrama confiável em vez de apenas decorativo.

Um diagrama sem prosa que explique o que não é óbvio na imagem é decoração, não documentação — a
estrutura visual mostra o quê, mas raramente explica o porquê de uma escolha específica de
representação. E um diagrama nunca verificado contra o que o sistema realmente faz hoje corre o
mesmo risco de qualquer documentação: ficar desatualizado silenciosamente, ativamente enganando
quem confia nele.

`35-DOCUMENTATION` já estabelece a disciplina de vigência para documentação em geral — este
volume aplica o mesmo princípio especificamente a diagrama, além de formalizar a escolha de tipo
certo para a necessidade certa, nunca o inverso.

Este volume não introduz sintaxe nova nem convenção paralela — formaliza, com propósito e
disciplina explícitos, exatamente o vocabulário visual que já percorre todo este acervo desde o
primeiro volume promovido, tornando esse vocabulário consultável num único lugar em vez de
implícito na prática repetida de quem escreveu cada volume anterior.