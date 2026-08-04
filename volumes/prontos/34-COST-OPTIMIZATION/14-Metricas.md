---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Custo por tarefa por escopo, comparado ao longo de múltiplos períodos.** É a métrica central
deste volume — decompor por escopo permite localizar onde o custo está crescendo, não apenas que
cresceu em algum lugar do sistema.

**Proporção de custo atribuído a escopo específico versus custo sem atribuição clara.** Deveria
ser 100% por construção (U2 impede registro sem escopo) — uma queda indica falha no próprio
processo de registro.

**Frequência de estado ALERTA atingido por escopo, e tempo até ação corretiva.** Mede se o
alerta antecipado (U3) está de fato gerando reação a tempo, não apenas existindo como sinal
ignorado.

**Proporção de otimizações propostas que de fato validam economia real versus as que são
rejeitadas por falta de redução medida.** Mede a qualidade do processo de propor otimização, não
apenas o resultado de cada tentativa isolada.


Estas quatro métricas, lidas em conjunto, revelam se a disciplina de gestão de custo está sendo
seguida na prática — atribuição completa e alerta gerando reação a tempo são os dois sinais mais
diretos de que o processo está funcionando como projetado, não apenas existindo como formalidade.

A leitura combinada dessas quatro métricas, ao longo de múltiplos períodos consecutivos, é sempre mais informativa do que qualquer uma isolada tomada como julgamento definitivo único.