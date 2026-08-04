---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Indexar documento antes de validar autoridade "para não atrasar o pipeline".** Isso inverte a
ordem que `04-Arquitetura.md` estabelece e permite que documento sem procedência confiável seja
recuperado por `13-RAG` antes de qualquer curadoria acontecer.

**Deixar documento expirado continuar sendo devolvido porque "ninguém teve tempo de remover do
índice".** A garantia de K2 é sobre o que a consulta devolve, não sobre quando o índice físico é
atualizado — um documento pode continuar fisicamente indexado enquanto a consulta já o trata como
expirado.

**Resolver conflito por ordem de chegada** (o último documento ingerido "vence" por padrão, sem
decisão explícita). Isso é exatamente o oposto de K3 — decisão implícita por acidente de tempo de
ingestão, não por autoridade nem por julgamento humano.

**Tratar toda divergência entre documentos como conflito a resolver com vencedor único.** Duas
fontes legítimas podem descrever o mesmo assunto de perspectivas diferentes sem que uma esteja
errada — forçar um vencedor nesses casos descarta informação válida.

**Renovar validade de documento automaticamente por decurso de tempo sem revisão.** Isso
contraria K6 diretamente: ausência de revisão deveria mover para expirado, não manter válido por
inércia.

**Tratar `fato_chave` como campo decorativo preenchido de forma inconsistente entre documentos.**
Se metade dos documentos usa "política de reembolso" e a outra metade usa "reembolso - política",
a detecção de conflito por agrupamento falha silenciosamente — os dois nunca são comparados,
mesmo tratando do mesmo fato.
