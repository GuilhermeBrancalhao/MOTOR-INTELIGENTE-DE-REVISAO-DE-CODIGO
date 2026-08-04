# Auditoria — Volume 15 CONTEXT

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 15
ok: volume 15 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/15-context -q
7 passed
```

## Método

Verificadas as seis regras (C1-C6) contra `orcamento.py`. Verificada a independência declarada
de `13-RAG` (C5) — `depende_de: []` confere, e nenhuma seção do volume pressupõe a existência de
um pipeline de RAG para fazer sentido. Este é o quarto e último volume do grupo 2 do
`ROADMAP.md`; a fronteira com os outros três (`11`, `13`, `14`) foi conferida sem contradição.

## Notas por seção (resumo)

18 seções, prosa específica (orçamento de janela, não genérica). Ponto forte: a garantia de C6
(instrução de sistema nunca descartada silenciosamente) é verificável tanto no código
(`OrcamentoExcedidoPelaInstrucao` como exceção distinta, não descarte parcial) quanto na ausência
estrutural de qualquer seta de descarte de instrução nos diagramas — a garantia aparece em três
formas independentes (regra, código, diagrama) sem contradição entre elas.

media: 8.0

## Verificação do domínio neutro

```
$ grep -rin "concilia|controladoria|omie|sicoob" 15-CONTEXT/ exemplos/15-context/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8,0, nenhuma seção abaixo de 6. Com este volume,
o grupo 2 (conhecimento e contexto: 11, 13, 14, 15) está completo.
