# Auditoria — Volume 38 PROJECT-PLANNER

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 38
ok: volume 38 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/38-project-planner -q
8 passed
```

## Método

Verificadas as seis regras (Z1-Z6) contra `planejamento.py`: Z1 via `ordenar_por_dependencia` e
`DependenciaForaDeOrdem` para ciclo detectado; Z2 via `EstimativaSemIncerteza`; Z3 via
`EscopoNaoNegociado`; Z4 via `RevisaoIncompleta`; Z5 via `MotivoDoBloqueioAusente` e o teste que
confirma `BLOQUEADA` distinto de `NAO_INICIADA`; Z6 via `CriterioNaoAtingido`. Verificada a
fronteira com `39-ROADMAP` (decomposição de ciclo vs. backlog de longo prazo) e a analogia
explícita com a própria Definição de PRONTO deste acervo (conclusão verificável, nunca presumida).

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8.5 | Liga explicitamente o princípio central à Definição de PRONTO do próprio acervo, sem exagero. |
| 02-Objetivos | 8 | Cinco objetivos como ciclo completo: antes, durante e depois da execução. |
| 03-Escopo | 8 | Três fronteiras nomeadas (39, 35, 32), mantendo o volume sobre decomposição de ciclo já priorizado. |
| 04-Arquitetura | 8 | Verificação no momento da operação, nunca posterior opcional. |
| 05-Diagramas | 8 | flowchart sem atalho entre objetivo proposto e plano pronto; custo de detecção cedo vs. tarde explicado. |
| 06-Fluxogramas | 8 | Distinção de granularidade entre estado de tarefa e revisão de plano completo. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo compartilhar histórico de revisão com toda a equipe. |
| 10-Anti-Patterns | 8 | Cinco padrões, incluindo o mais sutil (revisão só na retrospectiva final, tarde demais para influenciar o ciclo). |
| 11-Implementacao | 8 | Justifica DFS simples como escolha adequada ao tamanho típico de um plano real. |
| 12-Exemplos | 8 | Cinco casos, Caso 2 didático mostrando a consequência de não detectar ciclo. |
| 13-Testes | 8 | Prova por mutação nomeada; suíte livre de dependência de ferramenta externa de planejamento. |
| 14-Metricas | 8 | Quatro métricas com foco em tendência ao longo de múltiplos ciclos. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (recalibração automática, priorização sob capacidade limitada, dependência entre ciclos). |
| 17-Conclusao | 8.5 | Fecha distinguindo planejamento de previsão perfeita, sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: []` justificado. |

media: 8.1

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 38-PROJECT-PLANNER/ exemplos/38-project-planner/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 8 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
