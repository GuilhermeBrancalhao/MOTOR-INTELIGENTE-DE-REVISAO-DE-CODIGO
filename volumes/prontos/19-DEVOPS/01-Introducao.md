---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Uma mudança de código só tem valor quando chega a produção — e o caminho entre o commit e a
produção é, ele mesmo, uma superfície de risco tão real quanto o código que percorre esse
caminho. Um pipeline que permite deploy direto "só desta vez, é urgente" reintroduz exatamente os
riscos que build, teste e gate de segurança existem para prevenir; um deploy que substitui 100%
do tráfego de uma vez transforma qualquer defeito não capturado antes em um incidente de escala
total, em vez de um incidente contido; um deploy sem caminho de reversão testado transforma um
problema de minutos em um problema de horas, porque a reversão só é inventada durante o
incidente, sob pressão.

Este volume trata do pipeline de entrega em si — a sequência não pulável de estágios que uma
mudança atravessa, a estratégia de rollout que limita o raio de impacto por padrão, e a garantia
de que o artefato testado é exatamente o artefato implantado, nunca reconstruído no caminho.

`18-DEVSECOPS` é uma etapa deste pipeline, não um processo paralelo a ele — o gate de segurança
roda dentro da sequência que este volume define, na posição que a ordem de estágios determina.
`20-CLOUD` trata da infraestrutura que hospeda o sistema em execução; este volume trata de como
uma mudança chega até essa infraestrutura.
