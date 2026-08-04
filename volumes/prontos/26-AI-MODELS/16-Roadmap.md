---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Deriva de comportamento de modelo detectada automaticamente entre reavaliações periódicas — hoje
a reavaliação é uma boa prática recomendada, sem mecanismo automático que dispare reavaliação
quando um sinal de deriva é observado.

Seleção automática de fallback baseada em similaridade de capacidade, em vez de declaração manual
— hoje o fallback é sempre escolhido explicitamente por quem declara o `PlanoDeTarefa`.

Composição de múltiplos modelos para a mesma tarefa (por exemplo, um modelo barato para
triagem e um mais caro só para casos que passam por um filtro inicial) — hoje o modelo assume
seleção de um único modelo principal por tarefa, com um fallback.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (requisito, avaliação, fallback, custo por tarefa,
registro de troca), testado por mutação nas seis regras. Depois, integração real com o mecanismo
de roteamento do `27-LLM-ROUTER`.

## O que este volume assume que pode mudar

Tudo neste volume relacionado a número específico — preço, limite, nome de modelo — muda por
definição (regra de volume perecível). O que não deveria mudar é o método em si: requisito antes
de avaliação, avaliação antes de confiança, fallback explícito, custo pela tarefa completa,
registro de toda troca.
