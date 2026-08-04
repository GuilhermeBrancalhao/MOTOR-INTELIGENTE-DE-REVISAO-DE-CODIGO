# Auditoria — Volume 30 AI-GOVERNANCE

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 30
ok: volume 30 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/30-ai-governance -q
8 passed
```

## Método

Verificadas as seis regras (G1-G6) contra `governanca_ia.py`: G1 via `DonoResponsavelAusente`;
G2 via `CasoDeUsoNaoClassificado` para caso não registrado; G3 via `RevisaoHumanaAusente` para
decisão ALTO/CRITICO sem revisão, e o teste que confirma decisão BAIXO não exige o mesmo; G4 via
inspeção da trilha de auditoria preservando `modelo_usado` e `entrada` completos; G5 via
`AprovacaoAusente`; G6 via teste que confirma duas revisões periódicas coexistem sem substituição.
Verificada a fronteira com `17-SECURITY` (defesa técnica vs. governança de decisão) em todas as
seções que a mencionam, incluindo a matriz de controles adicional (exigida para tipo GOVERNANCA)
em `05-Diagramas.md`.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8.5 | Recusa "a IA decidiu" como resposta antes da prescrição; liga explicitamente ao 17 como as duas metades de segurança completa. |
| 02-Objetivos | 8 | Cinco objetivos como cadeia de accountability, cada um habilitando o seguinte. |
| 03-Escopo | 8 | Três fronteiras nomeadas (17, 18, 26), mantendo o volume estritamente sobre governança organizacional. |
| 04-Arquitetura | 8 | Camada de governança explicitamente desacoplada do mecanismo técnico do 17. |
| 05-Diagramas | 8.5 | flowchart com dois portões distintos (caso de uso vs. decisão individual) mais matriz de controles completa (exigência de tipo GOVERNANCA). |
| 06-Fluxogramas | 8 | Cadência de revisão periódica distinguida da cadência de evento único. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 08-Modelos | 8 | Três coleções separadas por ciclo de vida distinto, justificado. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo formato de consulta acessível para investigação de incidente. |
| 10-Anti-Patterns | 8.5 | Cinco padrões, incluindo o mais sutil (revisão marcada como feita sem ter acontecido de fato). |
| 11-Implementacao | 8 | Reconhece imutabilidade de histórico como padrão recorrente do acervo (19, 24), não escolha isolada. |
| 12-Exemplos | 8 | Cinco casos cobrindo os dois portões mais o ciclo de revisão periódica. |
| 13-Testes | 8.5 | Prova por mutação nomeada; nota sobre dado sintético mantendo suíte livre de preocupação de privacidade. |
| 14-Metricas | 8 | Quatro métricas distinguindo controle real de formalidade vazia. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (apelação, métricas de viés específicas, integração com auditoria externa). |
| 17-Conclusao | 8.5 | Fecha ligando explicitamente a 17-SECURITY como as duas metades de segurança completa, sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: []` justificado. |

media: 8.2

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 30-AI-GOVERNANCE/ exemplos/30-ai-governance/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.2, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 8 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
