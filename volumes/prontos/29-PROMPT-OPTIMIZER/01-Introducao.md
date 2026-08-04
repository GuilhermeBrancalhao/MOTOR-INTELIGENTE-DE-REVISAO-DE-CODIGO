---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

`07-PROMPT-ENGINE` decide quando uma versão de prompt está pronta para produção — versionada,
avaliada contra caso de ouro, promovida. Esse processo, por padrão, é conduzido por uma pessoa
escrevendo e ajustando o corpo do prompt manualmente. Este volume trata de uma forma diferente de
chegar a uma versão melhor: busca automática de variante, usando os mesmos casos de ouro do 07
como função objetivo, gerando candidatos e comparando cada um contra a versão atual sob o mesmo
critério que decidiria se um humano tivesse escrito aquela variante à mão.

A tentação central que este volume existe para conter é a busca que "descobre" melhoria movendo o
próprio critério de avaliação, não o prompt — um otimizador que ajusta a função objetivo para
favorecer o que ele já encontrou não está otimizando nada, está enganando a si mesmo. A segunda
tentação é a busca que promove sua própria descoberta diretamente, pulando a barreira de revisão
que o 07 impõe a toda versão nova, automática ou não.

Este volume nunca promove nada — ele propõe. `07-PROMPT-ENGINE` continua sendo o único lugar onde
uma versão de prompt se torna PROMOVIDO, e `28-PROMPT-COMPILER` continua sendo o único lugar onde
uma versão promovida vira payload real. A busca automática deste volume produz apenas mais uma
versão candidata, tratada exatamente como qualquer outra proposta de mudança de prompt.
