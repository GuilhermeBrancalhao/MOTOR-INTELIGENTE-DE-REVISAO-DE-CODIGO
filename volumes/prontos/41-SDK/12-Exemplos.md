---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 12-Exemplos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — release compatível aceita sem bump de major

Uma mudança que não quebra compatibilidade, lançada como versão menor nova, é aceita por
`validar_release` sem ressalva.

## Caso 2 — release que quebra sem bump de major é rejeitado

A mesma verificação, mas com `quebra_compatibilidade=True` e versão maior inalterada, é
rejeitada — a mudança precisaria de uma versão maior nova para ser válida.

## Caso 3 — membro público sem justificativa é rejeitado

Uma tentativa de criar `MembroDeSDK` com `publico=True` mas sem `motivo_publico` falha antes de o
membro existir como parte válida da superfície.

## Caso 4 — remoção de membro público sem depreciação prévia é rejeitada

Uma tentativa de remover um membro público que nunca foi marcado como depreciado é rejeitada,
mesmo que a versão proposta incremente o número maior.

## Caso 5 — remoção correta após ciclo completo de depreciação

O mesmo membro, agora marcado como depreciado com motivo, é removido com sucesso numa versão que
de fato incrementa o número maior — o ciclo completo (depreciar, depois remover em major nova) é
respeitado.

## Caso 6 — exemplo de documentação aceito só após verificação

Um `ExemploDeUso` com `resultado_verificado=False` é rejeitado por `aceitar_exemplo`; o mesmo
exemplo, após ser de fato executado contra o código real do SDK e confirmado correto, com
`resultado_verificado=True`, é aceito sem ressalva — a diferença entre os dois casos é
exatamente o que separa documentação confiável de documentação que apenas parece confiável.

Os seis casos juntos cobrem o ciclo de vida completo de um membro público: criação com
justificativa, tentativa de remoção prematura, depreciação correta, e finalmente remoção
legítima após o aviso — a mesma sequência que um mantenedor real de SDK segue ao aposentar parte
da superfície pública ao longo de versões sucessivas.