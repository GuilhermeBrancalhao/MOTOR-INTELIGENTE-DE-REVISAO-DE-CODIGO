---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**C1 — Orçamento total de tokens é declarado explicitamente, nunca implícito.**
*Consequência:* um sistema sem essa declaração descobre o limite por truncamento em produção, não
por decisão de desenho.

**C2 — Ordem de prioridade entre categorias de conteúdo é declarada antes da pressão de
orçamento acontecer**, nunca decidida no momento em que o limite é atingido.
*Consequência:* descarte sob pressão, sem prioridade pré-definida, tende a remover o que estiver
"mais à mão" tecnicamente, não o que é de fato menos importante.

**C3 — Todo descarte é registrado com o que foi removido e por qual categoria de prioridade.**
*Consequência:* um sistema que trunca silenciosamente não tem como diagnosticar depois por que
uma resposta pareceu esquecer contexto relevante.

**C4 — Compactação é acionada com margem antes do limite, nunca no próprio limite.**
*Consequência:* compactação sem margem compete pelo espaço que está tentando liberar, podendo
falhar exatamente quando mais necessária.

**C5 — Este volume funciona independente de recuperação de conhecimento.** Documento recuperado
por `13-RAG`, se existir, compete pelo mesmo orçamento que qualquer outro conteúdo, sem
tratamento especial implícito. *Consequência:* um sistema sem RAG nenhum ainda precisa deste
volume para gerir orçamento de histórico de conversa.

**C6 — Instrução de prioridade máxima nunca é descartada silenciosamente, mas pode ser recusada
explicitamente se sozinha já exceder o orçamento total.** *Consequência:* esse caso raro é
tratado como erro de configuração a ser corrigido, não como situação normal de operação.
