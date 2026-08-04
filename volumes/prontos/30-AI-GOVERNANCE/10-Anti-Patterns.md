---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Caso de uso lançado em produção como parte de uma funcionalidade maior, sem classificação de
risco própria.** Viola G2 e G5 ao mesmo tempo — o caso de uso de IA específico nunca passou pelo
próprio gate de governança, escondido dentro de uma entrega mais ampla.

**"A IA decidiu" como resposta final numa investigação de decisão questionada.** Viola G1
diretamente — sempre existe um dono responsável nomeado, e é essa pessoa ou papel que deveria
responder pela decisão, não o modelo em abstrato.

**Decisão de alto risco marcada como revisada por humano sem revisão de fato ter acontecido,
"porque a IA geralmente acerta".** Viola G3 na essência, mesmo que tecnicamente marque o campo
como verdadeiro — a revisão precisa ser real, não apenas registrada como tendo acontecido.

**Trilha de auditoria que registra só a decisão final, sem o dado de entrada nem o modelo que a
produziu.** Viola G4 — uma decisão sem contexto suficiente para reconstrução não é auditável de
verdade, mesmo que tecnicamente exista um registro.

**Classificação de risco definida uma vez no lançamento e nunca revisitada, mesmo com o caso de
uso crescendo em escala e impacto.** Viola G6 — a governança fica presa a uma fotografia antiga
da realidade.
