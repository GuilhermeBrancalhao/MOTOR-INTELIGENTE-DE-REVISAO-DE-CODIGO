---
volume: "38"
volume_nome: PROJECT-PLANNER
tipo: PROCESSO
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Ordenar tarefas por facilidade percebida em vez de dependência real, deixando dependência
crítica para depois "porque é mais difícil".** Viola Z1 — cedo ou tarde a execução esbarra na
dependência não resolvida, geralmente no pior momento possível.

**Estimativa de número único apresentada como se fosse certeza, sem faixa nem confiança
declarada.** Viola Z2 — cria expectativa que a estimativa nunca teve fundamento real para
sustentar.

**Aceitar tarefa adicional no meio do ciclo sem renegociar escopo, "porque é rápido".** Viola Z3
— múltiplas pequenas adições não renegociadas se acumulam até o escopo real ser irreconhecível em
relação ao originalmente negociado.

**Continuar reportando uma tarefa como "em andamento" quando na verdade está bloqueada esperando
algo externo.** Viola Z5 — esconde a real necessidade de escalação atrás de um status que sugere
progresso normal continuando a acontecer.

**Marcar tarefa como concluída porque o prazo chegou, sem verificar se o critério de pronto foi
de fato atingido.** Viola Z6 — o mesmo problema, em miniatura, de qualquer afirmação não
verificada tratada como fato.


**Revisar o plano apenas na retrospectiva do fim do ciclo, nunca durante a execução quando a
divergência de fato aconteceu.** Adia a correção de curso para um momento em que ela já não pode
mais influenciar o resultado do ciclo corrente, apenas o próximo.