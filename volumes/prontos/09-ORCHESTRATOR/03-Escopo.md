---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-03
---

# Escopo

## Dentro deste volume

A mecânica de coordenação de um DAG de nós: ordenação topológica, execução paralela de nós sem
dependência pendente entre si, política de falha por nó (abortar, pular dependentes, retry com
backoff), fan-out/fan-in, e detecção de ciclo antes de iniciar qualquer execução. O contrato
entre o orquestrador e cada nó (o que o orquestrador espera de um nó: entrada, saída, e um sinal
de sucesso/falha) — não o que o nó faz internamente.

## Fora deste volume, e para onde vai

**A execução interna de um nó que é um agente de IA** é `08-AGENT-ENGINE` — este volume trata
essa execução como uma caixa-preta que recebe entrada e devolve saída ou falha; não sabe nada
sobre loop de tool-calling, orçamento de passos, ou motivo de encerramento do agente (embora
esse motivo possa influenciar a política de falha que este volume aplica ao nó).

**Workflows que misturam etapas de IA com etapas determinísticas como padrão de desenho
recorrente** (aprovação humana no meio, transformação de dados entre etapas) é `10-WORKFLOW` —
esse volume consome a mecânica de DAG deste volume, mas adiciona semântica específica de
"quando uma etapa é IA e quando não é" que este volume não precisa conhecer.

**Seleção de modelo ou ferramenta dentro de um nó de agente** é assunto de `08` e dos volumes que
`08` consome (`27-LLM-ROUTER`) — este volume não decide nada sobre o que acontece dentro de um nó.

**Persistência do estado do grafo entre reinícios do processo orquestrador** é uma preocupação de
infraestrutura tratada em `19-DEVOPS`/`20-CLOUD` quando aplicável — este volume define o contrato
de estado (qual nó está em qual status), não onde esse estado é armazenado fisicamente.

## Fronteira deliberada

Este motor não sabe otimizar a ordem de execução por custo ou latência esperada — ele só garante
que a ordem respeita as dependências declaradas. Otimização de agendamento (qual nó executar
primeiro entre vários prontos, quando há limite de concorrência) é extensão possível, registrada
como pendente em `16-Roadmap.md`, não parte do contrato mínimo.
