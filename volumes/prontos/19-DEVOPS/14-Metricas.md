---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de deploys que usaram rollout gradual versus deploy completo justificado.** Mede se
P3 está sendo respeitado na prática, não apenas disponível como opção.

**Tempo entre a decisão de reverter e a reversão de fato completada.** Mede se o caminho de
reversão (P2) está de fato rápido o suficiente para conter um incidente, não apenas
tecnicamente disponível.

**Número de tentativas de deploy rejeitadas por estágio fora de ordem ou por pipeline
incompleto.** Um número consistentemente maior que zero indica processo ou ferramenta tentando
contornar o pipeline, não erro pontual — vale investigar a causa, não apenas celebrar que o
bloqueio funcionou.

**Frequência de rollback.** Não é, por si só, um indicador ruim — mede se o processo está
detectando e corrigindo problemas, e um número muito baixo pode indicar rollout gradual demais
lento para gerar sinal, tanto quanto detecção de problema falhando.


Nenhuma dessas métricas substitui o resultado de um deploy específico — elas existem para revelar
tendência: se a proporção de deploy gradual está caindo, se o tempo de reversão está subindo, algo
no processo mudou e vale investigar antes que um incidente real torne a resposta urgente.


A combinação das quatro métricas conta uma história maior do que qualquer uma isoladamente: alta
frequência de rollback com tempo de reversão baixo é um processo funcionando como projetado;
a mesma alta frequência com tempo de reversão crescente é sinal de que o mecanismo de reversão
não está sendo exercitado o suficiente fora de incidentes reais para permanecer rápido.