---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — operação declarada corretamente pronta

Uma operação com SLO e estratégia de sobrecarga declarados é aceita por
`declarar_operacao_pronta` sem ressalva.

## Caso 2 — medição sob carga insuficiente é rejeitada

Uma medição com concorrência de apenas 2 requisições simultâneas, abaixo do mínimo realista
configurado, é rejeitada antes de qualquer verificação de SLO acontecer.

## Caso 3 — SLO de operação com IA sem margem declarada é rejeitado

Um `SLO` marcado como `envolve_chamada_de_ia=True`, mas com `p99_ms` igual a `p95_ms`, é
rejeitado — a variabilidade da chamada de IA não está refletida na margem entre os percentis.

## Caso 4 — regressão de desempenho detectada entre duas medições

Uma medição atual com p95 maior que a medição anterior, sob a mesma operação, produz um objeto
`Regressao` com os dois valores específicos.

## Caso 5 — otimização validada e otimização rejeitada

Uma mudança que reduz o p95 medido sob a mesma carga é aceita como otimização válida; a mesma
estrutura de teste, mas com p95 igual ou pior depois da mudança, é rejeitada.


Os cinco casos cobrem, juntos, os dois portões de prontidão (SLO, estratégia de sobrecarga) mais
os três mecanismos de verificação contínua (carga insuficiente, regressão, otimização) — a mesma
cobertura que os testes da seção seguinte confirmam individualmente, caso a caso.

Essa cobertura relativamente compacta ainda assim exercita cada uma das seis regras pelo menos uma vez, o padrão mínimo que este acervo espera de toda seção de exemplos.

Cada um dos cinco foi escolhido especificamente por corresponder a exatamente uma regra ou a um par de regras relacionadas, evitando exemplos redundantes que provariam a mesma coisa duas vezes.