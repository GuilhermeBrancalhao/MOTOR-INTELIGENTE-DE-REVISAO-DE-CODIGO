---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de tarefas ativas com fallback declarado e testado.** Deveria ser 100% para tarefa
crítica — uma tarefa sem fallback verificado é risco não mitigado, mesmo que M3 exija a
declaração.

**Frequência de reavaliação de candidato ativo contra casos de ouro.** Reavaliação rara demais
significa que uma degradação silenciosa do fornecedor pode passar despercebida por muito tempo.

**Custo total por tarefa ao longo do tempo, comparado entre candidatos disponíveis.** Não uma
tabela de preço estática — uma comparação viva, recalculada conforme preço ou comportamento de
modelo mudam.

**Número de trocas de modelo sem motivo ou avaliação associada no histórico.** Deveria ser zero
por construção (M6 exige os dois campos); um valor acima de zero indica uma via de troca que
contornou `registrar_troca`.


Nenhuma dessas métricas deveria ser lida como valor absoluto fixo — todas fazem sentido apenas
como tendência observada ao longo do tempo, contra a linha de base do próprio sistema, nunca como
comparação direta contra um número publicado por um fornecedor externo sem data e contexto.

A métrica de custo total por tarefa, em particular, só é significativa quando comparada entre
candidatos avaliados na mesma janela de tempo — comparar um valor observado hoje contra um valor
registrado há meses mistura mudança real de comportamento com mudança de preço do fornecedor.