---
volume: "05"
volume_nome: BUSINESS
tipo: PROCESSO
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

O processo tem três etapas em sequência estrita, porque cada uma depende do resultado da
anterior de forma que invertê-las produz retrabalho: mapear stakeholders por autoridade primeiro
(sem isso não se sabe quem valida o objetivo), capturar o objetivo mensurável segundo (validado
por quem decide, não por quem só tem interesse), e só então liberar o objetivo para
`03-DISCOVERY` e `04-REQUIREMENTS` consumirem como entrada.

## Componentes

O **mapeador de autoridade** produz uma lista de stakeholders, cada um com exatamente uma
classificação — decide, consultado, informado — nunca mais de uma, porque autoridade ambígua é o
mesmo problema que autoridade não mapeada: ninguém sabe, na hora de aceitar ou rejeitar o
resultado, quem de fato pode fazer isso. O **capturador de objetivo** aplica o teste de
falsificabilidade a cada objetivo proposto e recusa objetivo que não passa, devolvendo para
refinamento em vez de aceitar como está. O **resolvedor de discordância** entra em ação quando
dois ou mais stakeholders com autoridade (não apenas interesse) propõem objetivos incompatíveis —
ele não decide, registra a discordância e força uma decisão explícita de quem tem autoridade
final, se existir uma hierarquia entre eles, ou escalona se não existir.

## Por que a ordem importa

Capturar objetivo antes de mapear autoridade é o erro mais comum e mais caro: o objetivo
capturado reflete a opinião de quem estava na sala, não de quem tem autoridade de fato — e a
correção, quando descoberta tarde, custa muito mais do que teria custado mapear autoridade
primeiro.
