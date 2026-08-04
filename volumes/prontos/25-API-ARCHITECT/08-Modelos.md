---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`ContratoDeEndpoint.campos_expostos` mapeia nome de campo para tipo, servindo como o registro
único contra o qual toda nova declaração é verificada — não existe um segundo lugar no sistema
que também "sabe" quais campos um endpoint expõe, o que eliminaria a possibilidade de os dois
divergirem silenciosamente.

`ErroDeAPI` carrega `codigo`, `mensagem` e `detalhes` — três campos suficientes para cobrir tanto
erro de máquina (o `codigo`, estável e comparável programaticamente) quanto erro para humano (a
`mensagem`), sem depender de análise de texto livre para decisão automatizada baseada em erro.

`RecursoDeStatusDeTrabalho` carrega `url_consulta` como campo explícito do próprio recurso — o
cliente nunca precisa construir essa URL por convenção implícita, ela vem pronta na resposta
inicial que criou o trabalho.


Nenhum dos tipos deste exemplo (`ContratoDeEndpoint`, `ErroDeAPI`, `RecursoDeStatusDeTrabalho`,
`OrcamentoDeLatencia`) importa ou referencia diretamente um tipo do modelo interno de persistência
do `24-DATABASE-ARCHITECT` — essa ausência de acoplamento no próprio código é a garantia estrutural
de que a camada de contrato nunca depende do formato interno além do que passa explicitamente por
`traduzir_para_resposta`.

Essa ausência de acoplamento é verificável por inspeção do próprio arquivo de código — nenhuma
linha de `contrato_api.py` importa de `repositorio.py` (o módulo correspondente do
24-DATABASE-ARCHITECT), e essa separação física entre os dois arquivos é, na prática, o que torna
a garantia estrutural concreta, não apenas uma intenção documentada em prosa.