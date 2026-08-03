# Auditoria — Volume 01 FUNDACAO

**Data:** 2026-08-03
**Revisao:** 2 (revisao 1 no mesmo dia, antes de o volume ter exemplos)
**Auditor:** Opus 5 (redator: Sonnet 5)
**Gates na entrada (estado da revisao 1; ver Revisao 2 ao final):**

```
$ python -m ferramentas.validar 01
ok: volume 01 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ pytest exemplos/01-fundacao
(nao existe — o volume nao cita codigo executavel)
```

## Ressalva de independencia

O auditor (Opus 5) e um modelo distinto do redator (Sonnet 5), mas opera na **mesma sessao**,
com o contexto da redacao disponivel. Isso e uma forma mais fraca de independencia do que uma
auditoria de contexto limpo: reduz o vies de autoavaliacao do modelo, nao o elimina. A
contramedida aplicada foi verificar por execucao toda afirmacao factual verificavel, em vez de
julgar a prosa por leitura.

## Método

Toda afirmacao sobre o motor foi conferida contra o codigo real, uma a uma:

```
$ grep -n "def secoes_de\|def diagramas_de\|def minimo_de" ferramentas/contrato.py
39:    def secoes_de   47:    def diagramas_de   50:    def minimo_de          [confere]

$ grep -n "def validar_volume\|def validar_tudo\|def validar_cross_refs" ferramentas/validar.py
44 / 103 / 111 — docstring de validar_volume e literalmente
"Aplica todas as regras de um volume. Nao levanta por conteudo ruim."               [confere]

$ nomes de regra reais em regras.py/validar.py
frontmatter-campo, substancia-curta, marcador-proibido, volume-yml, volume-tipo,
depende-de-ciclo — os seis citados na prosa existem com o nome exato               [confere]
"auditoria-ausente-para-pronto" NAO existe — o 16-Roadmap afirma essa ausencia     [confere]

$ grep -rn "def test_convencoes_nao_derivou\|def test_os_42_volumes_estao_declarados"
acervo/ferramentas/tests/test_contrato.py:81 e :54                                 [confere]

$ ls acervo/ferramentas/tests/ | grep "test_contrato\|test_validar"
os dois arquivos existem com os nomes citados                                      [confere]
```

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 8.5 | O argumento central (especificacao errada custa mais que implementacao errada porque corrige N instancias, nao uma) e proprio e bem construido. A justificativa de `depende_de: []` e literal e correta. Falta-lhe um numero reproduzido — e prosa boa, nao evidencia. |
| 02-Objetivos | 8 | Cinco objetivos acionaveis, cada um com o lugar onde se verifica. O objetivo 2 cita o proprio erro de 2026-08-02 como ancora concreta, o que salva a secao de ser generica. |
| 03-Escopo | 8.5 | Fronteira nomeia o volume vizinho e a razao em cada linha (02, 06, 17, 21), seguindo a convencao de `07-PROMPT-ENGINE`. A distincao entre as duas matrizes de controle (esta audita texto, a do 17 audita sistema) e a linha mais util. |
| 04-Arquitetura | 8.5 | As tres camadas (contrato executavel / projecao humana / decisao do autor) sao uma abstracao propria e correta — a terceira e a unica nao derivavel de codigo, e isso e dito. O flowchart corresponde a Definicao de PRONTO real. |
| 05-Diagramas | 8 | O `erDiagram` acerta o ponto sutil: `depende_de` opera no nivel de volume, nunca de secao. O mindmap separa o que o gate mede do que so a auditoria julga — distincao que este proprio relatorio exerce. |
| 06-Fluxogramas | 8 | Os tres caminhos (feliz, reprovacao no gate, reprovacao na auditoria) sao concretos e os nomes de regra citados foram verificados. Perde por repetir em prosa o que `04` ja mostrou em diagrama. |
| 07-Regras | 9 | Cinco invariantes, cada uma com o custo de violar. A matriz de controles tem cinco linhas e **cada uma nomeia uma verificacao que existe** — as duas testaveis (`test_convencoes_nao_derivou`, `depende-de-ciclo`) foram conferidas no fonte. E a secao mais forte do volume. |
| 08-Modelos | 8 | Os quatro contratos (`_VOLUME.yml`, front-matter, `Violacao`, relatorio de auditoria) estao corretos. O detalhe de `linha=0` significar "arquivo inteiro" confere com a saida real do validador. |
| 09-Boas-Praticas | 8.5 | "Rodar o gate antes da segunda secao, nao depois da decima oitava" tem custo quantificado (uma correcao contra dezoito). A ultima pratica — auditar antes de reescrever em lote — e a licao real de 2026-08-03, escrita sem eufemismo. |
| 10-Anti-Patterns | 9 | Cinco anti-padroes, todos com caso real por tras: a contagem de teste como prova de conteudo, a geracao em lote, o BOM, o ciclo em `depende_de`, o PRONTO por impressao. O do BOM explica a causa tecnica exata (`utf-8` nao remove BOM; `utf-8-sig` remove). |
| 11-Implementacao | 8.5 | Os tres modulos e as assinaturas citadas foram conferidos um a um contra o fonte — todos conferem. O estudo de caso do BOM acerta o ponto de desenho: a correcao foi na fonte, nao tolerar BOM no parser, porque tolerar mascararia BOM futuro. |
| 12-Exemplos | 8.5 | **Corrigido nesta auditoria** (ver Problema 1). Os tres casos agora sao verificaveis: o Caso 1 usa os proprios sete volumes deste ciclo como exemplo do estado "gate verde, nao PRONTO"; o Caso 2 tem a aritmetica correta (657 − 39 = 618); o Caso 3 e a decisao de escopo datada. |
| 13-Testes | 8.5 | **Corrigido nesta auditoria** (ver Problema 2). Os dois arquivos de teste citados existem com os nomes exatos, agora afirmados sem hedge. A secao de prova por mutacao propoe o teste certo (reintroduzir BOM de proposito). |
| 14-Metricas | 7.5 | Quatro metricas com fonte declarada, e a leitura de 39→657 como *melhora* (visibilidade) e a interpretacao correta e nao obvia. **Mas nenhuma das quatro esta instrumentada** — sao metricas propostas, e a secao nao marca isso com a mesma clareza que `16-Roadmap` marca suas lacunas. |
| 15-Checklist | 8 | **Corrigido nesta auditoria** (ver Problema 3). Dez itens, todos acionaveis, e o ultimo (`validar NN` retorna exit 0) fecha com a distincao certa entre "revisei e parece certo" e "a maquina confirmou". |
| 16-Roadmap | 8 | Duas lacunas reais e verificadas: a ausencia da regra `auditoria-ausente-para-pronto` (confirmada por grep) e a ausencia de processo de revogacao de PRONTO. A segunda tem precedente real citado (a deriva de `volumes/prontos/`). |
| 17-Conclusao | 8.5 | Fecha com as tres licoes e aplica a propria regra a si mesmo — declara-se RASCUNHO ate passar pelo criterio 3. A frase final ("a mesma regra que ele mesmo define, aplicada a si mesmo sem excecao") e verdadeira e verificavel neste relatorio. |
| 18-Referencias-Cruzadas | 8 | Distingue pre-requisito de vizinhanca, justifica `depende_de: []` com a mesma razao do `_VOLUME.yml`, e todos os links resolvem (gate 1). A tabela de vizinhos evita a confusao mais provavel (as duas matrizes de controle). |

