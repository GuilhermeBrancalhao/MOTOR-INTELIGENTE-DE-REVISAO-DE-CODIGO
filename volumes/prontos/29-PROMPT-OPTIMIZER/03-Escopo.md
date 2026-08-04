---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a busca automática de variante de prompt: geração de candidato, avaliação
contra amostra fixa de casos de ouro, critério de melhoria significativa, orçamento de busca, e
registro de toda tentativa.

**Fronteira com `07-PROMPT-ENGINE`.** O contrato do prompt, o versionamento, a máquina de estados
até PROMOVIDO, e os próprios casos de ouro usados como função objetivo são daquele volume. Este
volume nunca versiona nem promove — apenas propõe uma variante, que entra no fluxo do 07 como
qualquer outra proposta de mudança.

**Fronteira com `28-PROMPT-COMPILER`.** Compilar uma versão promovida em payload concreto de
provedor é daquele volume. Este volume nunca compila — a variante que ele propõe só é compilada
depois de passar pelo 07 e ser promovida como qualquer outra versão.

Como o `07-PROMPT-ENGINE` reaproveitado aqui já reconhece (`ROADMAP.md`, grupo 1), a distinção
central entre os três volumes deste grupo é *o que cada um faz com um prompt*: o 07 define o
contrato, o 28 compila o payload, este volume propõe variante — nenhum dos três faz o trabalho do
outro.

Não cobre estratégia específica de geração de candidato (busca aleatória, busca guiada por
modelo, mutação de template) — o volume trata do processo de avaliação e controle da busca,
independente de qual estratégia gera os candidatos.
