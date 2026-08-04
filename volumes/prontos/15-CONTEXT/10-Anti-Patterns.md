---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Deixar orçamento implícito, "o que couber cabe".** Isso adia a descoberta do limite para o
momento de falha em produção, exatamente o oposto de C1 — orçamento declarado permite testar o
comportamento de descarte antes que ele aconteça de forma inesperada.

**Definir prioridade por ordem de código, não por decisão explícita de negócio.** Se a categoria
que "por acaso" é adicionada primeiro no código do gestor acaba com prioridade mais alta sem
ninguém ter decidido isso deliberadamente, a prioridade real do sistema é acidente de
implementação, não decisão de desenho.

**Truncar histórico silenciosamente sem registro do que foi removido.** Um usuário que percebe o
sistema "esquecendo" algo dito antes não tem como confirmar se foi truncamento (removível por
ajuste de orçamento) ou limitação real do modelo — a ausência de registro esconde a causa.

**Acionar compactação só quando o limite já foi atingido**, sem margem. Isso é o oposto direto de
C4, e o sintoma é compactação que falha ou é abortada precisamente no momento em que mais seria
necessária, porque não sobrou orçamento para ela operar.

**Dar tratamento especial implícito a documento recuperado por RAG**, como se ele tivesse
prioridade automática sobre histórico só por vir de um pipeline de recuperação. Isso viola C5 —
documento recuperado compete pelo mesmo orçamento que qualquer outro conteúdo, com prioridade
declarada como qualquer categoria, nunca por status especial não declarado.
