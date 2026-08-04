---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Taxa de incompatibilidade de versão detectada, por integração.** Fonte: log do verificador de
versão. Qualquer ocorrência não-zero merece investigação imediata — significa que o outro lado
mudou contrato sem coordenação prévia, e a taxa ajuda a identificar quais integrações são mais
propensas a mudança não anunciada.

**Taxa de chamadas idempotentes que devolveram resultado em cache versus que executaram de
fato.** Fonte: log do aplicador de idempotência. Uma taxa alta de cache sustentada pode indicar
retry excessivo por timeout mal calibrado, não necessariamente falha real do sistema externo.

**Tempo em cada estado do circuit breaker, por integração**, ao longo do tempo. Fonte:
transições registradas do `CircuitBreaker`. Uma integração que passa muito tempo em `ABERTO` é
candidata a revisão de contrato com o fornecedor, ou a busca de alternativa, dependendo da
criticidade da funcionalidade que depende dela.

**Distribuição de latência de cada integração externa**, comparada ao timeout configurado. Fonte:
tempo de resposta de cada chamada bem-sucedida. Um timeout configurado muito acima do p99 real
observado desperdiça tempo de espera desnecessário em caso de falha; muito abaixo do p95 gera
timeout de chamadas que teriam sucedido com só um pouco mais de tempo.

**Proporção de aberturas de circuito que de fato correspondiam a degradação real do sistema
externo**, versus falsos positivos por limiar mal calibrado. Fonte: correlação entre abertura de
circuito e confirmação externa (por exemplo, status page do fornecedor) de indisponibilidade real
no mesmo período. Uma proporção baixa de correspondência sugere que o limiar de abertura está
sensível demais para variação normal de latência, não para degradação real.
