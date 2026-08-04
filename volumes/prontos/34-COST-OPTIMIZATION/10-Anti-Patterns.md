---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Rastrear custo por chamada de API isolada, sem nunca agregar por tarefa de negócio completa.**
Viola U1 — o número resultante não responde a pergunta que realmente importa: quanto custa
realizar o trabalho que o sistema existe para fazer.

**Custo registrado sem escopo, acumulado num total geral que ninguém especificamente possui.**
Viola U2 — sem atribuição, ninguém tem incentivo nem responsabilidade de investigar quando o
custo cresce.

**Orçamento com apenas um limite rígido, sem alerta antecipado.** Viola U3 — a primeira notícia
de problema chega exatamente no momento em que já é tarde para reagir preventivamente.

**Aceitar uma mudança como "otimização de custo" só porque parece mais eficiente, sem medir gasto
real antes e depois.** Viola U5 diretamente — economia não validada é uma suposição, não um fato.

**Documentar uma tabela de preço específica por modelo como referência permanente no próprio
volume.** Viola U6 — esse tipo de número expira rápido e vira desinformação assim que o fornecedor
muda a tabela real.


**Somar custo de múltiplos escopos num único número "geral" antes de decidir onde investigar.**
Esconde exatamente a informação que tornaria a investigação eficiente — qual escopo específico
está crescendo mais que o esperado.

Esse anti-pattern é particularmente comum quando a pressão é apenas visualizar rapidamente um número no topo de um painel, sem considerar que a agregação prematura destrói justamente o detalhe mais útil.