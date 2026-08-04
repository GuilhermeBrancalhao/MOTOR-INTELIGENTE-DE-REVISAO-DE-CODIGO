---
volume: "39"
volume_nome: ROADMAP
tipo: PROCESSO
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`CriterioDePriorizacao.__post_init__` recusa criação sem `valor`, `risco` e `dependencia`
preenchidos — todo item de roadmap carrega critério de priorização explícito desde sua origem,
nunca adicionado depois como justificativa retroativa.

`ItemDeRoadmap.__post_init__` recusa um item marcado como `DIRECIONAL_LONGO_PRAZO` que também
declara `data_comprometida` — as duas coisas juntas seriam uma contradição: um item direcional,
por definição, ainda não tem certeza suficiente para sustentar uma data comprometida.

`Roadmap.registrar_fora_de_escopo` recusa um `ItemForaDeEscopo` sem motivo — a mesma disciplina
de `ROADMAP.md` deste acervo, onde cada item na seção "Fora de escopo" carrega explicação, nunca
apenas o nome do item descartado.

`Roadmap.sinalizar_decisao_de_autoridade` recusa uma `DecisaoQueExigeAutoridade` sem
`autoridade_necessaria` declarada — sinalizar que uma decisão está fora do escopo do processo
exige nomear especificamente quem (ou qual papel) tem autoridade para decidir, nunca apenas
"alguém precisa decidir isso".


Cada uma dessas quatro verificações acontece no momento da operação correspondente — adicionar
item, registrar item fora de escopo, sinalizar decisão, registrar revisão — nunca como validação
posterior que poderia ser esquecida sob pressão de manter o roadmap "parecendo" atualizado sem
de fato estar.

Essa disciplina de verificação imediata segue o mesmo padrão já consistentemente aplicado por outros volumes de processo deste acervo inteiro.

Isso reforça, no próprio comportamento do código, exatamente a garantia que a prosa das seções anteriores já descreve com todo o detalhe necessário.