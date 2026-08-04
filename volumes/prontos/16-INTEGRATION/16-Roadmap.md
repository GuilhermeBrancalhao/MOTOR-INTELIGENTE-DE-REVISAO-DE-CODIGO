---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Descoberta automática de depreciação de versão de contrato (por exemplo, consultando changelog
do fornecedor programaticamente) — hoje a detecção de incompatibilidade é reativa, só acontece
quando uma resposta de fato chega com versão diferente da esperada.

Estratégia de fallback quando circuit breaker está aberto (por exemplo, resposta em cache
degradada, ou funcionalidade alternativa) — este volume garante que a falha é isolada, mas não
especifica o que o sistema interno deveria fazer funcionalmente enquanto uma integração crítica
está indisponível.

Coordenação de versão entre múltiplos consumidores da mesma integração dentro do mesmo sistema —
hoje cada chamador declara sua própria versão mínima esperada, sem mecanismo central que garanta
consistência entre diferentes partes do sistema que consomem a mesma integração externa.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (verificação de versão, idempotência, circuit breaker),
testado por mutação nas seis regras. Depois, integração real com `27-LLM-ROUTER` como caso
concreto de integração externa que se beneficiaria diretamente desta camada de robustez.

## O que este volume assume que pode mudar

O modelo de versão `major.minor` (I1) é o mínimo suficiente hoje — um esquema mais expressivo
(versionamento semântico completo, com `patch`) pode ser necessário para integrações com
granularidade de mudança mais fina, sem alterar o princípio central de verificação explícita
antes de consumir.
