---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Compactação com geração de resumo real (usando modelo para resumir histórico antigo) — o exemplo
mínimo trata compactação como descarte com registro, sem cobrir a variante que produz resumo
substituto do conteúdo original; essa variante introduziria uma chamada adicional ao modelo que
o exemplo não modela.

Orçamento dinâmico ajustado por tipo de tarefa — hoje o orçamento total é fixo por sistema; uma
tarefa que sabidamente precisa de mais espaço para histórico (uma conversa longa planejada) versus
uma tarefa pontual poderia ter orçamento diferenciado, não coberto neste ciclo.

Priorização dentro da mesma categoria (por exemplo, qual documento recuperado específico descartar
primeiro quando múltiplos da mesma categoria competem) — hoje a prioridade é só entre categorias;
dentro de uma categoria, a ordem de descarte não está especificada.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (`ItemDeContexto`, `Orcamento`, descarte por prioridade),
testado por mutação nas seis regras. Depois, integração real com `13-RAG` para confirmar que a
tradução de documento recuperado para item de contexto preserva informação suficiente para
diagnóstico de descarte.

## O que este volume assume que pode mudar

O conjunto de cinco categorias fixas pode crescer conforme sistemas reais expõem necessidade de
categorias adicionais (por exemplo, "resumo de sessão anterior" como categoria própria, distinta
de histórico recente) — a regra de que toda categoria nova precisa de posição explícita na
prioridade permanece independente de quantas categorias existirem.
