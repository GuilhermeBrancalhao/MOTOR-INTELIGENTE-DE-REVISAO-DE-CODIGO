# Auditoria — Volume 35 DOCUMENTATION

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 35
ok: volume 35 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/35-documentation -q
8 passed
```

## Método

Verificadas as seis regras (W1-W6) contra `documentacao.py`: W1 via `ADRIncompleto`; W2 via
`ADRImutavel` e o teste que confirma `substituir` preserva o ADR anterior com `status="SUPERADO"`
sem apagar seus campos; W3 via `DocumentoNaoVersionado`; W4 via `DocumentoDesatualizado` e
`verificar_vigencia`; W5 via `FonteDeVerdadeAusente` e `EdicaoManualDeConteudoGerado`; W6 via
`PublicoAlvoInvalido`. Verificada a matriz de controles (exigência de tipo GOVERNANCA) em
`05-Diagramas.md`, seguindo o mesmo padrão de `17-SECURITY` e `30-AI-GOVERNANCE`.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8.5 | Reconhece que o próprio acervo é exemplo prático do princípio defendido, sem exagero. |
| 02-Objetivos | 8 | Cinco objetivos ligados a cinco formas específicas de perda de conhecimento. |
| 03-Escopo | 8 | Três fronteiras nomeadas (39, 30, 36/40), isolando o volume da tentação de virar "documentação geral". |
| 04-Arquitetura | 8 | Validação na construção do objeto, não posterior, consistente com padrão do acervo. |
| 05-Diagramas | 8.5 | flowchart com matriz de controles completa, espelhando estrutura de 17 e 30. |
| 06-Fluxogramas | 8 | Reconhece dependência implícita de W3 sem forçar verificação estrutural além do escopo mínimo. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 08-Modelos | 8 | Ausência de campo opcional parcialmente preenchível reforça garantia em todos os três tipos. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo registrar alternativas descartadas no ADR. |
| 10-Anti-Patterns | 8 | Cinco padrões, incluindo o mais sutil (ADR reconstruído de memória após pergunta, não no momento da decisão). |
| 11-Implementacao | 8 | Liga imutabilidade a padrão recorrente já visto em 19, 24 e 30. |
| 12-Exemplos | 8 | Cinco casos, Casos 2-3 formando par didático para W2 nos dois sentidos. |
| 13-Testes | 8.5 | Prova por mutação nomeada; suíte livre de dependência de controle de versão real. |
| 14-Metricas | 8 | Quatro métricas com sinais diretos de processo funcionando vs. intenção não seguida. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (verificação automática em CI, índice pesquisável, revisão periódica formal). |
| 17-Conclusao | 8.5 | Fecha com analogia direta ao histórico de commits, sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: []` justificado. |

media: 8.1

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 35-DOCUMENTATION/ exemplos/35-documentation/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 8 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
