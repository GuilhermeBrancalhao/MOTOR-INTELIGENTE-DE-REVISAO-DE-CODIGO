---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Um pipeline de recuperação de conhecimento pode ter índice impecável e ranqueamento sofisticado
e ainda devolver resposta errada, se o documento que ele recupera estiver desatualizado,
duplicado com informação conflitante, ou sem procedência que permita confiar nele. O erro nesse
caso não está no índice nem no ranqueamento — está na fonte, que é o assunto deste volume.

Curar uma base de conhecimento não é o mesmo que indexá-la. Indexar (`14-VECTOR`) transforma
documento em vetor pesquisável; curar decide se um documento deveria entrar na base, com que
autoridade, e por quanto tempo continua válido. Um documento pode estar perfeitamente indexado e
ainda assim ser a fonte errada — porque expirou, porque foi substituído por uma versão mais
recente que ninguém removeu, ou porque nunca teve autoridade suficiente para ser tratado como
verdade.

Este volume trata do ciclo de vida completo de um documento na base: ingestão com autoridade
declarada, detecção de conflito quando dois documentos afirmam coisas diferentes sobre o mesmo
fato, e expiração — a garantia de que documento vencido nunca é devolvido como se fosse válido
por padrão. A fronteira com `13-RAG` é direta: este volume decide o que **pode** ser recuperado;
aquele decide o que **de fato é** recuperado e como isso vira resposta.
