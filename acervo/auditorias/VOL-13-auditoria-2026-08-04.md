# Auditoria — Volume 13 RAG

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 13
ok: volume 13 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/13-rag -q
6 passed
```

## Método

Verificadas as seis regras (R1-R6) contra `pipeline.py`. Verificado que `depende_de: ["11",
"14"]` é coerente — este volume de fato consome tipos e conceitos dos dois (validade de
documento de `11`, `ResultadoBusca`/proximidade de `14`), sem redefinir nenhum dos dois. Os dois
pontos de recusa (sem fonte, fidelidade insuficiente) foram verificados como estados distintos e
alcançáveis por transições diferentes no `stateDiagram-v2`, coerente com a prosa que os
distingue.

## Notas por seção (resumo)

18 seções, prosa específica ao pipeline de RAG. Ponto forte: a distinção entre `score_proximidade`
e `score_relevancia` (R3) é consistente em `07-Regras`, `08-Modelos`, `12-Exemplos` e no exemplo
executável, com um caso concreto (Caso 4) mostrando a inversão de ranking na prática.

media: 8.0

## Verificação do domínio neutro

```
$ grep -rin "concilia|controladoria|omie|sicoob" 13-RAG/ exemplos/13-rag/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8,0, nenhuma seção abaixo de 6.
