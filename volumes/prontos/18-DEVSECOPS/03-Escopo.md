---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o processo de enforcement contínuo: o gate que roda os controles do 17 a cada
mudança, o mecanismo de exceção com prazo, e o registro de qual controle falhou e por quê.

**Fronteira com `17-SECURITY`.** O 17 fica com a política — quais controles existem, que risco
cada um mitiga, e a definição de verificação (a coluna "como é verificado" da matriz de
controles do 17). Este volume fica com o processo — a automação que roda essa verificação em
toda mudança, o bloqueio por padrão, e a exceção com prazo. Um controle novo no 17 sem check
automatizado correspondente aqui é uma lacuna deste volume, não do 17.

**Fronteira com `31-TESTING` e `32-QUALITY`.** Teste de segurança não é uma categoria separada de
teste — é teste, escrito e mantido pela mesma prática que o 31 descreve. Este volume não redefine
como se escreve teste; define que resultado de segurança bloqueia por padrão, enquanto outras
categorias de teste podem ter política de bloqueio diferente, decidida pelo 32.

**Fronteira com `19-DEVOPS`.** O pipeline de entrega em si — como uma mudança vai do commit ao
deploy — é do 19. Este volume define uma etapa específica desse pipeline (o gate de segurança),
não o pipeline inteiro.

Não cobre a definição de política de segurança em si, nem a infraestrutura de execução do
pipeline (agente de CI, orquestração de job) — apenas o comportamento do gate: o que ele verifica,
quando bloqueia, e como uma exceção é concedida e expira.
