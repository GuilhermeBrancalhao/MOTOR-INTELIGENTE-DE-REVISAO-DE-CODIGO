# Auditoria — Volume 29 PROMPT-OPTIMIZER

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 29
ok: volume 29 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/29-prompt-optimizer -q
6 passed
```

## Método

Verificadas as seis regras (O1-O6) contra `otimizador.py`: O1 via captura de amostra em todas as
chamadas de `avaliar_variante` numa mesma busca; O2 via os dois testes de melhoria marginal e
significativa; O3 via inspeção de `dir(Otimizador)` confirmando ausência de método relacionado a
promoção; O4 via teste que confirma candidato além de `max_tentativas` nunca é avaliado; O5 via
histórico contendo tentativa rejeitada; O6 verificado estruturalmente — nenhuma linha de
`otimizador.py` reatribui `self.casos_de_ouro`. Verificada a fronteira com `07-PROMPT-ENGINE`
(função objetivo e único lugar de promoção) e `28-PROMPT-COMPILER` (compilação nunca acontece
neste volume) — fecha o grupo 1 do `ROADMAP.md`.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8.5 | Nomeia as duas tentações centrais (mover o critério, pular a revisão) antes da prescrição. |
| 02-Objetivos | 8 | Cinco objetivos agrupados pelas duas tentações que existem para conter. |
| 03-Escopo | 8 | Duas fronteiras nomeadas (07, 28), reforçando a distinção de "o que cada um faz com um prompt" do grupo 1. |
| 04-Arquitetura | 8 | Gerador de candidatos como parâmetro externo, desacoplado da lógica de avaliação. |
| 05-Diagramas | 8 | C4Context e sequenceDiagram; ausência de seta direta otimizador→promoção destacada visualmente. |
| 06-Fluxogramas | 8.5 | flowchart e stateDiagram-v2 (ENGINE completo); relação O2/O5 explicada com cuidado. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 08-Modelos | 8 | Ausência do vocabulário "promovido" nos tipos centrais, tratada como escolha deliberada. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo calibrar limiar contra tamanho de amostra. |
| 10-Anti-Patterns | 8.5 | Cinco padrões, incluindo o mais sutil (reduzir limiar depois de ver o resultado, sem tocar em O6 diretamente). |
| 11-Implementacao | 8 | Justifica ausência de teste dedicado para O3/O6 como garantia estrutural, citando paralelo com R10 do 07. |
| 12-Exemplos | 8 | Cinco casos cobrindo o espectro completo de resultado de busca. |
| 13-Testes | 8.5 | Prova por mutação nomeada; teste de orçamento verifica identidade dos candidatos, não só contagem. |
| 14-Metricas | 8 | Quatro métricas com aviso contra otimização isolada de qualquer uma. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (estratégia de geração, paralelização, parada antecipada). |
| 17-Conclusao | 8 | Fecha distinguindo ampliação honesta de atalho disfarçado, sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: ["07"]` justificado como pré-requisito real. |

media: 8.1

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 29-PROMPT-OPTIMIZER/ exemplos/29-prompt-optimizer/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 6 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`. Com este volume, o grupo 1 do ROADMAP.md (07, 28, 29) está completo.
