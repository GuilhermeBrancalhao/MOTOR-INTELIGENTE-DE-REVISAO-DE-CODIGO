# Auditoria — Volume 37 CODE-GENERATION

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 37
ok: volume 37 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/37-code-generation -q
8 passed
```

## Método

Verificadas as seis regras (Y1-Y6) contra `geracao_de_codigo.py`: Y1 via
`ResultadoDeValidacaoAusente` e `ValidacaoFalhou`; Y2 via `CodigoNaoMarcado` e
`EdicaoManualDeCodigoGerado`; Y3 via teste de igualdade de valor entre duas chamadas de `gerar`
com gerador sintético determinístico; Y4 via `RevisaoHumanaAusente`; Y5/Y6 via
`EspecificacaoIncompleta`. Verificada a fronteira com `35-DOCUMENTATION` (W5, mesma disciplina de
conteúdo gerado aplicada a código) e `30-AI-GOVERNANCE` (G3, revisão humana obrigatória) em todas
as seções que as mencionam.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8 | Recusa "a IA normalmente acerta" como justificativa antes da prescrição. |
| 02-Objetivos | 8 | Cinco objetivos como disciplina que trata código gerado igual a código manual. |
| 03-Escopo | 8 | Três fronteiras nomeadas (28, 35, 30/19), evitando duplicar disciplina já estabelecida. |
| 04-Arquitetura | 8 | Sequência fixa de quatro verificações sem atalho. |
| 05-Diagramas | 8 | C4Context e sequenceDiagram; ausência de seta direta gerador→produção. |
| 06-Fluxogramas | 8.5 | stateDiagram-v2 sem transição direta que pule revisão humana; nota sobre não tentar reparo automático. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 08-Modelos | 8 | Separação intenção/resultado preserva rastreabilidade entre tentativas. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo repositório de especificações de referência. |
| 10-Anti-Patterns | 8.5 | Cinco padrões, incluindo o mais atual (capacidade do modelo como falsa justificativa para relaxar disciplina). |
| 11-Implementacao | 8 | Injeção de gerador como Callable justificada por testabilidade e neutralidade a provedor. |
| 12-Exemplos | 8 | Cinco casos isolando exatamente uma causa de rejeição cada. |
| 13-Testes | 8 | Prova por mutação nomeada; suíte livre de dependência de compilador ou IA real. |
| 14-Metricas | 8 | Quatro métricas com sinal de maturação do processo ao longo do tempo. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (comparação entre gerações, métrica de qualidade de especificação, integração com 30). |
| 17-Conclusao | 8.5 | Fecha recusando capacidade do gerador como resposta à pergunta central, sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: []` justificado. |

media: 8.1

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 37-CODE-GENERATION/ exemplos/37-code-generation/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 8 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
