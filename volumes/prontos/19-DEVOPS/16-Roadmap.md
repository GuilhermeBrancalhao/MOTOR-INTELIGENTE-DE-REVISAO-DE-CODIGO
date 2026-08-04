---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Critério automático de promoção entre percentuais de rollout gradual (hoje o incremento é uma
decisão externa ao pipeline, não uma regra baseada em sinal de observabilidade medido
automaticamente).

Rollback automático disparado por métrica de degradação, sem intervenção humana — hoje a decisão
de reverter é sempre externa ao mecanismo, que apenas executa a reversão quando solicitada.

Coordenação de deploy entre múltiplos serviços com dependência entre si — hoje o pipeline trata
um artefato por vez, sem modelar ordem de deploy quando duas mudanças em serviços diferentes
precisam ser sequenciadas.

## Ordem de cobertura pretendida

Primeiro, o pipeline de referência mínimo (estágios ordenados, rollout gradual, reversão),
testado por mutação nas seis regras. Depois, integração real com sinal de `21-OBSERVABILITY`
como gatilho de decisão de reversão.

## O que este volume assume que pode mudar

O conjunto fixo de cinco estágios (BUILD, TESTE, SEGURANCA, STAGING, PRODUCAO) é o mínimo
suficiente hoje — um pipeline mais complexo pode precisar de estágios adicionais (por exemplo,
aprovação manual explícita antes de produção), sem alterar o princípio central de sequência não
pulável com bloqueio em falha.
