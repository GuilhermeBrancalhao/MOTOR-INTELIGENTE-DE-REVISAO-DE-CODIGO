---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Normalizar ou converter vetores de métricas diferentes "para permitir a comparação".** Isso
mascara exatamente o erro que V2 existe para prevenir — a conversão produz um número que parece
válido, mas não corresponde a nenhuma medida de similaridade real entre os documentos originais.

**Deixar consulta sem partição declarada usar um padrão "todas as partições".** Isso parece
conveniente e é exatamente o cruzamento acidental que V3 proíbe — um documento de uma coleção não
relacionada pode aparecer num resultado sem que ninguém tenha decidido isso de propósito.

**Reindexar em produção, sobrescrevendo o índice atual, em vez de construir em paralelo e trocar
atomicamente.** Isso expõe estado inconsistente exatamente durante o período mais sensível — a
transição entre versões de índice.

**Confiar que exclusão física acontece rápido o suficiente para nunca precisar de filtro
explícito.** Compactação física de índice vetorial pode ser cara e assíncrona por desenho; um
sistema que assume exclusão imediata sem o filtro de V6 devolve documento excluído durante a
janela entre exclusão lógica e compactação física.

**Deixar o índice decidir corte de relevância** (por exemplo, "só devolver resultado acima de um
score mínimo") como parte da busca em si, em vez de devolver os N mais próximos e deixar
`13-RAG` decidir o corte. Isso mistura a responsabilidade de V4 com julgamento de relevância que
pertence ao consumidor.
