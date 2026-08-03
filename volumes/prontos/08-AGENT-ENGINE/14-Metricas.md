---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-03
---

# Métricas

**Distribuição de passos consumidos até encerramento por objetivo atingido.** Fonte: trilha de
cada execução, filtrando por `MotivoEncerramento.OBJETIVO_ATINGIDO`. Esta é a métrica que
calibra o orçamento de passos — um p95 muito próximo do limite configurado sugere orçamento
apertado demais para a complexidade real das tarefas; um p95 muito abaixo sugere espaço para
reduzir o limite sem perder cobertura de casos legítimos.

**Taxa de encerramento por orçamento excedido, segmentada por dimensão (passos, tokens,
tempo).** Fonte: contagem de `MotivoEncerramento.ORCAMENTO_EXCEDIDO` por dimensão que disparou o
guardião. Uma taxa alta numa dimensão específica aponta onde investigar primeiro — se é tempo,
provavelmente ferramenta lenta; se é passos, provavelmente objetivo mal definido ou tarefa maior
que o esperado.

**Taxa de recuperação de erro** — proporção de execuções que tiveram pelo menos um erro
recuperável na trilha e ainda assim encerraram por objetivo atingido, sobre o total de execuções
com pelo menos um erro recuperável. Fonte: varredura da trilha por execução. Uma taxa baixa
sugere que os erros classificados como "recuperáveis" não estão de fato sendo recuperados na
prática, e a classificação em `08-Modelos.md` merece revisão.

**Latência por passo, decomposta em tempo de decisão do modelo versus tempo de execução de
ferramenta.** Fonte: timestamp de cada `Passo` na trilha. Essa decomposição é o que permite
saber se um orçamento de tempo apertado está sendo consumido pela decisão do modelo ou pela
execução das ferramentas — e são otimizações completamente diferentes (a primeira aponta para
`27-LLM-ROUTER`, a segunda para a ferramenta específica).
