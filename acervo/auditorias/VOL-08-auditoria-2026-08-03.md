# Auditoria — Volume 08 AGENT-ENGINE

**Data:** 2026-08-03
**Revisao:** 2 (revisao 1 no mesmo dia, antes de o volume ter exemplos)
**Auditor:** Opus 5 (redator: Sonnet 5)
**Gates na entrada (estado da revisao 1; ver Revisao 2 ao final):**

```
$ python -m ferramentas.validar 08
ok: volume 08 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ pytest exemplos/08-agent-engine
(nao existe — o volume nao cita codigo executavel)
```

## Ressalva de independencia

Auditor (Opus 5) e um modelo distinto do redator (Sonnet 5), mas na **mesma sessao**, com o
contexto da redacao disponivel — independencia mais fraca que auditoria de contexto limpo. A
contramedida foi verificar por execucao o que e verificavel e marcar explicitamente o que e
apenas especificacao nao verificavel.

## Método

Este volume nao tem componente executavel, entao nao ha numero a reproduzir. O que foi conferido:
a coerencia interna dos tres diagramas contra o contrato descrito em `07-Regras` e `08-Modelos`;
a fronteira declarada contra `09-ORCHESTRATOR` conferida nos dois sentidos (o `03-Escopo` de cada
um nomeia o outro e nao se contradizem); e a existencia da secao "Prova por mutacao" em
`13-Testes`, que `31-TESTING` afirma existir neste volume — confere.

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 8.5 | Define agente como o loop em volta do modelo, nao o modelo — a definicao certa para um volume de motor. A fronteira com `09` ("uma execucao" contra "varias coordenadas") aparece ja aqui, com o teste pratico de qual pergunta cai em qual volume. |
| 02-Objetivos | 8 | Cinco objetivos verificaveis. O quarto (diferenciar encerramento por objetivo de encerramento por orcamento) e o que sustenta a decisao de desenho mais importante do volume. |
| 03-Escopo | 8.5 | Cinco fronteiras, cada uma nomeando o volume responsavel. A distincao sobre RAG e precisa: se uma ferramenta usa recuperacao, isso e implementacao da ferramenta, nao deste motor. |
| 04-Arquitetura | 8 | O `C4Context` posiciona o motor entre chamador e tres dependencias externas, e o texto acerta o ponto central — nenhuma das tres decide quando o ciclo termina. Os quatro componentes internos tem responsabilidade disjunta. |
| 05-Diagramas | 8 | O `sequenceDiagram` mostra a ordem que importa (decisao do modelo, depois guardiao) e o mindmap dos tres motivos de encerramento distingue o que cada um significa para quem chama. Perde por ter precisado de expansao para bater o minimo de prosa. |
| 06-Fluxogramas | 8.5 | O `stateDiagram-v2` cobre as transicoes e a prosa resolve o empate entre `EncerradoPorObjetivo` e `EncerradoPorOrcamento` de forma deterministica. O caminho de erro distingue recuperavel de nao recuperavel com a razao economica (nao gastar passos em erro que sempre falha igual). |
| 07-Regras | 8.5 | Cinco invariantes com o custo de violar cada uma. A terceira dimensao do orcamento e justificada por contraexemplo concreto (ferramenta lenta estoura tempo sem estourar passos). A matriz de controles tem tres linhas, cada uma com o teste que a provaria. |
| 08-Modelos | 8 | Quatro estruturas coerentes entre si. O detalhe de `saida: None` quando o motivo nao e `OBJETIVO_ATINGIDO` e desenho, nao decoracao: a ausencia do valor e o sinal estrutural. |
| 09-Boas-Praticas | 8 | Seis praticas, cada uma com a razao. "Medir consumo por tipo de motivo de encerramento separadamente" e a que o codigo sozinho nao garante — e o buraco certo a cobrir em prosa. |
| 10-Anti-Patterns | 8.5 | Cinco padroes com custo concreto. "Deixar o modelo decidir quando parar sem limite estrutural independente" nomeia o erro exato: apostar que o modelo nunca entra em loop sem progresso. |
| 11-Implementacao | 7.5 | **Secao mais fraca, e honesta sobre isso**: declara que nao cita codigo por decisao do ciclo e explica por que inventar exemplo seria pior. A ordem de construcao recomendada (guardiao primeiro) e util. Mas uma secao chamada "Implementacao" sem implementacao e, por natureza, a que menos entrega. |
| 12-Exemplos | 8 | Tres casos que percorrem os tres motivos de encerramento, com o numero de passos coerente entre eles (3 no caso feliz, 4 com retry — a diferenca e a evidencia do erro recuperado). Dominio inventado e neutro (consulta de estoque). |
| 13-Testes | 8 | Propoe a tecnica certa (modelo fake com sequencia programada) e o teste discriminante certo: contar chamadas ao modelo quando o orcamento ja chega zerado — esperado zero. E o unico teste do volume que distingue as duas ordens possiveis de verificacao. |
| 14-Metricas | 8 | Quatro metricas com fonte e leitura. A decomposicao de latencia entre decisao do modelo e execucao de ferramenta aponta para volumes diferentes conforme o resultado — a metrica orienta acao, nao so descreve. |
| 15-Checklist | 8 | **Corrigido nesta auditoria** (ver Problema 1). Oito itens, todos verificaveis contra uma implementacao, desmarcados para quem verificar marcar com evidencia. |
| 16-Roadmap | 8 | Tres lacunas declaradas, incluindo a ausencia de codigo (que bloqueia o criterio 2) e o paralelismo dentro de uma execucao, deliberadamente fora do contrato com a razao dita. |
| 17-Conclusao | 8 | Resume as duas ideias que sustentam o volume (motivo de encerramento explicito; fronteira com `09`) e declara o proprio estado sem inflar. |
| 18-Referencias-Cruzadas | 8 | Cinco vizinhos com o sentido do consumo em cada linha; `depende_de: []` justificado. Links resolvem (gate 1). |

