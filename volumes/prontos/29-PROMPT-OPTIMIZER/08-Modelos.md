---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`Variante` carrega apenas `nome` e `corpo` — nenhum campo de estado de promoção, porque decidir
promoção nunca é responsabilidade de um objeto deste volume.

`ResultadoDeAvaliacao` carrega `amostra_usada` junto de `taxa_acerto` — não apenas o resultado
numérico, mas a prova de qual amostra o produziu, o que torna O1 auditável depois: qualquer pessoa
revisando um resultado consegue confirmar que a mesma amostra foi de fato usada.

`HistoricoDeBusca` é uma lista simples de `ResultadoDeAvaliacao`, sem distinção estrutural entre
tentativa aprovada e rejeitada — as duas vivem juntas no mesmo histórico, e a distinção entre elas
é sempre calculável a partir do `taxa_acerto` registrado, nunca perdida por serem guardadas em
lugares diferentes.


Nenhum dos três tipos centrais (`Variante`, `ResultadoDeAvaliacao`, `HistoricoDeBusca`) conhece o
conceito de "promovido" — essa palavra nem aparece no vocabulário deste módulo, o que é
proposital: promoção pertence exclusivamente ao vocabulário e à máquina de estados do 07.

Essa ausência de vocabulário é uma escolha deliberada de design, não uma omissão que poderia ser corrigida adicionando um campo mais tarde sem repensar a fronteira entre os dois volumes.

Se a fronteira precisasse mudar no futuro, a mudança exigiria revisar a decisão de escopo registrada em ROADMAP.md, não apenas adicionar um atributo a um destes tipos.