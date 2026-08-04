---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`Medicao` carrega os componentes nomeados do indicador — `regras_totais`,
`regras_com_prova_de_mutacao`, `cobertura_de_linha` — como campos separados, nunca um único
`score` opaco. `taxa_prova_de_mutacao()` é a métrica primária derivada; `cobertura_de_linha`
existe como dado complementar, mas nunca decide sozinha o resultado do gate.

`GateDeQualidade.verificar` usa exclusivamente a taxa de prova por mutação contra
`limiar_minimo` — uma medição com cobertura de linha alta mas taxa de prova baixa ainda falha o
gate, porque cobertura de linha nunca substitui prova de regra na decisão.

`ItemDeDivida` recusa sua própria criação sem os quatro campos preenchidos — descrição, motivo do
adiamento, data de registro, custo estimado — tornando dívida técnica registrada de forma
incompleta estruturalmente impossível.

`detectar_regressao` compara as duas medições mais recentes de um `HistoricoDeQualidade` e
retorna um objeto explícito quando a taxa cai — nunca um booleano genérico que esconderia os
números específicos da queda.


Essa separação entre métrica primária (taxa de prova) e dado complementar (cobertura de linha)
existe estruturalmente no próprio tipo `Medicao`, não apenas como convenção documental — quem lê
o código do gate confirma diretamente que `cobertura_de_linha` nunca entra na condição de
bloqueio.

Essa transparência estrutural é o que torna H1 uma garantia verificável por leitura, não apenas uma promessa em prosa que poderia divergir silenciosamente do comportamento real.