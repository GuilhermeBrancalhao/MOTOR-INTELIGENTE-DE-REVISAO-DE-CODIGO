---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — gate bloqueia taxa baixa mesmo com cobertura de linha alta

Uma medição com `cobertura_de_linha=0.95` mas `taxa_prova_de_mutacao()` de apenas 0.60, abaixo do
limiar de 0.8, é bloqueada pelo gate — a cobertura de linha alta não compensa a ausência de prova
real.

## Caso 2 — exceção registrada permite release apesar do limiar

A mesma medição do Caso 1, mas com exceção explicitamente registrada para este release
específico, passa pelo gate — a decisão de liberar mesmo assim fica rastreável.

## Caso 3 — item de dívida técnica incompleto é rejeitado

Uma tentativa de registrar dívida técnica sem custo estimado preenchido falha antes de o item
existir no registro.

## Caso 4 — regressão detectada entre duas medições

Uma medição com taxa de prova menor que a medição anterior produz um objeto `Regressao` com os
dois valores específicos — pronta para investigação, não apenas um alerta genérico.

## Caso 5 — uma única medição nunca produz regressão

Com apenas uma medição no histórico, `detectar_regressao` retorna `None` — não há ponto de
comparação suficiente para julgar tendência.


Os cinco casos cobrem, juntos, as seis regras completas — o Caso 1 sozinho já prova H1 de forma
direta, mostrando que uma cobertura de linha quase perfeita não impede o bloqueio quando a prova
de mutação real está baixa, o contraste mais didático que este volume pode oferecer.

Os casos restantes cobrem o espaço complementar: exceção registrada, dívida incompleta, e as duas variações de detecção de regressão.

Juntos, os cinco casos formam a cobertura mínima necessária para confiar no comportamento correto de todas as seis regras deste volume.