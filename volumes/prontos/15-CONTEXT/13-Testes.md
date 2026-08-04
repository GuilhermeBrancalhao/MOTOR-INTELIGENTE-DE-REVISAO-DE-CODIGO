---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

## Estratégia

Testar este gestor exige simular pressão de orçamento explicitamente — não é suficiente testar
só o caminho onde tudo cabe confortavelmente. A técnica é configurar orçamento artificialmente
pequeno e verificar o comportamento de descarte no ponto exato em que ele deveria acontecer.

## O que a suíte precisa cobrir

Descarte por prioridade: um teste com itens de categorias diferentes, orçamento insuficiente para
todos, verificando que o descarte remove exatamente o de menor prioridade primeiro (C2). Registro
de descarte: um teste que confirma que todo item removido tem `Descarte` correspondente, nunca
ausência silenciosa (C3). Instrução nunca descartada: um teste que enche o orçamento com outras
categorias e confirma que `INSTRUCAO_SISTEMA` permanece até o fim, sendo a última candidata a
remoção (C6). Recusa quando nem instrução cabe: um teste com orçamento menor que o tamanho da
própria instrução, verificando recusa explícita, não descarte parcial da instrução.

## Prova por mutação

Um teste forte para C2 é um que falha se a ordem de descarte for trocada para "remove o item mais
recente" em vez de "remove o de menor prioridade" — um item de prioridade alta adicionado por
último seria removido incorretamente antes de um item de prioridade baixa adicionado antes.

## Testes de integração com volumes vizinhos

Um teste relevante verifica que documento recuperado por `13-RAG`, traduzido para
`ItemDeContexto`, é tratado com a mesma disciplina de prioridade que qualquer outra categoria —
sem tratamento especial implícito só por vir daquele pipeline.
