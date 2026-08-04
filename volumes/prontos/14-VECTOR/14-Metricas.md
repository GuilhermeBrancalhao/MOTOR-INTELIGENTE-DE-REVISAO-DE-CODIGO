---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Tempo de reindexação completa, medido por versão de modelo.** Fonte: timestamps do processo de
reindexação. Um tempo crescente ao longo de sucessivas reindexações sinaliza que o volume de
documentos está superando a capacidade de reindexação em tempo aceitável — sinal para revisar
infraestrutura antes que uma migração de modelo se torne inviável.

**Taxa de consultas rejeitadas por campo obrigatório ausente**, segmentada por qual campo faltou
(métrica, partição, versão). Fonte: log do validador de consulta. Uma taxa alta persistente numa
integração específica sugere bug de cliente, não frouxidão do índice — a resposta correta é
corrigir o cliente, nunca relaxar a validação.

**Proporção de resultados de busca filtrados por exclusão (V6) sobre o total de resultados brutos
antes do filtro.** Fonte: comparação entre resultado bruto e resultado pós-filtro. Uma proporção
alta sustentada sugere que o volume de documentos excluídos ainda fisicamente presentes está
crescendo mais rápido que a compactação — sinal para revisar a frequência de compactação física.

**Tamanho do índice antigo retido após reindexação, ao longo do tempo de retenção.** Fonte:
armazenamento do gestor de reindexação. Útil para calibrar o período de retenção: um período
longo demais desperdiça espaço; curto demais reduz a janela de reversão segura se um problema for
descoberto na versão nova.
