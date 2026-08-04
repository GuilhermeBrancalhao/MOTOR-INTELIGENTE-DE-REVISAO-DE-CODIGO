---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 08-Modelos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Modelos

`VersaoSemantica` carrega `major`, `minor` e `patch` como campos separados, nunca uma string
única — a estrutura explícita é o que permite `validar_release` comparar especificamente o
número maior entre duas versões, sem depender de análise de string frágil.

`MembroDeSDK` e `ErroDoSDK` são ambos imutáveis, e ambos recusam sua própria criação em estado
inválido — a mesma disciplina de validação em `__post_init__` já vista em outros volumes deste
acervo, tornando estado inválido estruturalmente impossível de existir, não apenas
desencorajado por convenção.

`SuperficieDoSDK.membros` é um dicionário indexado por nome — a estrutura escolhida garante que
`remover_membro` sempre encontra o estado atual (público, depreciado, ou nenhum dos dois) antes
de decidir se a remoção é permitida, sem precisar varrer uma lista para localizar o membro.

`ExemploDeUso` carrega `resultado_verificado` como campo booleano simples, deliberadamente sem
metadado adicional sobre quando ou como a verificação ocorreu — o modelo mínimo aqui é
suficiente para provar a regra AC6 por mutação; um sistema real de documentação executável
poderia estender esse campo com timestamp e referência à execução real, sem alterar o princípio
central de que nenhum exemplo é aceito sem verificação prévia.

Nenhum dos três modelos (`VersaoSemantica`, `MembroDeSDK`, `ErroDoSDK`) depende de biblioteca
externa de validação — toda a verificação acontece com Python puro no próprio `__post_init__`,
mantendo o modelo simples de auditar e de testar por mutação sem qualquer dependência adicional.