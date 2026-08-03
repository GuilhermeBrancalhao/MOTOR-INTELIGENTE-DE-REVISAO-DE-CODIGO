---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-03
---

# Introdução

Um teste que só confirma o caminho feliz — entrada válida produz saída esperada — documenta que
o código funciona quando tudo dá certo, mas não prova que ele detectaria uma quebra futura na
regra que deveria proteger. Essa distinção entre "teste que documenta comportamento" e "teste que
trava comportamento contra regressão" é o assunto central deste volume: tratar teste como
especificação executável significa que cada teste corresponde a uma regra ou invariante
específica, e prova sua própria utilidade ao falhar quando essa regra é violada de propósito.

O critério prático para essa prova é mutação: alterar deliberadamente o código para violar a
regra que um teste deveria proteger e confirmar que o teste de fato falha. Um teste que continua
passando depois da mutação não estava testando a regra — estava testando alguma outra coisa,
frequentemente só a ausência de erro de sintaxe. Este padrão não é abstrato neste acervo: cada um
dos volumes essenciais escritos neste ciclo (`08-AGENT-ENGINE`, `09-ORCHESTRATOR`, `10-WORKFLOW`,
`17-SECURITY`, `21-OBSERVABILITY`) descreve, na própria seção `13-Testes.md`, pelo menos um
exemplo concreto de teste que só se justifica por sobreviver à mutação da regra que protege.

Este volume trata da prática — como escrever, organizar e manter esse tipo de teste — e não do
indicador agregado que mede a saúde dessa prática ao longo do tempo (cobertura, taxa de teste
quebradiço, tendência de dívida), que é assunto de `32-QUALITY`. A fronteira entre os dois é a
mesma que existe entre "como se faz" e "como se mede que está sendo bem feito", e confundir os
dois volumes levaria a tratar uma prática de engenharia como se fosse apenas um número a
otimizar.
