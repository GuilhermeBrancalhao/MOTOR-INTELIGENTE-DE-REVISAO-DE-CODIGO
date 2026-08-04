---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Taxa de descarte por categoria, sobre o total de itens candidatos daquela categoria.** Fonte:
registro de `Descarte`. Uma taxa alta persistente para uma categoria específica sugere que a
prioridade declarada não reflete a importância real percebida pelos usuários — sinal para
revisar `ORDEM_DE_PRIORIDADE`, não necessariamente aumentar o orçamento total.

**Frequência de acionamento de compactação, e proporção que de fato evita descarte
subsequente.** Fonte: log do gatilho de compactação. Uma compactação que aciona mas não evita
descarte na sequência sugere que a margem configurada é pequena demais para o volume real de
crescimento do histórico entre acionamentos.

**Número de recusas por instrução de prioridade máxima excedendo o orçamento sozinha.** Fonte:
log de recusa (C6). Qualquer ocorrência não-zero é sinal de erro de configuração a corrigir
imediatamente — esse caso nunca deveria ser normal em operação madura.

**Tokens efetivamente usados sobre orçamento total declarado, ao longo do tempo.** Fonte:
`JanelaMontada.tokens_usados`. Uma proporção consistentemente baixa sugere orçamento
superdimensionado (oportunidade de reduzir custo); consistentemente próxima do limite sugere
risco de descarte frequente não ainda manifestado como problema visível.

**Tamanho médio da instrução de sistema, ao longo de mudanças de versão do prompt.** Fonte:
tokens de itens de categoria `INSTRUCAO_SISTEMA`. Uma tendência de crescimento sustentado é o
sinal antecipado mais direto de risco de aproximação do Caso 4 (`12-Exemplos.md`) — revisar antes
que o crescimento force uma recusa em produção é mais barato que descobrir o problema depois.