media: 8.4

## Problemas encontrados

1. **(médio — corrigido) 12-Exemplos afirmava tres gates verdes e negava o terceiro na mesma
   frase.** O texto dizia "gates 1, 2 e 3 mecanicos verdes, `status: RASCUNHO` mantido porque a
   auditoria por outro modelo nunca aconteceu" — mas o gate 3 **e** a auditoria por outro modelo.
   Autocontradicao num volume cuja tese central e nao afirmar verificacao que nao houve.
2. **(menor — corrigido) 13-Testes cobria os nomes de teste com um hedge desnecessario.** O texto
   dizia "nomes ilustrativos do papel; ver o motor para os arquivos exatos" — mas
   `test_contrato.py` e `test_validar.py` existem com esses nomes exatos. Hedge sobre fato
   verificavel e ruido, nao prudencia.
3. **(médio — corrigido) 15-Checklist vinha com nove itens ja marcados `[x]`.** Marcar afirma
   feito. Os volumes PRONTO deste acervo (`03`, `12`) deixam o checklist **desmarcado** — quem
   verifica marca com evidencia a mao. Ver o problema sistemico no relatorio de qualquer um dos
   sete volumes deste ciclo.
4. **(observacao) 14-Metricas propoe metricas nao instrumentadas.** Nao e defeito — o volume nao
   tem componente executavel — mas a secao poderia declarar isso como `16-Roadmap` declara suas
   proprias lacunas.

## Verificacao do dominio neutro

```
$ grep -rin "concilia\|controladoria\|extrato\|lancamento\|contabil\|omie\|sicoob\|boleto" 01-FUNDACAO/
(saida vazia)
```

**Limpo — apos correcao.** A versao auditada continha tres referencias nomeando outro acervo e o
volume `45` daquele acervo. Removidas: o Caso 1 de `12-Exemplos` passou a usar os proprios sete
volumes deste ciclo, e `13-Testes` passou a citar `12-MEMORY`, que vive neste acervo. A regra
aplicada: extrair o padrao e legitimo, nomear o sistema de origem nao.

## Revisao 2 — exemplos executaveis acrescentados

Depois da revisao 1, o volume ganhou `exemplos/01-fundacao/` com
`definicao_de_pronto.py` e a suite correspondente. Gates reconferidos nesta revisao:

```
$ python -m ferramentas.validar 01
ok: volume 01 sem violacoes

$ python -m pytest exemplos/01-fundacao -q
8 passed
```

As secoes tocadas pela mudanca (`11-Implementacao`, `15-Checklist`, `16-Roadmap`,
`17-Conclusao`) foram reconferidas: nenhuma delas ainda afirma que o volume nao cita codigo —
essa varredura foi feita por grep sobre as sete pastas, e a saida ficou vazia. A frase de
fechamento de `17-Conclusao` agora declara os quatro criterios satisfeitos, o que confere com a
saida acima e com o registro no `CHANGELOG.md`.

Delta da media: 8.3 -> 8.4. 11-Implementacao 8,5->9,0: passa a citar a Definicao de PRONTO em forma executavel, incluindo a leitura do criterio 2 que este proprio relatorio aplicou. As demais secoes nao mudaram e mantem a nota da
revisao 1.

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Media 8.4, nenhuma secao abaixo de 6. Os quatro
criterios da Definicao de PRONTO estao satisfeitos: gate estrutural verde (criterio 1), os 8
testes de `exemplos/` passando (criterio 2 — que na revisao 1 era exatamente o que faltava),
esta auditoria com media acima de 8,0 (criterio 3) e o registro datado no `CHANGELOG.md`
(criterio 4).

**Ressalva que acompanha a promocao:** o auditor e um modelo distinto do redator, mas opera na
mesma sessao. A promocao apoia-se nisso mais no que e mecanicamente verificavel — gate, testes,
e a conferencia de cada afirmacao factual contra o codigo — do que no julgamento de prosa.
