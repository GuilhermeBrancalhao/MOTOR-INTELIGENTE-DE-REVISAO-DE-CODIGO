---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

## Dentro deste volume

Versionamento de embedding por modelo, declaração explícita de métrica de similaridade por
índice, particionamento de coleções não relacionadas, atomicidade de reindexação do ponto de
vista do consumidor, e exclusão real (documento excluído nunca é devolvido, mesmo antes de
compactação física completa).

## Fora deste volume, e para onde vai

**O que fazer com o resultado de uma busca** (ordenar por relevância, filtrar, citar, decidir se
é suficiente para uma resposta) é `13-RAG` — este volume só garante que a busca em si compara os
vetores certos, na métrica certa, dentro da partição certa.

**Curadoria e ciclo de vida de documento** é `11-KNOWLEDGE` — este volume indexa o que já foi
validado por aquele; nunca decide se um documento deveria existir na base.

**Geração do próprio embedding** (qual modelo, qual dimensão) é decisão de projeto que consome
este volume como infraestrutura — este volume versiona e isola por modelo, mas não escolhe qual
modelo usar.

**Orçamento de janela de contexto** é `15-CONTEXT`, inteiramente independente — um sistema pode
usar este volume sem nunca ter RAG algum, ou pode ter janela de contexto sem nunca consultar
índice vetorial.

## Fronteira deliberada

Este volume nunca decide relevância semântica de um resultado — só devolve o vetor mais próximo
pela métrica declarada. Julgamento sobre se o resultado é de fato útil para a pergunta que o
originou é sempre `13-RAG`.
