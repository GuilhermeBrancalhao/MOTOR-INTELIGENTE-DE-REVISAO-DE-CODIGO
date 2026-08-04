---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Código gerado por IA ou por ferramenta determinística não ganha um passe livre pelas mesmas
verificações que código escrito à mão precisa atravessar — a origem do código nunca é motivo
para dispensar validação, revisão ou rastreabilidade. Um código que compila e passa teste porque
foi gerado corretamente é indistinguível, nas garantias que oferece, de um código que passou por
essas mesmas verificações depois de escrito manualmente; um código gerado que pula essas
verificações "porque a IA normalmente acerta" é uma aposta, não uma garantia.

Este volume trata da disciplina de geração de código: toda saída gerada passa pela mesma
validação que código humano (compilação, teste), é marcada como gerada e nunca editada
manualmente, a geração é reproduzível a partir da mesma especificação, revisão humana é
obrigatória antes de qualquer código gerado entrar em produção, a especificação que produziu o
código é versionada junto dele, e todo código gerado declara explicitamente seu escopo — o que
foi pensado para fazer, e o que não foi.

A disciplina de nunca editar manualmente conteúdo gerado, já estabelecida em `35-DOCUMENTATION`
para documentação, se aplica aqui com ainda mais força — código gerado editado manualmente sem
atualizar a especificação correspondente cria uma divergência que a próxima geração apaga
silenciosamente, exatamente o problema que motivou a regra original.
