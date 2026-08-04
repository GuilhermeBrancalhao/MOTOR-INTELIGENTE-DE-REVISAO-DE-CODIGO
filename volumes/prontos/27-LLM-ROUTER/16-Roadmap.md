---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Roteamento ponderado entre mais de dois candidatos (hoje o modelo trata apenas o par
principal/fallback, sem uma estratégia de distribuição entre três ou mais candidatos
simultaneamente elegíveis).

Ajuste automático de limiar de degradação baseado em comportamento histórico da própria tarefa,
em vez de configuração estática declarada uma vez.

Coordenação entre múltiplas instâncias de roteador operando sobre a mesma tarefa (hoje o estado
é local a uma instância de `Roteador`, sem modelo de estado compartilhado entre processos).

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (roteamento entre dois candidatos, detecção de
degradação por janela, fallback e recuperação com estabilidade), testado por mutação nas seis
regras. Depois, integração real com o sinal de saúde observado pelo `21-OBSERVABILITY`.

## O que este volume assume que pode mudar

O par único principal/fallback é o mínimo suficiente hoje — um esquema com múltiplos candidatos
ordenados por prioridade pode ser necessário conforme a diversidade de provedores cresce, sem
alterar o princípio central de degradação por amostra e recuperação com estabilidade.
