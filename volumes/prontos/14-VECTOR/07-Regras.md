---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**V1 — Embedding é versionado por modelo, e comparação só acontece entre vetores da mesma
versão.** *Consequência:* reindexação completa é necessária quando o modelo de embedding muda,
nunca mistura de versões no mesmo espaço de comparação.

**V2 — Métrica de similaridade é declarada explicitamente por índice e por consulta, nunca
assumida por padrão implícito.** *Consequência:* consulta sem métrica declarada é rejeitada, não
processada com uma suposição silenciosa.

**V3 — Partição isola coleções não relacionadas, e consulta sem partição declarada não tem
padrão implícito que a torne válida.** *Consequência:* cruzamento acidental de partição, que
misturaria resultado de coleções não relacionadas, é estruturalmente impossível, não só evitado
por convenção.

**V4 — O índice nunca decide o que fazer com o resultado da busca.** Ordenação final, filtro por
relevância e decisão de uso são sempre `13-RAG`. *Consequência:* um índice que reordena resultado
por critério próprio, além de proximidade vetorial, ultrapassou o próprio escopo.

**V5 — Reindexação é atômica do ponto de vista do consumidor.** *Consequência:* nunca existe
consulta que veja parte do índice antigo e parte do novo simultaneamente.

**V6 — Exclusão é real: documento excluído nunca é devolvido**, mesmo que a estrutura física
ainda não tenha compactado o espaço correspondente. *Consequência:* a garantia de exclusão opera
na consulta, não depende de quando a compactação física acontece.
