---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**G1 — Toda decisão automatizada que afeta pessoa tem dono responsável nomeado.**
*Consequência:* "a IA decidiu" nunca é resposta final para "quem é responsável" — sempre existe
uma pessoa ou papel organizacional nomeado.

**G2 — Todo caso de uso é classificado por nível de risco antes de entrar em produção, e a
classificação determina os controles aplicáveis.** *Consequência:* nenhum caso de uso de alto
impacto é tratado com o mesmo rigor mínimo de um trivial — o nível de risco decide o rigor.

**G3 — Decisão de risco alto ou crítico exige revisão humana antes de tomar efeito.**
*Consequência:* automação de ponta a ponta nunca é aceitável para o nível de risco mais alto,
independente de quão confiante o modelo esteja na própria resposta.

**G4 — Toda decisão automatizada que afeta pessoa é registrada em trilha de auditoria imutável.**
*Consequência:* qualquer decisão é reconstruível depois — o que entrou, qual modelo decidiu, e
qual foi a decisão — sem depender de memória ou log incompleto.

**G5 — Caso de uso novo exige aprovação explícita antes de produção.** *Consequência:* nenhum
caso de uso entra em produção como efeito colateral silencioso de uma funcionalidade mais ampla.

**G6 — Classificação de risco e dono responsável são revisados periodicamente, nunca fixados uma
única vez.** *Consequência:* um caso de uso cujo impacto real cresceu com a escala de uso é
reclassificado antes que a governança fique desatualizada em relação à realidade.
