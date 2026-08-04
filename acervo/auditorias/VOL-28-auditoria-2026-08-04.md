# Auditoria — Volume 28 PROMPT-COMPILER

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 28
ok: volume 28 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/28-prompt-compiler -q
7 passed
```

## Método

Verificadas as seis regras (Q1-Q6) contra `compilador.py`: Q1 via `PromptNaoPromovido` para
prompt fora de PROMOVIDO; Q2 via teste de igualdade de valor entre duas compilações idênticas; Q3
via `OrcamentoExcedido` após renderização; Q4 via dois dialetos distintos produzindo formatações
diferentes sem alterar `compilar`; Q5 via `PosicaoDeCacheInvalida` para posição fora de
`"inicio_estavel"`; Q6 via `VariavelAusente` antes da renderização. Verificada a fronteira com
`07-PROMPT-ENGINE` (contrato do prompt vs. compilação do payload) — a mesma decisão de
sobreposição de domínio do grupo 1 do `ROADMAP.md`.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8 | Risco concreto (falha silenciosa só visível na resposta do provedor) antes da prescrição. |
| 02-Objetivos | 8 | Cinco objetivos agrupados em duas categorias (integridade vs. custo/previsibilidade). |
| 03-Escopo | 8 | Três fronteiras nomeadas (07, 29, 26/27), mantendo o volume estritamente sobre tradução. |
| 04-Arquitetura | 8 | Sequência fixa de quatro verificações sem caminho que as pule. |
| 05-Diagramas | 8 | C4Context e sequenceDiagram; adaptador de dialeto modelado como sistema externo injetado. |
| 06-Fluxogramas | 8.5 | flowchart e stateDiagram-v2 (ENGINE completo); relação entre os dois níveis explicada. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 08-Modelos | 8 | Tipos passivos vs. lógica centralizada em `compilar`, justificado. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo versionamento conjunto de adaptador e formato. |
| 10-Anti-Patterns | 8 | Cinco padrões, incluindo o mais perigoso (ignorar orçamento excedido "para ver o que acontece"). |
| 11-Implementacao | 8 | Ausência de estado compartilhado ligada tanto a Q2 quanto a paralelismo seguro. |
| 12-Exemplos | 8 | Cinco casos cobrindo as quatro rejeições mais o caminho de sucesso com dois dialetos. |
| 13-Testes | 8.5 | Prova por mutação nomeada; nota sobre suíte rápida sem dependência externa. |
| 14-Metricas | 8 | Quatro métricas distinguindo problema de contrato de problema de estimativa. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (compressão automática, tokenizador real, cache multi-nível). |
| 17-Conclusao | 8 | Nomeia Q6 como a regra mais fácil de negligenciar, sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: ["07"]` justificado como pré-requisito real. |

media: 8.1

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 28-PROMPT-COMPILER/ exemplos/28-prompt-compiler/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 7 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
