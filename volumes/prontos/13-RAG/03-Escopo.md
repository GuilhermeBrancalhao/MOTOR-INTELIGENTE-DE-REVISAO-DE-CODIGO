---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

## Dentro deste volume

O pipeline que recupera candidatos de `14-VECTOR`, reordena por relevância à pergunta específica,
compõe resposta com citação rastreável a documento de `11-KNOWLEDGE`, e mede fidelidade — o quanto
da resposta de fato se sustenta no que foi citado.

## Fora deste volume, e para onde vai

**Curadoria e ciclo de vida de documento** é `11-KNOWLEDGE` — este volume consulta o estado de
validade de um documento antes de citá-lo, mas nunca decide se o documento deveria existir ou
continuar válido.

**Índice, métrica de similaridade e particionamento** é `14-VECTOR` — este volume consome
resultado de busca já correto; nunca decide qual métrica usar ou como o espaço vetorial é
organizado.

**Orçamento de janela de contexto** (quantos documentos cabem, o que é descartado por limite de
tokens) é `15-CONTEXT` — este volume decide *quais* documentos são candidatos relevantes; aquele
decide *quantos* cabem na chamada ao modelo.

**Geração de texto da resposta em si** (a chamada ao modelo que produz a resposta final) é
`08-AGENT-ENGINE` ou infraestrutura de geração direta, dependendo do desenho do sistema — este
volume prepara o contexto e verifica fidelidade do resultado, não executa a geração.

## Fronteira deliberada

Este volume nunca aceita citação que não resolve a um documento real e válido no momento da
citação — mesmo que o documento tenha sido válido quando indexado, se expirou entre a indexação e
a consulta, a citação é recusada.
