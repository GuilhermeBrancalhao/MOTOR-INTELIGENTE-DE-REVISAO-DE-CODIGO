---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**K1 — Todo documento carrega autoridade de origem explícita.** *Consequência:* documento sem
essa informação é rejeitado na ingestão, nunca aceito "por enquanto".

**K2 — Documento expirado nunca é devolvido como válido por consulta padrão.**
*Consequência:* consumidor que precisa de histórico usa consulta explicitamente marcada como tal.

**K3 — Conflito entre documentos sobre o mesmo fato é sinalizado para decisão humana, nunca
resolvido implicitamente pelo ranqueamento de recuperação.** *Consequência:* dois documentos
conflitantes que chegam ao índice sem essa resolução produzem resposta inconsistente que parece
aleatória a quem consome, quando na verdade reflete indecisão não resolvida na fonte.

**K4 — Falha de ingestão é evento registrado, nunca ausência silenciosa.**
*Consequência:* um documento que devia estar na base e não está precisa ter um motivo
rastreável, não só a ausência.

**K5 — Curadoria decide o que entra; recuperação (13-RAG) decide o que sai numa resposta
específica.** *Consequência:* a mesma base de documentos válidos pode produzir respostas
diferentes para consultas diferentes sem que isso implique falha de curadoria.

**K6 — Revalidação de documento expirando é ação explícita do curador, nunca renovação
automática por decurso de tempo sem revisão.** *Consequência:* um documento não permanece válido
só porque ninguém teve tempo de revisá-lo — a ausência de revisão o move para expirado, não o
mantém válido por omissão.
