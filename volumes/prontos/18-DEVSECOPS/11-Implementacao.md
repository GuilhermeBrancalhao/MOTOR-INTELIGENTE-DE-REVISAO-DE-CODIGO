---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/18-devsecops/gate.py -->

`gate.py`, citado acima, formaliza D1-D6: `Controle` sem `verificacao_automatizada` é reportado
como lacuna, não como aprovado (D1/D6); `GateDeSeguranca.avaliar` bloqueia por padrão toda falha
sem waiver ativo (D2); um `Waiver` cuja `expira_em` já passou é tratado como inexistente, sem
remoção manual (D3); o gate roda contra o conjunto completo de controles a cada chamada,
correspondendo a "toda mudança" em vez de agendado (D4); `ResultadoGate` carrega o vetor de risco
de cada falha bloqueante (D5).

O gate não executa as verificações em si — ele recebe um dicionário de resultados já produzidos
por scanners, testes ou ferramentas externas específicas de cada controle, e apenas consolida
essas entradas contra a política de bloqueio e waiver. Essa separação é deliberada: acoplar o
gate à execução de cada verificação tornaria impossível testar sua lógica de decisão (bloquear,
liberar por waiver, registrar lacuna) sem depender das ferramentas reais de cada controle
individual, que variam de scanner de dependência a teste de integração.

A comparação de data em `Waiver.esta_ativo` usa ordenação lexicográfica de string no formato
`YYYY-MM-DD` propositalmente, em vez de um tipo de data dedicado — o formato ISO garante que a
comparação textual coincide com a comparação cronológica, e evita introduzir dependência de fuso
horário numa decisão que só precisa responder "hoje já passou do prazo declarado?". Essa escolha
mantém o exemplo livre de dependência externa, sem abrir mão de correção.