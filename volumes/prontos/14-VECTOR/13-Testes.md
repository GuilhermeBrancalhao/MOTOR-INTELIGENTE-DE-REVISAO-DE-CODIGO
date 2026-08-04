---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

## Estratégia

Testar este motor exige simular os pontos de rejeição do fluxograma (`06-Fluxogramas`)
explicitamente — consulta sem métrica, sem partição, com versão de modelo incompatível — não só
o caminho de busca bem-sucedida.

## O que a suíte precisa cobrir

Versão de modelo: um teste que tenta comparar vetores de versões diferentes e verifica rejeição
(V1). Métrica e partição obrigatórias: testes que omitem cada campo separadamente e verificam
rejeição independente um do outro (V2, V3). Exclusão: um teste que exclui um documento e confirma
que ele nunca aparece em resultado de busca subsequente, mesmo que o vetor continue
fisicamente presente na estrutura (V6).

## Prova por mutação

Um teste forte para V3 é um que falha se a checagem de partição for removida da função de busca —
um resultado de partição diferente da consultada apareceria, e o teste que compara `particao` de
cada resultado contra a partição da consulta capturaria isso.

## Testes de integração com volumes vizinhos

Um teste relevante verifica que documento marcado como `Expirado` por `11-KNOWLEDGE` continua
fisicamente indexado aqui (a exclusão de `13-RAG`/`11` é lógica, não deste volume) — a
responsabilidade de excluir por expiração é de outro volume; este só executa exclusão que lhe é
explicitamente comunicada.

## O que a suíte não cobre ainda

Desempenho de busca em escala — os testes verificam correção (rejeição, filtro, exclusão) com
poucos vetores, não o comportamento sob volume que exigiria estrutura de indexação eficiente em
vez da varredura linear que o exemplo mínimo usa. Essa lacuna é aceitável para o propósito do
exemplo (provar o contrato), mas registrada aqui para não ser confundida com benchmark de
desempenho real.
