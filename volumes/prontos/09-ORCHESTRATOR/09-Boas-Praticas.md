---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-03
---

# Boas Práticas

**Declarar dependência explícita mesmo quando a ordem "provavelmente" já sai correta por acaso.**
Confiar em ordem observada empiricamente entre nós sem aresta declarada quebra na primeira vez
que o motor mudar a estratégia de agendamento interno — a garantia formal é só sobre dependência
declarada.

**Preferir `PularDependentes` a `AbortarDependentes` quando os ramos do grafo são de fato
independentes em valor de negócio.** Abortar o grafo inteiro por falha de um ramo que não afeta
o resultado de outros ramos desperdiça trabalho que já teria sucesso — a escolha da política
correta por nó é uma decisão de custo, não uma configuração padrão única para todo o grafo.

**Tornar nós idempotentes sempre que possível**, especialmente os que serão alvo de retry. Um nó
que produz efeito colateral não-idempotente (por exemplo, criar um registro sem verificar se já
existe) executado duas vezes por um retry produz duplicata — a idempotência é responsabilidade
de quem implementa o nó, este motor não a impõe.

**Limitar a profundidade de fan-out para um número conhecido e testado**, não deixar o número de
nós paralelos crescer sem limite a partir de um dado de entrada variável. Um fan-out de tamanho
não controlado (por exemplo, "um nó por item de uma lista de tamanho desconhecido") pode saturar
o limite de concorrência configurado e degradar o comportamento de todo o grafo, não só do ramo
que gerou o fan-out.

**Medir tempo de espera em `Pendente` separadamente de tempo em `Executando`.** Um nó que passa
muito tempo em `Pendente` está esperando dependência, não executando — misturar as duas métricas
esconde se o gargalo é de dependência ou de execução própria (ver `14-Metricas.md`).
