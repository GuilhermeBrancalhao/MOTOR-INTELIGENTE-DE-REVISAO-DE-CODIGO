# Auditoria — Volume 27 LLM-ROUTER

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 27
ok: volume 27 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/27-llm-router -q
7 passed
```

## Método

Verificadas as seis regras (L1-L6) contra `roteador.py`: L1 via `CandidatoNaoAprovado` e o teste
que tenta rotear para candidato fora do conjunto aprovado; L2 via degradação sustentada
acionando fallback; L3 via `historico` acrescentado a cada chamada de `rotear`; L4 via
`JanelaDeSaude.esta_degradado` retornando `False` para amostra abaixo de `minimo_de_chamadas`,
mesmo com falha isolada de 100%; L5 via o teste de janela de estabilidade que confirma dois
sinais saudáveis consecutivos abaixo do limiar mantêm fallback e o terceiro recupera; L6 via
`estado_de`. Verificada a fronteira com `26-AI-MODELS` (seleção de candidato vs. roteamento em
tempo de execução) e `34-COST-OPTIMIZATION` (saúde vs. custo) em todas as seções que as
mencionam.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8 | Reconhece a mesma tensão gate/perecibilidade já estabelecida em 26, sem repetir de forma redundante. |
| 02-Objetivos | 8 | Assimetria "cair rápido, subir devagar" explicitada como defesa central, não acidente. |
| 03-Escopo | 8 | Três fronteiras nomeadas (26, 34, 16), cada uma ligada a uma forma comum de o roteador crescer além do escopo. |
| 04-Arquitetura | 8 | Separação histórico/estado justificada por propósito distinto de cada estrutura. |
| 05-Diagramas | 8 | C4Context e sequenceDiagram; limite de escopo do diagrama explicitamente justificado. |
| 06-Fluxogramas | 8 | stateDiagram-v2; L1 explicitamente situado como anterior à máquina de estados. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada. |
| 08-Modelos | 8 | Neutralidade de fornecedor verificável nos três tipos centrais. |
| 09-Boas-Praticas | 8 | Quatro práticas, incluindo registrar o sinal bruto junto da decisão categorizada. |
| 10-Anti-Patterns | 8 | Cinco padrões, incluindo o mais fácil de deixar passar (teste só do caminho de degradação). |
| 11-Implementacao | 8 | Justifica reset total vs. decremento gradual como escolha deliberada de simplicidade. |
| 12-Exemplos | 8 | Cinco casos formando ciclo de vida completo, incluindo progressão entre casos. |
| 13-Testes | 8.5 | Prova por mutação nomeada; teste de recuperação verifica os dois lados da janela de estabilidade. |
| 14-Metricas | 8 | Quatro métricas com nota explícita sobre leitura conjunta com métricas do 26. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais (múltiplos candidatos, ajuste automático de limiar, coordenação multi-instância). |
| 17-Conclusao | 8 | Fecha nomeando a assimetria degradação/recuperação como o ponto central do volume. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: ["26"]` justificado como pré-requisito real de leitura. |

media: 8.0

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 27-LLM-ROUTER/ exemplos/27-llm-router/
(saida vazia)
```

## Verificação da regra de volume perecível

Nenhuma seção contém preço, nome de provedor ou parâmetro numérico específico como fato duradouro.
Os valores de exemplo em `roteador.py` (limiares, janela de estabilidade) são parâmetros
configuráveis do próprio tipo, não constantes fixas — consistente com `26-AI-MODELS`.

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8,0, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 7 testes passando, auditoria na média mínima,
registro no `CHANGELOG.md`.
