---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**L1 — O roteador escolhe apenas entre candidatos já aprovados por `26-AI-MODELS`; nunca decide
elegibilidade por conta própria.** *Consequência:* a fronteira entre "quem pode" (26) e "quem é
escolhido agora" (aqui) nunca se confunde.

**L2 — Candidato principal degradado aciona fallback automaticamente, sem bloquear esperando
recuperação quando alternativa aprovada existe.** *Consequência:* uma tarefa nunca fica
indisponível só porque o candidato principal está temporariamente degradado e um fallback já
aprovado está disponível.

**L3 — Toda decisão de roteamento é registrada, com candidato escolhido e motivo.**
*Consequência:* nenhuma decisão de roteamento é reconstruída por suposição depois — o motivo
específico (saudável, degradado, recuperado) está sempre disponível.

**L4 — Degradação é julgada por sinal acumulado numa janela mínima de amostra, nunca por uma
única falha isolada.** *Consequência:* ruído estatístico pontual não dispara fallback — só um
padrão sustentado de falha ou latência dispara.

**L5 — Recuperação do candidato principal exige janela de estabilidade, nunca volta no primeiro
sinal saudável isolado após um fallback.** *Consequência:* o roteador nunca alterna repetidamente
entre principal e fallback numa sucessão de trocas — o custo de ficar mais tempo no fallback é
menor que o custo de uma oscilação.

**L6 — O estado atual de roteamento por tarefa é sempre consultável.** *Consequência:* saber
qual candidato está ativo para uma tarefa nunca depende de inferir a partir de log — é uma
consulta direta e imediata.
