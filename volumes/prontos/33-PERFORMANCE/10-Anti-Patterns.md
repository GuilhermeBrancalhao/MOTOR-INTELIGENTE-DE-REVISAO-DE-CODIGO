---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Medir desempenho apenas em ambiente de desenvolvimento local, sem carga concorrente.** Viola J2
— não revela nenhuma contenção de recurso que só aparece sob múltiplas requisições simultâneas.

**SLO de operação com chamada de IA fixado igual ao de uma operação puramente determinística.**
Viola J6 — a variabilidade real da chamada de IA vai violar esse orçamento com frequência,
tornando o SLO inútil como alvo prático.

**Sistema que falha completamente para toda requisição assim que a capacidade é excedida, sem
nenhuma estratégia de degradação.** Viola J4 diretamente — o dano de uma sobrecarga se espalha
para todo usuário, em vez de ser contido.

**Aceitar uma mudança como otimização porque "faz sentido teoricamente ser mais rápida", sem
medir.** Viola J5 — otimização não validada por medição é uma suposição, não um fato.

**Regressão de desempenho detectada e ignorada repetidamente, cada vez atribuída a "ruído" sem
verificação.** Viola J3 — depois de algumas repetições, o "ruído" pode ser uma tendência real
sendo normalizada silenciosamente.


**Declarar SLO uma vez e nunca revisar, mesmo com o sistema mudando significativamente de
escala.** Um SLO calibrado para o volume de tráfego de meses atrás pode já não refletir a
realidade atual, tanto para mais quanto para menos exigente.