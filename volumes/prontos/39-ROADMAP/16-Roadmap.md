---
volume: "39"
volume_nome: ROADMAP
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Alerta automático quando um item direcional de longo prazo permanece sem reclassificação por
tempo excessivo — hoje a reclassificação é uma boa prática recomendada, sem gatilho automático de
revisão.

Priorização quantitativa formal (pontuação numérica combinando valor, risco e dependência) — hoje
o critério é qualitativo e textual, sem um método de cálculo que combine os três fatores num
único score comparável entre itens.

Integração com o histórico de decisões de autoridade externa já resolvidas, para referência
futura — hoje cada sinalização de autoridade é tratada isoladamente, sem acumular um histórico
consultável de decisões anteriores semelhantes.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (critério de priorização, item fora de escopo, decisão de
autoridade, revisão periódica, distinção de horizonte), testado por mutação nas seis regras.
Depois, integração real com o processo de decomposição do `38-PROJECT-PLANNER` quando um item do
roadmap é de fato priorizado para um ciclo específico.

## O que este volume assume que pode mudar

O modelo de dois horizontes (`COMPROMETIDO_CURTO_PRAZO`, `DIRECIONAL_LONGO_PRAZO`) é o mínimo
suficiente hoje — uma escala mais granular (três ou mais níveis de confiança) pode ser necessária
conforme a diversidade de itens do backlog cresce, sem alterar o princípio central de nunca
prometer certeza que a distância temporal não sustenta.
