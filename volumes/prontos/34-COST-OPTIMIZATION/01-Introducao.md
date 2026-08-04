---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Este é um volume perecível (regra 9 de `00-INTRODUCAO/Convencoes.md`), como `26-AI-MODELS` e
`27-LLM-ROUTER`. Nenhum preço específico entra aqui como fato duradouro — o volume descreve o
método de medir, atribuir e otimizar custo, nunca uma tabela de valor que expiraria antes de ser
lida por muito tempo.

`26-AI-MODELS` já estabelece que comparação de custo entre modelos deveria ser pela tarefa
completa, nunca por preço unitário isolado (M4 daquele volume). Este volume estende esse mesmo
princípio para o acompanhamento contínuo de gasto real: custo é medido e atribuído por tarefa
concluída, nunca por chamada isolada sem contexto, e todo escopo (equipe, produto, ambiente) tem
orçamento declarado com alerta antes do limite, não descoberto só depois de já ter sido excedido.

`27-LLM-ROUTER` já declara explicitamente que não é tabela de custo — este volume é onde essa
responsabilidade de fato mora: rastrear gasto real, atribuí-lo a um dono, alertar antes do limite,
acompanhar tendência ao longo do tempo, e validar toda decisão de redução de custo por medição
real, nunca por suposição de que uma mudança "obviamente" custaria menos.

O mesmo cuidado com piso de substância do gate estrutural, já discutido em 26 e 27, vale aqui: a
regra de volume perecível restringe o que pode ser dito como fato duradouro, não quanto texto é
necessário para explicar o método com profundidade suficiente.