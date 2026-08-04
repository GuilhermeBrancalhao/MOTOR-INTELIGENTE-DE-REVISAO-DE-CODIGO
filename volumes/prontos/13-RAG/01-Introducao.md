---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Um sistema de recuperação aumentada por geração pode ter fonte curada (`11-KNOWLEDGE`) e índice
correto (`14-VECTOR`) e ainda produzir resposta que ninguém consegue verificar — porque a
resposta não cita de onde veio, ou porque cita algo que na verdade não sustenta a afirmação
feita. Fidelidade — a propriedade de que toda afirmação na resposta é rastreável a um documento
recuperado que de fato a sustenta — é o problema que este volume resolve, e ele não se resolve
automaticamente só porque a recuperação em si funciona bem.

Este volume trata do pipeline que junta fonte e índice numa resposta: recuperar candidatos
(consultando `14-VECTOR`), reordenar por relevância (um passo distinto da recuperação inicial,
porque proximidade vetorial não é a mesma coisa que relevância para a pergunta específica),
compor resposta com citação, e medir fidelidade — o quanto da resposta de fato se sustenta nos
documentos citados, não só parece plausível.

A fronteira com os dois volumes que este consome é a mesma decidida em `ROADMAP.md`: este volume
nunca cura fonte (isso é `11`) nem opera índice (isso é `14`) — ele só decide, a partir do que os
dois já garantem, o que de fato entra numa resposta e como isso é citado de volta à fonte.
