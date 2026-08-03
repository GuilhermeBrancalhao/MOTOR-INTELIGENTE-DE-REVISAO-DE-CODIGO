---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 14-Metricas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Métricas

**Tempo em `Pendente` versus tempo em `Executando`, por nó.** Fonte: timestamps de transição na
trilha. Um nó que passa muito tempo em `Pendente` está gargalado por dependência, não por
execução própria — otimizar a execução desse nó não reduziria o tempo total do grafo; otimizar
a dependência que ele espera, sim.

**Taxa de sucesso de retry por número de tentativa.** Fonte: trilha de nós com política
`RetryComBackoff`, segmentada por qual tentativa (1ª, 2ª, 3ª) teve sucesso. Se a maioria dos
sucessos vem só na última tentativa configurada, o número de tentativas pode estar subdimensionado
para o tipo de falha transitória real observada.

**Proporção de execuções de grafo terminando em sucesso total, sucesso parcial, e falha total.**
Fonte: `status_por_no` agregado por execução. Uma proporção alta de sucesso parcial pode ser
aceitável (se os ramos que falham não são críticos) ou pode indicar que a política de falha de
algum nó está configurada errada para a criticidade real daquele ramo — a métrica por si só não
decide, mas aponta onde investigar.

**Largura efetiva de paralelismo alcançada, comparada ao limite de concorrência configurado.**
Fonte: contagem de nós simultaneamente em `Executando` ao longo do tempo de uma execução. Se a
largura efetiva raramente se aproxima do limite configurado, o grafo tem menos paralelismo real
disponível do que o limite sugere — sinal de que o desenho do grafo, não a configuração do
motor, é o que limita o tempo total.
