---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-08-03
---

# Conclusão

Este volume define o motor de execução de um agente de IA como uma máquina de estados fechada,
não como um prompt que "decide o que fazer" sem limite. O contrato central — uma ação por passo,
orçamento em três dimensões independentes verificado antes de cada decisão do modelo, motivo de
encerramento sempre explícito — existe para que um agente nunca rode indefinidamente, nunca
esconda por que parou, e nunca tenha erro de ferramenta tratado como se não tivesse acontecido.

O que o leitor deve levar embora: a diferença entre "o agente terminou" e "o agente terminou por
quê" não é detalhe de log — é a informação que decide se um resultado é confiável, parcial, ou
deveria ser descartado. E a fronteira com `09-ORCHESTRATOR` (uma execução versus coordenação de
várias) é o que impede este motor de crescer para tentar resolver dois problemas ao mesmo tempo
com uma única interface.

Este volume passa nos quatro critérios da Definição de PRONTO: gate estrutural verde, os 14
testes de `exemplos/08-agent-engine` passando, auditoria registrada em
`auditorias/VOL-08-auditoria-2026-08-03.md` e registro datado no `CHANGELOG.md`.
