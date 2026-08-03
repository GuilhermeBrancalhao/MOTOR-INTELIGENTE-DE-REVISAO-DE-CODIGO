---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-03
---

# Exemplos

## Caso 1 — objetivo atingido em três passos

Um agente recebe o objetivo "responder quantos itens estão em estoque para o produto X". Passo
1: o modelo decide chamar a ferramenta de consulta de estoque com o argumento do produto. Passo
2: a ferramenta devolve a quantidade; o modelo recebe a observação e decide que já tem a
informação necessária. Passo 3: o modelo devolve resposta final com a quantidade. O motor
encerra com `OBJETIVO_ATINGIDO`, orçamento consumido de 3 dos N passos disponíveis — bem abaixo
do limite, o caso comum para tarefas simples e bem definidas.

## Caso 2 — orçamento de tempo excedido por ferramenta lenta

O mesmo objetivo, mas a ferramenta de consulta de estoque está degradada e demora 40 segundos
para responder, contra um orçamento de tempo de parede de 30 segundos para a execução inteira. O
guardião de orçamento detecta o limite excedido durante a espera pela ferramenta — não depois
que ela responde — e encerra com `ORCAMENTO_EXCEDIDO` antes mesmo de o passo 1 ser concluído com
observação. O chamador recebe um resultado sem `saida`, e a trilha registra que o motivo foi
tempo, não passos nem erro — informação que orienta a investigação para "a ferramenta está
lenta", não para "o agente está em loop".

## Caso 3 — erro recuperável seguido de sucesso

A ferramenta de consulta de estoque falha no passo 1 com timeout de rede (marcado como
recuperável). A observação de erro volta ao modelo no passo 2, que decide tentar a mesma
ferramenta de novo. No passo 3, a ferramenta responde com sucesso, e o passo 4 devolve a
resposta final. O motor encerra com `OBJETIVO_ATINGIDO`, mas a trilha mostra 4 passos em vez dos
3 do caso 1 — a diferença nos registros de trilha entre os dois casos é exatamente a evidência de
que o erro aconteceu e foi recuperado, sem precisar de nenhum campo adicional além do que
`08-Modelos.md` já define.
