---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — orçamento suficiente, sem descarte

Uma janela com limite de 8000 tokens recebe instrução do sistema (500 tokens), histórico recente
(2000 tokens) e três documentos recuperados (1500 tokens no total) — soma de 4000 tokens, dentro
do orçamento. Nenhum descarte acontece, e a janela é montada com todo o conteúdo.

## Caso 2 — descarte por prioridade quando o orçamento é excedido

A mesma configuração, mas o histórico recente cresce para 6000 tokens ao longo da conversa,
somando 8500 tokens no total — acima do limite de 8000. O gestor descarta primeiro os documentos
recuperados (prioridade mais baixa entre os três tipos presentes), registrando o descarte com
motivo. Se isso ainda não bastar, descartaria histórico mais antigo antes de tocar na instrução
do sistema, que tem prioridade máxima.

## Caso 3 — compactação acionada antes do limite

Um histórico de conversa longa se aproxima do limite com margem de 1000 tokens configurada. Ao
atingir essa margem (não o limite em si), o gestor aciona compactação do histórico mais antigo,
resumindo os primeiros turnos da conversa em um resumo mais curto — liberando espaço antes que
qualquer descarte forçado se torne necessário, com a compactação tendo orçamento disponível para
operar sem competir pelo espaço que está tentando liberar.

## Caso 4 — instrução sozinha excede o orçamento

Uma mudança de configuração reduz o orçamento total de 8000 para 500 tokens, mas a instrução de
sistema continua com 800 tokens (não ajustada para a nova configuração). A montagem da janela
recusa explicitamente com `OrcamentoExcedidoPelaInstrucao`, em vez de tentar acomodar parcialmente
a instrução ou descartar outras categorias até sobrar espaço insuficiente — o erro aponta
diretamente para a causa raiz (configuração incompatível), não para um sintoma downstream.
