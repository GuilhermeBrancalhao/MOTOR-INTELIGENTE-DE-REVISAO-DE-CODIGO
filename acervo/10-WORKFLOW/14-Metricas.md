---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 14-Metricas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Métricas

**Tempo médio em `AguardandoSinal`, segmentado por tipo de sinal.** Fonte: diferença entre
timestamp de entrada e saída desse estado, por workflow. Um tempo de aprovação humana muito
maior que o esperado pelo processo de negócio é sinal para revisar o processo de aprovação, não
o motor — mas o motor é a fonte confiável desse dado, porque grava o timestamp exato de cada
transição.

**Taxa de saída de IA rejeitada por validação de formato, por passo.** Fonte: contagem de
rejeições do validador dividida pelo total de execuções daquele passo. Uma taxa alta e
persistente num passo específico sugere que o schema declarado não está alinhado com o que o
modelo de fato produz de forma confiável — motivo para revisar o prompt daquele passo, não só
aumentar o limite de tentativas de correção automática.

**Taxa de reexecução por retomada versus execução ininterrupta.** Fonte: contagem de passos
marcados como reexecutados numa retomada, comparada ao total de passos executados. Uma taxa alta
sugere falhas de infraestrutura frequentes o bastante para justificar investigação — o motor
absorve a reexecução de forma segura, mas reexecução frequente ainda tem custo real de tempo e,
para passos de IA, de tokens.

**Distribuição de tempo total de workflow, decomposta por passo.** Fonte: soma dos intervalos
entre checkpoints consecutivos. Essa decomposição aponta se o tempo total é dominado por espera
de sinal externo (processo de negócio) ou por execução de passo em si (motor) — as duas
categorias pedem intervenções completamente diferentes.
