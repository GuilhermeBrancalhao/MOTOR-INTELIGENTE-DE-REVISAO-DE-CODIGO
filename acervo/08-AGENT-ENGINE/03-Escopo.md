---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 03-Escopo
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Escopo

## Dentro deste volume

O ciclo de vida de uma única execução de agente: inicialização com objetivo e ferramentas
disponíveis, o loop de decisão-ação-observação, orçamento de passos/tokens/tempo, e os critérios
de encerramento (objetivo atingido, orçamento excedido, erro não recuperável). O contrato entre
o motor e o modelo subjacente (o que é enviado, o que é esperado de volta) e entre o motor e cada
ferramenta chamada (como o resultado de uma ferramenta volta para o histórico do agente).

## Fora deste volume, e para onde vai

**Coordenação entre múltiplas execuções de agente** (sequencial, paralela, condicional, DAG de
dependência) é `09-ORCHESTRATOR` — este volume não sabe que existe mais de uma execução ao mesmo
tempo; cada execução é isolada do ponto de vista deste motor.

**Workflows determinísticos que combinam etapas de IA com etapas de código convencional** é
`10-WORKFLOW` — quando uma etapa é "chamar este agente", ela consome este motor como uma peça,
mas o workflow em si (a sequência de etapas, algumas com IA e outras sem) não é assunto daqui.

**Seleção e troca de modelo de linguagem por custo/latência** é `27-LLM-ROUTER` — este motor
recebe um modelo já selecionado e não decide entre provedores.

**Recuperação de conhecimento para dar contexto ao agente** é `13-RAG` e `11-KNOWLEDGE` — se um
agente usa uma ferramenta de busca que por sua vez usa RAG, o RAG é implementação da ferramenta,
não deste motor; este motor só sabe que uma ferramenta foi chamada e o que ela devolveu.

**Orçamento de janela de contexto** (o que cabe, o que é compactado) é `15-CONTEXT` — este volume
consome o orçamento de tokens como um número que `15` ajuda a calcular, mas não define como
compactar histórico.

## Fronteira deliberada

Este motor não decide *se* um agente deveria ser invocado — essa decisão é de quem o chama
(pode ser `09-ORCHESTRATOR`, pode ser código de aplicação fora do acervo). Da perspectiva deste
volume, "invocar" já é um fato consumado; o volume só executa o ciclo de vida a partir daí.
