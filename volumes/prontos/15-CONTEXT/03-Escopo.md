---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

## Dentro deste volume

Orçamento explícito de tokens da janela de contexto, ordem de prioridade entre categorias de
conteúdo que competem pelo espaço, registro do que é descartado quando o limite é excedido, e
gatilho de compactação de histórico antigo.

## Fora deste volume, e para onde vai

**O que é relevante recuperar de uma base de conhecimento** é `13-RAG` — este volume recebe os
documentos já selecionados por aquele pipeline como um dos tipos de conteúdo que competem por
espaço na janela, mas nunca decide quais documentos são candidatos.

**A qualidade do resumo produzido na compactação** (se compactação usa geração por modelo) é
responsabilidade de quem implementa a compactação especificamente — este volume decide *quando*
compactar e *o que* fica de fora do orçamento, não como o resumo em si é gerado.

**Orçamento de passos, tokens de execução e tempo de um agente** é `08-AGENT-ENGINE` — aquele
volume trata do orçamento de uma execução inteira (múltiplas chamadas ao modelo); este volume
trata do orçamento de uma única janela de contexto, que pode ser consultada múltiplas vezes
dentro do orçamento maior de uma execução.

## Fronteira deliberada

Este volume nunca decide se um sistema deveria ou não usar recuperação de conhecimento — ele só
garante que, se documentos recuperados existem, eles competem pelo mesmo orçamento que qualquer
outro tipo de conteúdo, sem tratamento especial implícito que os isente da priorização.
