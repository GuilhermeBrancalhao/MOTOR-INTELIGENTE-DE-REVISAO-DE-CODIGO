---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Estratégia de geração de candidato guiada por modelo (hoje o volume assume um gerador de
candidatos fornecido externamente, sem prescrever como ele produz variação).

Paralelização de avaliação de múltiplos candidatos simultaneamente, respeitando o mesmo orçamento
total — hoje a busca avalia um candidato de cada vez, sequencialmente.

Critério de parada antecipada quando uma sequência de tentativas consecutivas não produz melhoria
— hoje a busca só para por orçamento esgotado ou candidatos esgotados, nunca por "não está indo a
lugar nenhum".

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (avaliação contra amostra fixa, limiar de melhoria,
orçamento, histórico completo), testado por mutação nas seis regras. Depois, integração real com
o fluxo de versionamento do `07-PROMPT-ENGINE` para submissão de proposta.

## O que este volume assume que pode mudar

O critério de melhoria como diferença absoluta de taxa de acerto é o mínimo suficiente hoje — um
teste estatístico mais rigoroso (significância contra tamanho de amostra) pode ser necessário
conforme a escala de uso cresce, sem alterar o princípio central de nunca confundir ruído com
melhoria real.
