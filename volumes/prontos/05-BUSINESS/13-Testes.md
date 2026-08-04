---
volume: "05"
volume_nome: BUSINESS
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

## Estratégia

Testar este processo exige simular os dois pontos de travamento do fluxograma (`06-Fluxogramas`)
explicitamente: objetivo sem critério de falsificação e discordância entre stakeholders com
autoridade — não só o caminho onde tudo concorda e passa de primeira.

## O que a suíte precisa cobrir

Classificação de autoridade: um teste que tenta atribuir duas classificações à mesma pessoa para
o mesmo objetivo e verifica rejeição (B1). Falsificabilidade: um teste com critério vazio e um
teste com critério presente, confirmando que só o segundo é aceito (B2). Validação por autoridade:
um teste que tenta validar objetivo com stakeholder `CONSULTADO` e verifica rejeição — só
`DECIDE` valida (B3). Discordância: um teste com dois `DECIDE` propondo objetivos incompatíveis,
verificando que o sistema registra a discordância em vez de escolher um lado (B4).

## Prova por mutação

Um teste forte para B3 é um que falha se alguém trocar a checagem de `DECIDE` por "qualquer
stakeholder com objetivo proposto" — mutação que abriria a possibilidade de um `INFORMADO`
validar objetivo sozinho, quebrando a garantia central do processo.

## Testes de integração com volumes vizinhos

O objetivo validado por este processo alimenta `03-DISCOVERY` e `04-REQUIREMENTS` como entrada —
um teste de integração relevante verifica que um objetivo rejeitado por falta de falsificabilidade
nunca chega a esses dois volumes como se fosse válido.

## O que a suíte não cobre ainda

Concordância implícita entre dois `DECIDE` que propõem objetivos parecidos mas não idênticos
textualmente (por exemplo, dois enunciados que medem a mesma coisa com palavras diferentes) — o
exemplo atual compara objetivos por igualdade estrutural, o que classificaria dois enunciados
equivalentes como discordância. Registrado como lacuna honesta, não como bug: resolver isso
exigiria uma noção de equivalência semântica que o exemplo mínimo não tenta implementar.
