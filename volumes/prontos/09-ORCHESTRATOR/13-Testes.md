---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-03
---

# Testes

## Estratégia

Testar este motor exige grafos de teste com formas conhecidas — linear, fan-out simples, fan-out
com fan-in, diamante (dois caminhos que convergem), e grafo com ciclo introduzido de propósito.
Cada nó de teste é uma função fake com comportamento programado (sucesso imediato, falha
recuperável seguida de sucesso, falha definitiva), o que permite testar o motor sem depender de
nós reais como agentes ou chamadas externas.

## O que a suíte precisa cobrir

Cada transição do `stateDiagram-v2` em `06-Fluxogramas.md` precisa de um teste que a alcance,
incluindo a transição menos óbvia: `Pendente → Abortado` por dependência falha, que só é testável
com um grafo de pelo menos dois nós onde o segundo depende do primeiro. A prova de que a ordem
entre nós paralelos não é garantida determinística (mas a ordem de dependência é) exige um teste
que executa o mesmo grafo várias vezes e verifica que a ordem de dependência se mantém em todas
as execuções, mesmo que a ordem dentro de um mesmo nível de paralelismo varie.

## Prova por mutação

Um teste forte para "fan-in só libera com todas as dependências em Sucesso" é um que falha se
alguém alterar a condição para "qualquer dependência em Sucesso" (OU em vez de E) — testável
construindo um grafo com três dependências, uma delas falhando, e verificando que o nó de
agregação nunca entra em `Pronto`. Sem esse teste específico, uma regressão que trocasse E por OU
passaria despercebida em qualquer teste que só usasse grafos onde todas as dependências têm
sucesso.

## Testes de integração com volumes vizinhos

Como um nó pode ser uma execução de `08-AGENT-ENGINE`, um teste de integração relevante verifica
que a tradução de `MotivoEncerramento` do agente para `Sucesso`/`Falha` deste motor está correta
nos três casos (`OBJETIVO_ATINGIDO` → `Sucesso`; `ORCAMENTO_EXCEDIDO` e `ERRO_NAO_RECUPERAVEL` →
`Falha`, cada um preservando o motivo original na trilha para auditoria posterior).
