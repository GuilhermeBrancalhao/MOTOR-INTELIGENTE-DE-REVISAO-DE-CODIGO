---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Cálculo automático de custo estimado de dívida técnica (hoje o campo `custo_estimado` de
`ItemDeDivida` é texto livre fornecido por quem registra, sem um modelo que o calcule ou valide).

Alerta automático quando uma exceção de gate se repete acima de um limiar de frequência (hoje a
métrica existe para acompanhamento manual, sem gatilho automático de revisão).

Decomposição do indicador por tipo de regra (segurança, correção funcional, performance) além de
por área do sistema — hoje `Medicao` é uma medição única por execução, sem dimensão adicional de
categoria de regra.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (medição por prova de mutação, gate, dívida registrada,
detecção de regressão), testado por mutação nas seis regras. Depois, integração real com a
prática de teste do `31-TESTING` como fonte da contagem de regras com prova.

## O que este volume assume que pode mudar

O limiar único global (`limiar_minimo`) é o mínimo suficiente hoje — um limiar diferenciado por
criticidade de área do sistema pode ser necessário conforme a diversidade de componentes cresce,
sem alterar o princípio central de decisão por prova de regra, nunca por cobertura de linha.
