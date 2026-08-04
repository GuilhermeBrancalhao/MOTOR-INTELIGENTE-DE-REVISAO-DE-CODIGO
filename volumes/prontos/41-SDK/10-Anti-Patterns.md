---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 10-Anti-Patterns
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Lançar mudança que quebra compatibilidade como versão de correção, "porque é uma correção de
bug".** Viola AC1 — mesmo uma correção de comportamento incorreto quebra quem dependia
(mesmo sem querer) do comportamento antigo, e isso exige versão maior, não de correção.

**Marcar classe ou função como pública só porque esqueceram de marcar como privada.** Viola AC2 —
a superfície pública cresce por acidente, não por decisão, tornando cada vez mais difícil manter
compatibilidade no futuro.

**Erro do SDK que expõe a exceção interna bruta, sem tradução nem orientação.** Viola AC3 — força
quem integra a adivinhar o que fazer a partir de um traceback que só faz sentido para quem
conhece a implementação interna do SDK.

**Remover elemento público diretamente na próxima versão, sem ciclo de depreciação anterior.**
Viola AC5 — quebra código de terceiros sem qualquer aviso prévio que desse tempo de reação.

**Exemplo de documentação escrito uma vez e nunca mais executado contra versão atual do SDK.**
Viola AC6 — o exemplo pode divergir silenciosamente do comportamento real conforme o SDK evolui,
enganando quem confia nele como referência.

**Manter um único changelog misturando mudança interna irrelevante com mudança de superfície
pública que de fato afeta o desenvolvedor externo.** Viola o espírito de AC1 e AC5 — dificulta
que quem integra encontre rapidamente o que realmente precisa revisar antes de atualizar a
versão do SDK que usa.