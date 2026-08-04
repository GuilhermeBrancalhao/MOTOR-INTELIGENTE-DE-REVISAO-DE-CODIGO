---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Comparar dois vetores de embeddings gerados por modelos diferentes é uma operação que sempre
devolve um número — cosseno, produto escalar, distância euclidiana, qualquer métrica aceita dois
vetores de mesma dimensão e produz um resultado. O problema é que esse número não significa nada
quando os dois vetores vêm de espaços semânticos diferentes: a métrica não recusa a comparação,
ela só devolve lixo com aparência de resultado válido. Esse é o risco central que este volume
existe para prevenir — não porque a operação falha, mas porque ela "funciona" silenciosamente
enquanto produz resultado sem sentido algum.

Este volume trata do índice vetorial como componente de infraestrutura de busca: como o
embedding é gerado e versionado, qual métrica de similaridade é usada e por que ela precisa ser
declarada explicitamente por índice, como o espaço é particionado para isolar coleções
não relacionadas, e como reindexação e exclusão acontecem sem expor estado inconsistente a quem
consulta.

A fronteira com `13-RAG` é a mesma do restante do grupo: este volume nunca decide o que fazer com
o resultado de uma busca — ordenar, filtrar, citar, decidir se é relevante o suficiente para
compor uma resposta. Ele só garante que a busca em si é correta: que compara vetores do mesmo
espaço, na mesma métrica, dentro da partição certa, e nunca devolve um documento que já foi
excluído.
