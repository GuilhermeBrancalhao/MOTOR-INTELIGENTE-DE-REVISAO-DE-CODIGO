---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Trocar de modelo "porque saiu uma versão nova", sem rodar os casos de ouro contra ela antes.**
Viola M2 diretamente — a novidade de uma versão não é evidência de que ela atende à barra de
qualidade que a tarefa exige.

**Tarefa crítica com um único modelo e nenhum fallback declarado.** É exatamente o cenário que M3
existe para evitar — a tarefa fica tão disponível quanto o modelo principal, sem alternativa.

**Comparar modelos só pelo preço por token anunciado, sem considerar tokens ou tentativas
necessárias na prática.** Pode levar à escolha de um modelo mais caro na prática, mesmo parecendo
mais barato no papel.

**Documentar preço ou limite de modelo específico como se fosse fato permanente do produto.**
Viola M5 — esse tipo de número expira rápido e, sem data e fonte, vira desinformação assim que
o fornecedor muda a tabela.

**Trocar o modelo de uma tarefa em produção sem deixar registro de quando e por quê.** Torna
impossível, mais tarde, correlacionar uma mudança de comportamento observada com a troca que a
causou.


**Fixar, em código ou documentação de longa duração, uma tabela de preço por modelo.** Viola M5
diretamente — esse tipo de tabela expira antes que a maioria das pessoas perceba que já expirou.