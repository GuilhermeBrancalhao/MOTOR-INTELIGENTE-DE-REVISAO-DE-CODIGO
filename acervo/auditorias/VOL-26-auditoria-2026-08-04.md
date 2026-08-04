# Auditoria — Volume 26 AI-MODELS

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 26
ok: volume 26 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/26-ai-models -q
8 passed
```

## Método

Verificadas as seis regras (M1-M6) contra `selecao_de_modelo.py`: M1 (requisito antes de
avaliação) via `CandidatoDeModelo.aprovado` reprovando por `atende_requisito=False` mesmo com
ótima avaliação; M2 (avaliação obrigatória) via `ModeloNaoAvaliado`; M3 (fallback obrigatório)
via `validar_plano` e `FallbackAusente`; M4 (custo por tarefa completa) via
`comparar_custo_por_tarefa` e o cenário onde preço unitário maior produz custo total menor; M5
(nenhum número fixo) verificado por inspeção — nenhuma constante de preço ou nome de modelo
existe no módulo, todo valor é parâmetro; M6 (troca sempre registrada) via `registrar_troca`.
Verificada a regra 9 de `00-INTRODUCAO/Convencoes.md` (volume perecível): nenhum preço, limite ou
nome de modelo aparece como fato duradouro em nenhuma das 18 seções.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8 | Reconhece explicitamente a tensão entre gate estrutural (piso fixo) e regra de perecibilidade (conteúdo fino), sem contradição. |
| 02-Objetivos | 8 | Cinco objetivos como cadeia de confiança crescente. |
| 03-Escopo | 8 | Três fronteiras nomeadas (27, 07, 34), incluindo justificativa de ritmo de mudança diferente entre seleção e roteamento. |
| 04-Arquitetura | 8 | Ausência de valor fixo verificável nos próprios tipos, não apenas afirmada. |
| 05-Diagramas | 8 | C4Context, sequenceDiagram e stateDiagram-v2 (na seção 06); nota sobre estabilidade do diagrama frente a mudança de implementação do 27. |
| 06-Fluxogramas | 8 | stateDiagram-v2 do ciclo de vida de um candidato; nenhuma transição de Ativo pula o registro de substituição. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 08-Modelos | 8 | Obrigatoriedade de campo como mecanismo do interpretador, não apenas convenção. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo documentar motivo de reprovação, não só o número. |
| 10-Anti-Patterns | 8 | Cinco padrões, incluindo o mais direto (tabela de preço fixada em documentação de longa duração). |
| 11-Implementacao | 8 | Confirma ausência de constante de módulo por inspeção, incluindo nos próprios testes. |
| 12-Exemplos | 8 | Cinco casos formando jornada completa da decisão, incluindo os dois pontos de falha explícita. |
| 13-Testes | 8.5 | Prova por mutação nomeada; asserção intermediária tratada como parte da prova, não só depuração. |
| 14-Metricas | 8 | Quatro métricas com aviso sobre comparação através do tempo sem contexto de data. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (deriva automática, fallback por similaridade, composição de múltiplos modelos). |
| 17-Conclusao | 8 | Fecha com a distinção entre o que muda (números) e o que não muda (método), sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: []` justificado. |

media: 8.0

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 26-AI-MODELS/ exemplos/26-ai-models/
(saida vazia)
```

## Verificação da regra de volume perecível

Nenhuma seção contém preço, janela de contexto ou nome de modelo específico como fato duradouro.
Todo valor numérico no exemplo (`preco_por_1k_entrada`, `contexto_minimo_tokens`, etc.) é
parâmetro fornecido em tempo de uso, nunca constante hardcoded — verificado por inspeção de
`selecao_de_modelo.py` e ausência de `grep` para padrão de preço fixo no volume.

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8,0, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 8 testes passando, auditoria na média mínima, registro
no `CHANGELOG.md`.
