---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de controles declarados no 17 com verificação automatizada correspondente.** Mede
diretamente a lacuna entre política e enforcement que D1/D6 tornam visível — o objetivo é essa
proporção subir ao longo do tempo, nunca ficar oculta.

**Número de waivers ativos por controle, e idade média até expiração.** Um controle com waivers
recorrentes e renovados é sinal de que a política ou o processo em volta dele precisa mudar, não
que a exceção deveria virar permanente.

**Tempo entre a falha de um gate e a correção que a resolve (não o waiver, a correção real).**
Mede se o processo está de fato prevenindo risco cedo, ou apenas adiando com waivers sucessivos.

**Contagem de bypass fora do mecanismo de waiver, se detectável na configuração do pipeline.**
Idealmente zero — qualquer ocorrência é o anti-pattern mais grave deste volume acontecendo na
prática, e deveria ser tratada como incidente de processo.

Nenhuma dessas métricas substitui a leitura do resultado individual de um gate — elas existem para
revelar tendência ao longo do tempo (a lacuna está diminuindo? os waivers estão sendo renovados
sem revisão?), não para julgar uma mudança específica, que é sempre decidida pelo resultado binário
do próprio gate.

Uma queda súbita na contagem de falhas bloqueantes, sem correspondência em melhoria real do
código, é sinal de alerta tão relevante quanto um aumento — pode indicar que verificações
deixaram de rodar, não que os controles passaram a ser respeitados de fato.