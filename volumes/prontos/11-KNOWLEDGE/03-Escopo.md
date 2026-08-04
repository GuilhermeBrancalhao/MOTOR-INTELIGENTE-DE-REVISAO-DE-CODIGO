---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

## Dentro deste volume

Curadoria (o que entra na base e com que autoridade), ingestão (o processo de trazer documento
para dentro da base, com falha explícita), autoridade de origem por documento, e ciclo de vida
(válido/expirando/expirado) com a garantia de que documento expirado não é devolvido como válido.

## Fora deste volume, e para onde vai

**O índice que torna o documento pesquisável** é `14-VECTOR` — este volume decide se um documento
deveria existir na base; aquele decide como ele é armazenado para busca eficiente.

**Recuperação, ranqueamento e geração de resposta** são `13-RAG` — este volume nunca decide qual
documento é mais relevante para uma pergunta específica, só se o documento é válido para ser
considerado candidato.

**Orçamento de janela de contexto** é `15-CONTEXT` — mesmo um documento válido e recuperado pode
não caber na janela; essa decisão é daquele volume, independente deste.

**Governança de dado sensível** é `30-AI-GOVERNANCE` — se um documento contém dado que exige
tratamento especial, a política vem de lá; este volume só garante que a autoridade de origem está
registrada para que aquela política possa ser aplicada.

## Fronteira deliberada

Este volume nunca decide relevância de um documento para uma consulta específica — isso
pressupõe conhecer a consulta, e curadoria acontece antes de qualquer consulta existir. Relevância
é sempre `13-RAG`.
