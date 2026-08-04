---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — código gerado completo, aceito sem ressalva

Um `CodigoGerado` marcado como gerado, com validação bem-sucedida e revisão humana registrada, é
aceito por `aceitar_codigo_gerado` sem ressalva.

## Caso 2 — código não marcado como gerado é rejeitado

Um código produzido por geração, mas sem `marcado_como_gerado=True`, é rejeitado antes de
qualquer outra verificação — a marcação é pré-requisito para todo o resto.

## Caso 3 — validação que falhou impede aceitação

Um código com `ResultadoDeValidacao(compilou=True, testes_passaram=False)` é rejeitado, mesmo
tendo compilado — a falha de teste sozinha já é suficiente para bloquear.

## Caso 4 — código validado mas sem revisão humana é rejeitado

O mesmo código, agora com validação completa, mas sem `revisado_por_humano=True`, ainda é
rejeitado — validação automatizada nunca substitui o portão de revisão humana.

## Caso 5 — geração é determinística para a mesma especificação

Duas chamadas a `gerar` com a mesma especificação e o mesmo gerador produzem `CodigoGerado`
iguais por comparação de valor.


Os cinco casos cobrem, juntos, as quatro verificações de `aceitar_codigo_gerado` em sequência
mais o determinismo da geração em si — a mesma cobertura completa que os testes da seção
seguinte confirmam individualmente, caso a caso, sem sobreposição desnecessária entre exemplos.

Essa cobertura completa, sem lacuna entre os casos, é o padrão que este acervo já aplica consistentemente a praticamente todo volume promovido até aqui.

Cada caso foi escolhido deliberadamente para isolar exatamente uma causa de rejeição, evitando
exemplos compostos que tornariam mais difícil identificar qual regra específica está sendo
demonstrada em cada situação apresentada nesta seção do documento.