---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 12-Exemplos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — ativação recusada por contrato incompatível

Uma `DeclaracaoDePlugin` visando versão maior 2 do contrato tenta ativar contra um host que só
oferece versão maior 1 — `ativar_plugin` recusa antes de qualquer hook ser chamado.

## Caso 2 — hook que lança exceção não derruba o host

Um hook de plugin que lança `ValueError` propositalmente, ao ser chamado via
`executar_hook_isolado`, retorna um `ResultadoDeHook` com `sucesso=False` e o erro capturado, sem
propagar exceção alguma ao código que o chamou.

## Caso 3 — capacidade não declarada é negada

Um plugin que declarou apenas a capacidade `"leitura"` tenta acessar `"rede"` — `acessar_capacidade`
recusa, mesmo que o plugin em si nunca tenha sido inspecionado linha a linha antes da ativação.

## Caso 4 — desativação libera recurso sem resíduo

Um plugin ativado com recursos alocados é desativado; após a operação, nem o plugin nem seus
recursos permanecem em `EstadoDoHost`, confirmando ausência de efeito residual.

## Caso 5 — evolução de contrato que quebra hook exige versão maior

Uma mudança que altera a assinatura esperada de um hook existente, proposta como versão menor do
contrato, é recusada por `evoluir_contrato` — a mesma mudança, proposta como versão maior nova, é
aceita.

Os cinco casos juntos cobrem o ciclo completo de um plugin real: tentativa de ativação
incompatível, execução de hook que falha sem afetar o host, tentativa de acesso indevido a
capacidade, desativação limpa, e evolução do próprio contrato que o host oferece — a mesma
sequência de decisões que quem mantém um ecossistema de plugin real enfrenta ao longo do tempo,
não apenas na ativação inicial de um plugin específico.