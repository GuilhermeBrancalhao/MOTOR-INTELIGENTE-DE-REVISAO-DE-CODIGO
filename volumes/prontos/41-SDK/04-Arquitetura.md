---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 04-Arquitetura
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Arquitetura

`validar_release` recusa uma combinação de mudança que quebra compatibilidade
(`quebra_compatibilidade=True`) com uma nova versão que não incrementa o número maior — a
verificação compara a versão anterior contra a proposta antes de qualquer release ser
considerado válido.

`MembroDeSDK.__post_init__` recusa um membro marcado como `publico=True` sem
`motivo_publico` declarado, e recusa um membro marcado como `depreciado=True` sem
`motivo_de_depreciacao` — as duas verificações acontecem juntas, na própria criação do membro,
antes de ele existir como parte válida da superfície do SDK.

`SuperficieDoSDK.remover_membro` recusa remover um membro público que nunca passou por
depreciação prévia, e recusa remoção de membro público mesmo depreciado se a nova versão não
incrementa o número maior — a remoção de algo público sempre exige as duas coisas juntas:
depreciação anterior e versão maior nova.

`ErroDoSDK.__post_init__` recusa criação sem `como_corrigir` preenchido — todo erro que o SDK
levanta carrega orientação de correção desde o momento em que é formado, nunca adicionada depois
como reflexão tardia.

`aceitar_exemplo` recusa um `ExemploDeUso` cujo campo `resultado_verificado` permanece `False` —
a estrutura garante que nenhum exemplo alcance a documentação publicada do SDK sem antes ter sido
executado e confirmado contra o comportamento real do código, fechando o ciclo entre o que é
prometido ao desenvolvedor externo e o que o SDK de fato faz quando chamado.