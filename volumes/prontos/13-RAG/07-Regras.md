---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**R1 — Toda afirmação na resposta final rastreia a um documento citado que de fato a sustenta.**
*Consequência:* afirmação sem essa rastreabilidade é removida da resposta ou a resposta inteira é
marcada como não confiável.

**R2 — Fidelidade é medida depois da geração, nunca assumida pela presença de citação.**
*Consequência:* uma resposta pode citar documentos reais e válidos e ainda ter baixa fidelidade,
se o conteúdo gerado extrapola o que os documentos de fato afirmam.

**R3 — Reordenação por relevância é passo distinto de recuperação por proximidade vetorial.**
*Consequência:* um documento pode ser recuperado (candidato) e não sobreviver à reordenação
(não relevante o suficiente), sem que isso seja falha do índice.

**R4 — Nenhuma resposta é gerada sem pelo menos um candidato válido, a menos que o sistema
recuse explicitamente por falta de fonte suficiente.** *Consequência:* silêncio explícito é
sempre preferível a resposta plausível sem fundamento.

**R5 — Este volume nunca cura fonte nem opera índice**, só consome os dois. *Consequência:* um
problema de fonte desatualizada é bug de `11-KNOWLEDGE`; um problema de busca incorreta é bug de
`14-VECTOR`; um problema de citação errada ou fidelidade baixa é bug deste volume.

**R6 — Validade de documento é confirmada no momento da consulta, não assumida do momento da
indexação.** *Consequência:* um documento pode ter expirado entre indexação e consulta, e a
citação final precisa refletir o estado atual, não o estado de quando foi indexado.
