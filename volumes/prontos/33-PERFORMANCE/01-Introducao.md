---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Desempenho medido apenas em ambiente controlado, com um usuário e dado de teste, não prediz
comportamento sob carga real — concorrência revela contenção de recurso que uma medição isolada
nunca encontraria. E um sistema com componente de IA carrega uma complicação adicional: parte de
sua latência vem de uma chamada cuja duração é inerentemente variável, o que exige um orçamento de
desempenho que reconheça essa variabilidade em vez de tratá-la como a mesma coisa que a latência
previsível de uma operação determinística.

Este volume trata do processo de definir, medir e proteger orçamento de desempenho: todo
operação declara um alvo de latência antes de ser considerada pronta para produção, a medição
acontece sob carga que se aproxima da realidade, regressão de desempenho recebe o mesmo rigor de
investigação que regressão de qualidade, o sistema degrada graciosamente sob sobrecarga em vez de
falhar catastroficamente, e toda otimização é validada por medição, nunca assumida como
funcionando só porque parece mais rápida.

`25-API-ARCHITECT` já exige orçamento de latência declarado por endpoint síncrono; este volume
formaliza o processo mais amplo por trás dessa exigência — como o orçamento é definido, medido sob
carga, e o que acontece quando ele é violado ou quando o sistema precisa degradar sob sobrecarga.
