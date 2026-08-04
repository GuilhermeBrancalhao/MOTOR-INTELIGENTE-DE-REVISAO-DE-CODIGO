---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**I1 — Todo contrato de integração externa é versionado, e a versão é verificada antes de
consumir a resposta.** *Consequência:* mudança de contrato não anunciada pelo outro lado é
detectada como incompatibilidade explícita, não como erro de parsing silencioso mais adiante.

**I2 — Toda chamada externa com efeito colateral usa chave de idempotência.**
*Consequência:* retry por timeout ou erro de rede nunca duplica o efeito do lado externo, mesmo
quando não se sabe se a chamada original de fato falhou ou só a resposta se perdeu.

**I3 — Timeout e política de retry são declarados explicitamente por integração, nunca herdados
de padrão implícito da biblioteca cliente.** *Consequência:* cada integração externa tem
características próprias de latência e confiabilidade que exigem configuração própria, não uma
configuração genérica aplicada a todas.

**I4 — Falha de sistema externo é isolada, nunca se propaga como indisponibilidade do sistema
interno inteiro.** *Consequência:* um circuit breaker ou padrão equivalente protege o sistema
interno de degradação em cascata quando uma dependência externa específica falha.

**I5 — Este volume não trata chamada entre camadas do mesmo produto**, sob o mesmo controle de
release. *Consequência:* a pergunta "o outro lado pode mudar sem que eu saiba antes?" decide se
uma chamada específica pertence a este volume ou a `22`-`25`.

**I6 — Mudança de contrato de integração que este sistema expõe para outros é sempre versionada,
nunca um breaking change silencioso na mesma versão.** *Consequência:* consumidores externos de
uma integração que este sistema oferece têm a mesma garantia que este volume exige de
integrações que ele consome.
