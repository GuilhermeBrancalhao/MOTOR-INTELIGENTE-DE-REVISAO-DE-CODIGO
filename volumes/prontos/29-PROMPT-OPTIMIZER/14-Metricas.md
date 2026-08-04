---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de buscas que produzem ao menos uma proposta.** Uma proporção muito baixa pode
indicar que o gerador de candidatos não está explorando variação suficiente, ou que o limiar de
melhoria está calibrado alto demais para o tipo de mudança sendo tentada.

**Distribuição de taxa de acerto entre tentativas rejeitadas.** Revela quão perto (ou longe) as
tentativas descartadas ficaram do limiar — útil para calibrar o próprio limiar ao longo do tempo.

**Proporção de propostas deste volume que de fato são promovidas pelo 07, versus rejeitadas na
revisão.** Mede a qualidade real da busca automática comparada à barra que o 07 exige, não apenas
o resultado interno da otimização.

**Custo total de avaliação por busca (número de chamadas a `avaliar_variante`).** Contextualiza o
orçamento de tentativas (O4) contra o custo real — uma busca cara por tentativa exige um
orçamento mais conservador do que uma barata.


Nenhuma dessas métricas deveria ser otimizada isoladamente — uma proporção alta de propostas que
não são promovidas pelo 07, por exemplo, pode ser sinal de limiar de melhoria calibrado baixo
demais neste volume, não necessariamente um problema do processo de revisão do 07.

A leitura correta é sempre relativa e comparativa ao longo do tempo, nunca um julgamento definitivo baseado numa única medição isolada.