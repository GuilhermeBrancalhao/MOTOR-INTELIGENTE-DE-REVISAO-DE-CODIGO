---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 10-Anti-Patterns
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Anti-Patterns

**Verificar orçamento só entre execuções completas, não entre passos.** Um agente que consome
todo o orçamento de tempo dentro de uma única chamada de ferramenta lenta nunca é interrompido
se a verificação só acontece "depois que a execução terminar" — a verificação tem que acontecer
a cada passo, inclusive durante a espera por uma ferramenta.

**Deixar o modelo decidir quando parar sem limite estrutural independente.** Confiar
inteiramente no modelo para "saber quando encerrar" é apostar que o modelo nunca vai entrar em
loop de tentativa repetida sem progresso — o que acontece na prática com frequência suficiente
para justificar um guardião de orçamento que não depende do julgamento do próprio modelo que
está sendo limitado.

**Tratar todo erro de ferramenta como não recuperável.** Isso transforma qualquer falha
transitória (timeout de rede, rate limit) em encerramento imediato, desperdiçando a capacidade
do modelo de tentar de novo ou tentar outra abordagem — a distinção entre recuperável e não
recuperável em `08-Modelos.md` existe justamente para não perder essa capacidade.

**Misturar múltiplas ações por passo "para ser mais eficiente".** Permitir que o modelo chame
duas ferramentas no mesmo passo parece economizar uma rodada de decisão, mas quebra a garantia
de ordem causal linear na trilha — se as duas ações falham de formas relacionadas, não há como
saber qual causou o quê sem essa ordem.

**Silenciar o motivo de encerramento no resultado devolvido ao chamador.** Um motor que devolve
só "resultado: X" sem dizer se X veio de objetivo atingido ou de orçamento excedido empurra a
ambiguidade para quem consome o resultado, que normalmente não tem contexto suficiente para
notar a diferença — a informação só existe no momento do encerramento, e se não for propagada
ali, se perde.
