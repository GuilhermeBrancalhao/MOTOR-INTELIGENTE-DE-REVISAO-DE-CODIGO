---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-03
---

# Escopo

## Dentro deste volume

A declaração de workflow como sequência (não necessariamente linear — pode ter ramificação
condicional) de passos tipados, cada um determinístico ou de IA; o checkpoint de estado gravado
depois de cada passo; a validação de saída de passo de IA contra o formato esperado pelo próximo
passo; e a retomada de um workflow interrompido a partir do último checkpoint, sem reexecutar
passos já concluídos.

## Fora deste volume, e para onde vai

**A mecânica genérica de DAG de nós independente de semântica de IA/determinístico** é
`09-ORCHESTRATOR` — este volume consome aquela mecânica quando o workflow tem passos paralelos,
mas adiciona a semântica específica de "este passo é IA, precisa de validação de saída" que
`09` não conhece.

**A execução interna de um passo que invoca um agente de IA** é `08-AGENT-ENGINE` — um passo de
workflow que usa agente delega a execução daquele passo específico para aquele motor; o workflow
só vê entrada e saída do passo, não o loop interno do agente.

**Aprovação humana como gate explícito dentro do workflow** é modelada como um tipo de passo que
pausa a execução até receber um sinal externo — o mecanismo de "esperar por sinal externo" é
parte deste volume, mas a interface de aprovação em si (tela, notificação) é responsabilidade de
quem integra este motor, não deste volume.

**Compensação/rollback de passos já concluídos quando um passo posterior falha** (o padrão saga)
é registrado como pendência em `16-Roadmap.md` — o contrato mínimo atual não especifica
compensação automática, só retomada a partir de checkpoint.

## Fronteira deliberada

Este motor não decide dinamicamente a próxima sequência de passos com base em julgamento livre
de um modelo — mesmo passos condicionais são declarados com a condição explícita na definição do
workflow. Decisão de sequência não declarada a priori é `09-ORCHESTRATOR`, com agentes decidindo
seus próprios próximos passos.
