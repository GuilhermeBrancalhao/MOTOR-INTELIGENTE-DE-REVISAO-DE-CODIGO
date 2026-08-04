---
volume: "05"
volume_nome: BUSINESS
tipo: PROCESSO
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

## Dentro deste volume

Identificação de stakeholder com autoridade de decisão explícita (decide/consultado/informado),
captura de objetivo de negócio mensurável e falsificável, e o processo de resolver discordância
entre stakeholders com autoridade antes de prosseguir para descoberta técnica.

## Fora deste volume, e para onde vai

**O que falta saber para especificar tecnicamente o sistema** é `03-DISCOVERY` — este volume
entrega a esse motor o objetivo já validado por quem tem autoridade; `03-DISCOVERY` não precisa
(e não deveria) resolver discordância de negócio, só lacuna de especificação técnica.

**O requisito verificável do sistema** é `04-REQUIREMENTS` — este volume entrega o critério de
sucesso do negócio; aquele volume traduz esse critério em enunciados falsificáveis sobre o
comportamento do sistema. Um requisito sem objetivo de negócio por trás é requisito órfão, e um
objetivo de negócio sem requisito que o implemente é intenção não realizada.

**Planejamento de projeto e sequenciamento de entrega** é `38-PROJECT-PLANNER` — este volume não
decide quando cada parte é entregue, só o que precisa ser verdade para a entrega inteira ser
considerada bem-sucedida por quem decide.

**Arquitetura técnica da solução** é `02-CORE` e os volumes de arquitetura — este volume nunca
prescreve tecnologia ou desenho técnico, mesmo quando um stakeholder tenta introduzir preferência
técnica disfarçada de objetivo de negócio (ver `10-Anti-Patterns.md`).

## Fronteira deliberada

Este volume não decide o objetivo por conta própria quando stakeholders com autoridade discordam
— ele torna a discordância visível e força uma decisão explícita, registrada, mas quem decide
continua sendo quem tem autoridade, nunca o processo de captura em si.
