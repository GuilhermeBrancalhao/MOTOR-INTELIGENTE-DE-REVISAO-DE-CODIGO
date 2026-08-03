# Auditoria — Volume 09 ORCHESTRATOR

**Data:** 2026-08-03
**Revisao:** 2 (revisao 1 no mesmo dia, antes de o volume ter exemplos)
**Auditor:** Opus 5 (redator: Sonnet 5)
**Gates na entrada (estado da revisao 1; ver Revisao 2 ao final):**

```
$ python -m ferramentas.validar 09
ok: volume 09 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ pytest exemplos/09-orchestrator
(nao existe — o volume nao cita codigo executavel)
```

## Ressalva de independencia

Auditor (Opus 5) distinto do redator (Sonnet 5), mesma sessao — independencia parcial. Ver a
mesma ressalva no relatorio do volume 01.

## Método

Conferida a coerencia da fronteira tripla `08`/`09`/`10`: o `03-Escopo` de cada um dos tres
nomeia os outros dois e nenhum se contradiz sobre onde a linha passa. Conferida a afirmacao de
`11-Implementacao` de que o algoritmo de deteccao de ciclo e o mesmo usado por
`ferramentas.validar --cross-refs` neste acervo — confere: `validar_cross_refs` implementa
travessia com marcacao de tres estados sobre `depende_de`, exatamente a tecnica descrita.
Conferida a existencia de "Prova por mutacao" em `13-Testes`, afirmada por `31-TESTING`.

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 8.5 | Nomeia as duas classes de bug que o DAG existe para evitar (execucao fora de ordem; trabalho duplicado ou perdido em falha parcial) antes de descrever a solucao. A fronteira com `10` e a mais dificil das tres e e tratada com cuidado ja na abertura. |
| 02-Objetivos | 8 | Seis objetivos. O quinto (retry de no contra retry de grafo) e a distincao que o leitor tipicamente nao faz sozinho, e a condicao em que a segunda faz sentido — estado nao idempotente — esta dita. |
| 03-Escopo | 8.5 | Quatro fronteiras nomeadas. A fronteira deliberada final e honesta: este motor **nao** otimiza ordem por custo, so respeita dependencia — e isso esta registrado como extensao possivel, nao escondido. |
| 04-Arquitetura | 8 | O `C4Context` trata os tres tipos de no (agente, funcao, sub-workflow) de forma identica, que e a decisao de desenho central. Os quatro componentes internos tem responsabilidade disjunta. |
| 05-Diagramas | 8 | O `sequenceDiagram` separa validacao (uma vez) de execucao (iterativa) e o `flowchart` de fan-out/fan-in e claro. O detalhe de `C` herdar falha por dependencia nao resolvida, e nao por falha propria, e preciso. |
| 06-Fluxogramas | 8.5 | O `stateDiagram-v2` por no cobre `FalhaTentando` como estado transitorio com garantia de resolucao — nao fica parado. O caminho de falha parcial explica por que o resultado e granular por no, nao agregado. |
| 07-Regras | 8.5 | **Corrigido nesta auditoria** (ver Problema 1). Cinco invariantes, com destaque para "retry de no nunca reexecuta dependencias ja resolvidas", cuja razao (nao idempotencia produziria resultado inconsistente entre tentativas) esta dita. Matriz com tres controles testaveis. |
| 08-Modelos | 8 | Quatro estruturas. `ResultadoGrafo` sem campo agregado de sucesso e desenho deliberado e coerente com `07-Regras`. O backoff exponencial esta explicado com a serie concreta (2s, 4s, 8s). |
| 09-Boas-Praticas | 8 | Cinco praticas. "Declarar dependencia explicita mesmo quando a ordem provavelmente sai correta por acaso" ataca o erro mais provavel — confiar em ordem observada empiricamente, que o volume ja declarou nao garantir. |
| 10-Anti-Patterns | 8.5 | Cinco padroes com custo. "Usar `AbortarDependentes` como padrao universal para simplificar" nomeia o custo exato: desperdicar o paralelismo que a estrutura de DAG existe para preservar. |
| 11-Implementacao | 7.5 | **Mesma limitacao estrutural do volume 08**: sem codigo. Mas e a melhor das sete secoes 11 deste ciclo, porque a analogia com `validar --cross-refs` deste proprio acervo foi verificada e e verdadeira — o leitor tem onde olhar um exemplo real do algoritmo. |
| 12-Exemplos | 8 | Tres casos coerentes entre si (o Caso 2 reusa o grafo do Caso 1 mudando so a falha, o que isola a variavel). O Caso 3 tem a serie de backoff correta contra `08-Modelos`. |
| 13-Testes | 8 | Nomeia as cinco formas de grafo a testar (linear, fan-out, fan-in, diamante, ciclico) e o teste discriminante certo: E contra OU no fan-in, que so um grafo com dependencia falha revela. |
| 14-Metricas | 8 | Quatro metricas com fonte. "Tempo em `Pendente` contra tempo em `Executando`" e a que orienta a acao certa — otimizar o no gargalado nao reduz o tempo total se ele estava so esperando. |
| 15-Checklist | 8 | **Corrigido nesta auditoria** (ver Problema 2). Oito itens verificaveis, desmarcados. |
| 16-Roadmap | 8 | Tres lacunas, incluindo cancelamento externo de no em execucao — que o contrato atual assume nao existir, dito explicitamente em vez de omitido. |
| 17-Conclusao | 8 | Fecha com a distincao que mais importa (abortar contra pular dependentes) e declara o proprio estado. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, incluindo a ligacao com `01-FUNDACAO/11` pelo algoritmo compartilhado — referencia util e verificada. |

