---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Medição de fidelidade automatizada com precisão além de correspondência textual simples — o
exemplo mínimo verifica se uma afirmação "aparece" numa citação de forma direta; um verificador
mais sofisticado precisaria de julgamento semântico sobre se a citação de fato sustenta a
afirmação, não só contém palavras parecidas.

Reordenação por critério além de similaridade textual (por exemplo, autoridade do documento
combinada com relevância) — hoje o exemplo trata reordenação e confirmação de validade como
etapas separadas; combinar autoridade (de `11-KNOWLEDGE`) diretamente no critério de reordenação
é extensão possível não coberta ainda.

Cache de resposta para perguntas repetidas, com invalidação quando a fonte subjacente muda — não
especificado neste ciclo; toda consulta hoje é tratada como nova, sem reaproveitamento.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (recuperação, reordenação, confirmação de validade,
composição com citação), testado por mutação nas seis regras. Depois, integração real de ponta a
ponta com `11-KNOWLEDGE` e `14-VECTOR` já promovidos, verificando que a tradução de tipos entre
os três volumes preserva a informação necessária em cada fronteira.

## O que este volume assume que pode mudar

O cálculo de fidelidade como proporção simples de afirmações sustentadas é o mínimo suficiente
hoje — um cálculo ponderado (afirmações mais centrais pesando mais que detalhes secundários) pode
emergir com uso real, sem alterar o princípio central de R2 (fidelidade medida, não assumida).
