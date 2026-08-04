---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`compilar` é a função central: recebe um `PromptPromovido`, as variáveis a substituir, um
`Dialeto` (que carrega a função de formatação específica do provedor), orçamento de tokens, e
pontos de cache opcionais. A ordem de verificação dentro da função nunca muda: estado promovido
primeiro, depois variáveis completas, depois posição de cache válida, depois renderização, por
último orçamento contra o resultado já renderizado — cada verificação só faz sentido depois que a
anterior passou.

`Dialeto.formatar_mensagens` é uma função injetada, não uma condicional dentro de `compilar` — o
núcleo do compilador nunca sabe qual provedor está por trás de um dialeto específico, apenas
delega a formatação para a função fornecida. Trocar de provedor significa trocar o `Dialeto`
passado, nunca alterar o código de `compilar`.

`PayloadCompilado` é imutável e carrega `hash_origem` — o hash do prompt que o gerou — junto do
resultado, tornando possível auditar depois exatamente qual versão de prompt produziu um payload
específico, mesmo que o prompt original já tenha sido substituído por uma versão mais nova.


Nenhuma dessas quatro verificações (estado, variáveis, cache, orçamento) é opcional ou pulável —
`compilar` é uma função única que as aplica em sequência fixa, o que significa que não existe
caminho de código que produza `PayloadCompilado` sem ter passado por todas as quatro.