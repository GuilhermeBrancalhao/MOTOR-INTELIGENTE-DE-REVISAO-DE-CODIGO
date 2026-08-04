---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Taxa de rejeição na ingestão por falta de autoridade.** Fonte: log do validador. Uma taxa alta
persistente sugere que a fonte de documentos não está preparada para declarar origem
adequadamente — sinal para revisar o processo de origem, não para relaxar a exigência de K1.

**Proporção de documentos em cada estado de ciclo de vida** (válido, expirando, expirado).
Fonte: consulta ao gestor de ciclo de vida. Uma proporção crescente de "expirando" sem
revalidação correspondente é sinal de que a capacidade de curadoria não acompanha o volume de
documentos que precisam de revisão periódica.

**Tempo médio entre sinalização de conflito e resolução pelo curador.** Fonte: timestamps do
registro de conflito. Um tempo muito longo significa que documentos conflitantes ficam mais tempo
sem prevalência decidida, aumentando a chance de `13-RAG` recuperar informação inconsistente
nesse intervalo.

**Número de conflitos resolvidos por "coexistência" versus "vencedor único".** Fonte: registro de
resolução. Essa proporção é diagnóstica de quão frequentemente divergência real (não conflito) é
tratada como se fosse conflito — uma proporção muito baixa de coexistência pode indicar que
`10-Anti-Patterns.md` (forçar vencedor único sempre) está acontecendo na prática.

**Proporção de documentos com `fato_chave` preenchido sobre o total.** Fonte: varredura da base.
Uma proporção muito baixa pode ser legítima (muitos documentos de referência geral) ou pode
indicar que a detecção de conflito está subutilizada porque ninguém está preenchendo o campo —
a métrica sozinha não distingue os dois casos, precisa de leitura qualitativa junto.
