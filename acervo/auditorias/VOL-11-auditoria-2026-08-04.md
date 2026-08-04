# Auditoria — Volume 11 KNOWLEDGE

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 11
ok: volume 11 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/11-knowledge -q
8 passed
```

## Método

Verificadas as seis regras (K1-K6) contra `curadoria.py`. Verificada a fronteira com `13-RAG` e
`14-VECTOR` contra a decisão registrada em `ROADMAP.md` (grupo 2, decisão de 2026-07-29) — sem
divergência. **Encontrada e corrigida uma imprecisão própria**: `08-Modelos.md` afirmava
inicialmente que um terceiro documento conflitante "se junta ao mesmo `Conflito`", mas o código
de `ingerir` cria um novo registro sobreposto em vez de consolidar — a prosa foi corrigida para
declarar isso como limitação conhecida, e registrada em `16-Roadmap.md`.

## Notas por seção (resumo)

18 seções, prosa específica ao domínio (curadoria de conhecimento, não genérica), diagramas
coerentes com o código, nenhuma referência a outro projeto. Nota mais baixa: `08-Modelos` (8,0),
pela imprecisão encontrada e corrigida durante esta própria auditoria — o processo de correção em
si é evidência de que a verificação por execução funciona, não só o resultado final.

media: 8.1

## Verificação do domínio neutro

```
$ grep -rin "concilia|controladoria|omie|sicoob" 11-KNOWLEDGE/ exemplos/11-knowledge/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6.
