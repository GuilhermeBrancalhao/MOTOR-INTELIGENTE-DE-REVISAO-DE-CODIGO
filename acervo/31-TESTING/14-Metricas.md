---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 14-Metricas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Métricas

**Proporção de testes de regressão de regra que têm prova de mutação registrada** (comentário ou
changelog de teste), sobre o total de testes que afirmam proteger uma regra específica. Fonte:
revisão manual ou convenção de comentário padronizada. Uma proporção baixa não significa
necessariamente que os testes não protegem nada — significa que a evidência da prova não foi
preservada, o que é, em si, um problema de confiabilidade da suíte para quem vem depois.

**Taxa de rastreabilidade regra-teste**: proporção de invariantes declaradas em `07-Regras.md` de
qualquer volume com pelo menos um teste correspondente identificável pelo nome. Fonte: comparação
entre a lista de invariantes e a lista de nomes de teste. Uma invariante sem teste correspondente
é lacuna que `07-Regras.md` deste próprio volume trata como registro obrigatório, não omissão
silenciosa.

**Frequência de "teste ajustado para passar" versus "teste revelou regressão real"** em revisão
de mudança de código que quebrou teste existente. Fonte: histórico de revisão de código
(mensagem de commit, discussão de revisão). Uma frequência alta do primeiro tipo é sinal de que a
suíte está sendo mantida "verde" às custas de proteção real, o padrão que `10-Anti-Patterns.md`
trata como o mais silenciosamente perigoso.

**Cobertura de teste de fluxo completo** — proporção de sistemas com mais de um componente
interagente que têm pelo menos um teste de composição na ordem real de uso, sobre o total de
sistemas com essa característica. Esta métrica, diferente de cobertura de linha de código, mede
diretamente se a classe de bug "cada peça funciona isolada, a composição não" está sendo
verificada.
