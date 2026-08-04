---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o mecanismo de roteamento em tempo de execução: escolha entre candidatos já
aprovados, detecção de degradação por janela de sinal, fallback automático, janela de
estabilidade para recuperação, e estado consultável.

**Fronteira com `26-AI-MODELS`.** A lista de candidatos elegíveis, com avaliação e fallback
declarado, vem daquele volume — este volume nunca decide sozinho que um modelo é elegível; ele
escolhe entre o que já chegou aprovado.

**Fronteira com `34-COST-OPTIMIZATION`.** Este volume não é uma tabela de custo nem otimiza
roteamento por preço — a decisão aqui é sobre saúde e disponibilidade do candidato, não sobre
qual é mais barato. Otimização de custo agregado, incluindo possível roteamento sensível a
orçamento, é daquele volume.

**Fronteira com `16-INTEGRATION`.** A robustez da chamada individual a um provedor — retry,
timeout, circuit breaker — é daquele volume, aplicada a cada candidato individualmente. Este
volume decide qual candidato recebe a chamada; o 16 garante que a chamada em si é robusta.

Como volume perecível, não fixa nome de modelo, provedor ou número de janela como valor
duradouro — qualquer exemplo numérico é ilustração de método, não configuração recomendada.


Essas três fronteiras (26, 34, 16) cobrem as três formas mais comuns de um roteador crescer além
do que deveria: decidir elegibilidade sozinho (invadindo o 26), otimizar por preço em vez de
saúde (invadindo o 34), ou tentar reimplementar retry e circuit breaker por dentro do roteador
em vez de confiar no que o 16 já garante por chamada individual.