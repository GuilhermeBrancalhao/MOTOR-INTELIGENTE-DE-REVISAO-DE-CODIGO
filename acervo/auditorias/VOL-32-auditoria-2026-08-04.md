# Auditoria — Volume 32 QUALITY

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 32
ok: volume 32 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/32-quality -q
9 passed
```

## Método

Verificadas as seis regras (H1-H6) contra `indicador_de_qualidade.py`: H1 via
`Medicao.taxa_prova_de_mutacao` e o teste que confirma cobertura de linha alta não evita bloqueio
com taxa de prova baixa; H2 via `LimiarNaoAtingido` e o caminho de exceção registrada; H3 via
`ItemDeDividaIncompleto`; H4 via `detectar_regressao` retornando `None` com uma medição só; H5 via
o objeto `Regressao` explícito com os dois valores; H6 via inspeção dos campos de `Medicao`.
Verificada a fronteira com `31-TESTING` (prática vs. indicador agregado) em todas as seções que a
mencionam.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8 | Reaproveita a tese central do 31 (execução ≠ verificação) e a estende ao indicador agregado. |
| 02-Objetivos | 8 | Cinco objetivos em sequência de dependência. |
| 03-Escopo | 8 | Três fronteiras nomeadas (31, 33, 18), mantendo o volume sobre o indicador, não a prática. |
| 04-Arquitetura | 8 | Separação estrutural entre métrica primária e dado complementar, verificável no próprio tipo. |
| 05-Diagramas | 8 | flowchart com gate e histórico como mecanismos distintos claramente separados. |
| 06-Fluxogramas | 8 | Distinção entre exceção de gate (H2) e regressão (H5) explicada com cuidado. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo data de revisão sugerida para dívida técnica. |
| 10-Anti-Patterns | 8 | Cinco padrões, incluindo o mais sutil (taxa aprovada uma vez, nunca remedida). |
| 11-Implementacao | 8 | Justifica separação entre GateDeQualidade e HistoricoDeQualidade como independência real. |
| 12-Exemplos | 8 | Cinco casos cobrindo as seis regras completas. |
| 13-Testes | 8.5 | Prova por mutação nomeada; nota sobre suíte rápida sem depender de mutação real. |
| 14-Metricas | 8 | Quatro métricas com aviso contra leitura fora de contexto operacional. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (cálculo de custo de dívida, alerta de exceção repetida, decomposição por tipo de regra). |
| 17-Conclusao | 8 | Fecha nomeando H5 como a regra mais fácil de virar formalidade vazia, sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: []` justificado. |

media: 8.1

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 32-QUALITY/ exemplos/32-quality/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 9 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