media: 8.2

## Problemas encontrados

1. **(médio — corrigido) `07-Regras` continha uma palavra corrompida.** A frase lia "os tres
   precisam ter **sucesfrom**, nao apenas a maioria" — corrupcao de "sucesso", numa das cinco
   invariantes do volume. Passou pelo gate estrutural porque nenhuma regra do validador checa
   ortografia, e passou pela redacao porque a frase continua legivel. Corrigido.
2. **(médio — corrigido) 15-Checklist vinha com sete itens marcados `[x]`**, dois dos quais
   afirmavam testes que nao existem ("Existe teste que prova, por grafo ciclico construido de
   proposito..."). Defeito sistemico dos sete volumes deste ciclo. Corrigido nos sete.
3. **(menor — corrigido) uma ocorrencia de "excepcao"** (pt-PT) uniformizada para "excecao".
4. **(observacao) a analogia com `validar --cross-refs` e o melhor recurso do volume e esta
   subaproveitada.** Aparece so em `11-Implementacao`; `13-Testes` poderia apontar para os testes
   reais de ciclo daquele modulo como referencia concreta de como testar deteccao de ciclo.

## Verificacao do dominio neutro

```
$ grep -rin "concilia\|controladoria\|extrato\|lancamento\|contabil\|omie\|sicoob\|boleto" 09-ORCHESTRATOR/
(saida vazia)
```

**Limpo.** O dominio dos exemplos (tres buscas paralelas com agregacao) e inventado e neutro.

## Revisao 2 — exemplos executaveis acrescentados

Depois da revisao 1, o volume ganhou `exemplos/09-orchestrator/` com
`grafo.py` e a suite correspondente. Gates reconferidos nesta revisao:

```
$ python -m ferramentas.validar 09
ok: volume 09 sem violacoes

$ python -m pytest exemplos/09-orchestrator -q
10 passed
```

As secoes tocadas pela mudanca (`11-Implementacao`, `15-Checklist`, `16-Roadmap`,
`17-Conclusao`) foram reconferidas: nenhuma delas ainda afirma que o volume nao cita codigo —
essa varredura foi feita por grep sobre as sete pastas, e a saida ficou vazia. A frase de
fechamento de `17-Conclusao` agora declara os quatro criterios satisfeitos, o que confere com a
saida acima e com o registro no `CHANGELOG.md`.

Delta da media: 8.1 -> 8.2. 11-Implementacao 7,5->8,5: a analogia com validar --cross-refs agora vem acompanhada do algoritmo implementado e testado. As demais secoes nao mudaram e mantem a nota da
revisao 1.

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Media 8.2, nenhuma secao abaixo de 6. Os quatro
criterios da Definicao de PRONTO estao satisfeitos: gate estrutural verde (criterio 1), os 10
testes de `exemplos/` passando (criterio 2 — que na revisao 1 era exatamente o que faltava),
esta auditoria com media acima de 8,0 (criterio 3) e o registro datado no `CHANGELOG.md`
(criterio 4).

**Ressalva que acompanha a promocao:** o auditor e um modelo distinto do redator, mas opera na
mesma sessao. A promocao apoia-se nisso mais no que e mecanicamente verificavel — gate, testes,
e a conferencia de cada afirmacao factual contra o codigo — do que no julgamento de prosa.
