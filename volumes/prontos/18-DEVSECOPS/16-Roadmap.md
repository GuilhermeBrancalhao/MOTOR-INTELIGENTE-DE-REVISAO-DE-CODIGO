---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Notificação automática antes da expiração de um waiver (hoje a expiração só é percebida quando a
próxima avaliação do gate acontece, reativamente).

Métrica agregada de "idade da lacuna" por controle sem verificação automatizada — hoje a lacuna é
visível por avaliação individual, mas não há acompanhamento de quanto tempo um controle
específico permanece sem enforcement.

Integração com o processo de revisão periódica de waivers ativos (a boa prática existe na seção
09, mas o mecanismo que a torna automática, em vez de depender de alguém lembrar, ainda não está
formalizado).

## Ordem de cobertura pretendida

Primeiro, o gate de referência mínimo (avaliação de controle, waiver com expiração), testado por
mutação nas seis regras. Depois, integração real com o pipeline descrito em `19-DEVOPS` como
etapa concreta do fluxo de entrega.

## O que este volume assume que pode mudar

O modelo de waiver por controle único (um waiver cobre um controle) é o mínimo suficiente hoje —
um esquema que permita waiver por escopo mais amplo (por exemplo, por repositório ou por
ambiente) pode ser necessário conforme o número de controles cresce, sem alterar o princípio
central de bloqueio por padrão com exceção explícita e temporária.