media: 8.2

## Problemas encontrados

1. **(médio — corrigido) 15-Checklist vinha com sete itens marcados `[x]`.** Um deles afirmava
   "Existe teste que prova, por contagem de chamadas ao modelo fake, que orcamento zerado impede
   a proxima chamada" — **esse teste nao existe**, porque o volume nao tem codigo. Marcar `[x]`
   afirma feito; a convencao dos volumes PRONTO (`03`, `12`) e deixar desmarcado para quem
   verifica marcar com evidencia. Defeito sistemico nos sete volumes deste ciclo, corrigido nos
   sete.
2. **(menor — corrigido) tres ocorrencias de "excepcao"** (grafia pt-PT) contra "excecao" usada
   no resto do acervo. Uniformizado.
3. **(observacao) 11-Implementacao nao entrega o que o nome promete.** E consequencia da decisao
   de escopo do ciclo, esta declarada, e e a mesma lacuna que bloqueia o criterio 2 — nao um
   defeito de redacao.

## Verificacao do dominio neutro

```
$ grep -rin "concilia\|controladoria\|extrato\|lancamento\|contabil\|omie\|sicoob\|boleto" 08-AGENT-ENGINE/
(saida vazia)
```

**Limpo.** O dominio dos exemplos (consulta de estoque de um produto) e inventado e neutro.

## Revisao 2 — exemplos executaveis acrescentados

Depois da revisao 1, o volume ganhou `exemplos/08-agent-engine/` com
`orcamento.py + laco_agente.py` e a suite correspondente. Gates reconferidos nesta revisao:

```
$ python -m ferramentas.validar 08
ok: volume 08 sem violacoes

$ python -m pytest exemplos/08-agent-engine -q
14 passed
```

As secoes tocadas pela mudanca (`11-Implementacao`, `15-Checklist`, `16-Roadmap`,
`17-Conclusao`) foram reconferidas: nenhuma delas ainda afirma que o volume nao cita codigo —
essa varredura foi feita por grep sobre as sete pastas, e a saida ficou vazia. A frase de
fechamento de `17-Conclusao` agora declara os quatro criterios satisfeitos, o que confere com a
saida acima e com o registro no `CHANGELOG.md`.

Delta da media: 8.1 -> 8.2. 11-Implementacao 7,5->8,5: deixa de ser uma secao sem implementacao e passa a ser o manual de dois modulos reais. As demais secoes nao mudaram e mantem a nota da
revisao 1.

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Media 8.2, nenhuma secao abaixo de 6. Os quatro
criterios da Definicao de PRONTO estao satisfeitos: gate estrutural verde (criterio 1), os 14
testes de `exemplos/` passando (criterio 2 — que na revisao 1 era exatamente o que faltava),
esta auditoria com media acima de 8,0 (criterio 3) e o registro datado no `CHANGELOG.md`
(criterio 4).

**Ressalva que acompanha a promocao:** o auditor e um modelo distinto do redator, mas opera na
mesma sessao. A promocao apoia-se nisso mais no que e mecanicamente verificavel — gate, testes,
e a conferencia de cada afirmacao factual contra o codigo — do que no julgamento de prosa.
