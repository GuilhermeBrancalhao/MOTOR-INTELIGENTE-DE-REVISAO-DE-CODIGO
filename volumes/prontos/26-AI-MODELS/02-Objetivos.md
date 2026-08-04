---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Selecionar modelo por capacidade exigida pela tarefa, declarada explicitamente, nunca por
preferência de marca ou novidade sem verificação correspondente.

Validar todo modelo contra casos de ouro antes de confiar nele para uma tarefa — a mesma barra de
avaliação que `07-PROMPT-ENGINE` já formaliza para prompt se aplica à escolha de modelo.

Definir fallback explícito para toda tarefa que depende de um único modelo, para que
indisponibilidade do modelo principal não vire indisponibilidade da tarefa inteira.

Comparar custo pela tarefa completa — tokens de entrada, saída e número de tentativas até
sucesso — nunca apenas pelo preço isolado por token, que pode enganar quando um modelo mais barato
por token precisa de mais tokens ou mais tentativas para o mesmo resultado.

Registrar toda troca de modelo com data, motivo e resultado de avaliação — nunca uma substituição
silenciosa que ninguém consegue rastrear depois.

Os cinco objetivos formam uma sequência de confiança crescente: um modelo só é considerado (M1)
depois de declarado o que a tarefa exige; só é confiado (M2) depois de avaliado; só sustenta uma
tarefa crítica (M3) com alternativa definida; só é comparado a outro (M4) pelo resultado prático,
não pela etiqueta de preço; e toda mudança nessa cadeia de confiança (M6) fica registrada, para
que a decisão de ontem continue explicável amanhã.