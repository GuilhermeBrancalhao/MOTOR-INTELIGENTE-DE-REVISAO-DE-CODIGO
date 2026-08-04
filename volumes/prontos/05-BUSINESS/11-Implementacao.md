---
volume: "05"
volume_nome: BUSINESS
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/05-business/objetivo.py -->

`objetivo.py`, citado acima, formaliza as seis regras (B1-B6) em código: `Stakeholder` recusa
dupla classificação de autoridade (B1); `ObjetivoDeNegocio` exige um `criterio_de_falsificacao`
não vazio (B2); `validar_por` aceita só stakeholder com autoridade `DECIDE` (B3); discordância
entre dois `DECIDE` é registrada, nunca resolvida automaticamente (B4).

## Como o processo real aplicaria isto

A implementação mínima é um formulário estruturado, não um documento de texto livre: campo de
classificação de autoridade obrigatório por stakeholder, campo de critério de falsificação
obrigatório por objetivo proposto, e um passo de validação que recusa salvar o objetivo enquanto
o critério estiver vazio — a mesma disciplina de `04-REQUIREMENTS`, aplicada uma camada acima.

A ordem de implementação recomendada é: modelo de dado (`Stakeholder`, `ObjetivoDeNegocio`)
primeiro, testado contra os seis cenários de violação de regra. Processo de captura (formulário
ou entrevista estruturada) depois, consumindo o modelo já validado. Integração com
`03-DISCOVERY`/`04-REQUIREMENTS` por último — este volume produz o objetivo validado como entrada
para os dois, não consome nada deles.

## Onde a integração com outros volumes acontece

O objetivo validado por `Processo.validar` é o dado que `03-DISCOVERY` recebe como ponto de
partida — aquele motor não reabre a pergunta de quem tem autoridade, assume que este processo já
resolveu isso. Da mesma forma, `04-REQUIREMENTS` recebe o `criterio_de_falsificacao` do objetivo
como a âncora contra a qual cada requisito técnico deveria, em algum grau, se justificar — um
requisito que não serve a nenhum objetivo validado é candidato a requisito órfão, tratado em
`10-Anti-Patterns.md` daquele volume.
