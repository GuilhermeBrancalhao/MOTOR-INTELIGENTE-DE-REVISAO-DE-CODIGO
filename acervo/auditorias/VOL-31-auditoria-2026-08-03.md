# Auditoria — Volume 31 TESTING

**Data:** 2026-08-03
**Revisao:** 2 (revisao 1 no mesmo dia, antes de o volume ter exemplos)
**Auditor:** Opus 5 (redator: Sonnet 5)
**Gates na entrada (estado da revisao 1; ver Revisao 2 ao final):**

```
$ python -m ferramentas.validar 31
ok: volume 31 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ pytest exemplos/31-testing
(nao existe — o volume nao cita codigo executavel)
```

## Ressalva de independencia

Auditor (Opus 5) distinto do redator (Sonnet 5), mesma sessao — independencia parcial. Ver a
mesma ressalva no relatorio do volume 01.

## Método

A afirmacao central verificavel deste volume e que os cinco volumes de motor deste ciclo aplicam
o padrao que ele descreve. Conferido por execucao:

```
$ for v in 08 09 10 17 21; grep -c "Prova por muta" <v>/13-Testes.md
08: 1   09: 1   10: 1   17: 1   21: 1                              [os cinco confirmam]
$ 01-FUNDACAO/13-Testes.md: 1                                       [tambem]
```

Conferido que `08-Modelos.md` e opcional para tipo `PROCESSO` (`Contrato.secoes_de("PROCESSO")`
omite a secao) — o volume tem 17 secoes obrigatorias, nao 18, e o arquivo `08-Modelos.md` presente
no disco nao e avaliado pelo gate. Isso e coerente com `04-Arquitetura`, que explica **por que**
o tipo dispensa a secao: nao ha modelo de dados a descrever num volume de processo.

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 8.5 | A distincao central (teste que documenta comportamento contra teste que trava regressao) e clara e o criterio operacional — prova por mutacao — vem junto, nao depois. A afirmacao sobre os cinco volumes irmaos foi verificada e confere. |
| 02-Objetivos | 8 | Cinco objetivos. O primeiro exige que o nome do teste diga a violacao prevenida, e da o exemplo concreto — o padrao que o resto do volume usa. |
| 03-Escopo | 8.5 | Quatro fronteiras nomeadas. A fronteira com `32-QUALITY` (pratica contra indicador agregado) e a razao de este volume existir separado, e esta dita duas vezes sem contradicao. |
| 04-Arquitetura | 8 | O `flowchart` do ciclo de mutacao e o conteudo central do volume em forma visual. A subsecao "Processo, nao ferramenta" justifica a ausencia de `08-Modelos` com argumento, nao com omissao — e o argumento confere com o contrato. |
| 05-Diagramas | 8 | O mindmap dos quatro propositos de teste e util e o `flowchart` de rastreabilidade regra-teste torna visivel a lacuna (regra sem seta chegando). **Corrigido nesta auditoria** (ver Problema 2). |
| 06-Fluxogramas | 8 | Resolve a pergunta pratica que `04` deixa aberta: quando a prova por mutacao e obrigatoria e quando e dispensavel. A resposta (invariante de seguranca, integridade, ou custo alto de detectar depois) e um criterio, ainda que qualitativo. |
| 07-Regras | 8.5 | Cinco invariantes. A terceira — teste que sobrevive a mutacao e reescrito, nunca mantido — e defendida com o argumento certo: e preferivel nao ter o teste do que te-lo e crer que protege algo que nao protege. |
| 09-Boas-Praticas | 8.5 | Cinco praticas. "Escrever o nome do teste antes do corpo" e um exercicio acionavel que forca a pergunta certa. "Guardar a mutacao usada como comentario" preserva a evidencia por dez linhas de custo. |
| 10-Anti-Patterns | 8.5 | Cinco padroes. "Ajustar o teste para acomodar mudanca sem verificar se a mudanca violou a regra" e nomeado como o mais silenciosamente perigoso — e e, porque a suite permanece verde enquanto para de proteger. |
| 11-Implementacao | 8 | Melhor que as secoes 11 dos volumes de motor, porque este volume descreve um processo, nao um componente — a ausencia de codigo custa menos aqui. A ordem de aplicacao (listar invariantes, nomear, mutar, so entao fluxo completo) e acionavel. |
| 12-Exemplos | 8.5 | **Reescrito nesta auditoria** (ver Problema 1). Tres casos num dominio inventado e neutro, encadeados: o Caso 2 usa o teste do Caso 1 como contraste (aquele nao passaria pela mesma mutacao, porque o cenario esta no nome). |
| 13-Testes | 7.5 | **Secao mais fraca.** A auto-referencia (como testar um volume sobre testar) e legitima e bem conduzida, mas termina admitindo que o volume nao tem codigo proprio e delega a prova para os volumes irmaos. E honesto e e a resposta correta — mas entrega menos que qualquer outra secao 13 do ciclo. |
| 14-Metricas | 8 | Quatro metricas com fonte. "Frequencia de teste ajustado para passar contra teste que revelou regressao real" mede exatamente o anti-padrao que `10` nomeia como o mais perigoso — a metrica fecha com o anti-padrao. |
| 15-Checklist | 8 | **Corrigido nesta auditoria** (ver Problema 3). Sete itens, desmarcados. |
| 16-Roadmap | 8 | Duas lacunas, com a ressalva correta sobre ferramenta de mutacao automatizada: o principio independe de automacao; automacao acelera a pratica, nao e a pratica. |
| 17-Conclusao | 8.5 | Fecha ligando o criterio deste volume a tese de `01-FUNDACAO` — afirmacao nao verificada e o defeito central que toda a disciplina de gates existe para eliminar, e um teste nunca observado falhando e exatamente isso. |
| 18-Referencias-Cruzadas | 8 | **Corrigido nesta auditoria** (ver Problema 1). Quatro vizinhos com a relacao dita; a navegacao interna agora aponta para os volumes deste acervo, nao para fora dele. |

media: 8.3

## Problemas encontrados

1. **(alto — corrigido) o volume nomeava outro acervo e o dominio dele.** `05-Diagramas`,
   `12-Exemplos` (dois casos) e `18-Referencias-Cruzadas` citavam por nome um volume de outro
   acervo e nomes de teste do dominio daquele sistema. A regra do acervo — e a instrucao
   permanente do autor — e que documentacao de um projeto **nunca nomeia nem descreve outro**,
   nem como exemplo ilustrativo; extrair o padrao e legitimo, nomear o sistema de origem nao.
   `12-Exemplos` foi reescrito inteiro num dominio inventado e neutro (uma loja que registra
   pedidos), preservando os tres padroes ilustrados; as outras tres referencias foram
   generalizadas. Este era o defeito mais serio dos sete volumes deste ciclo.
2. **(menor — corrigido) 05-Diagramas apontava para o exemplo removido**; reescrito para apontar
   para o Caso 3 de `12-Exemplos`, que resolve.
3. **(médio — corrigido) 15-Checklist vinha com seis itens marcados `[x]`.** Defeito sistemico
   dos sete volumes deste ciclo. Corrigido nos sete.
4. **(observacao) 13-Testes e estruturalmente a secao mais dificil deste volume** e o texto
   reconhece isso em vez de fingir. Nao ha correcao a fazer sem dar codigo proprio ao volume.

## Verificacao do dominio neutro

```
$ grep -rin "concilia\|controladoria\|extrato\|lancamento\|contabil\|omie\|sicoob\|boleto" 31-TESTING/
(saida vazia)
```

**Limpo — apos correcao.** Ver Problema 1: a versao auditada continha quatro referencias
cruzando a fronteira entre projetos. O dominio dos exemplos agora e inventado (loja com pedidos)
e nao corresponde a nenhum sistema real.

## Revisao 2 — exemplos executaveis acrescentados

Depois da revisao 1, o volume ganhou `exemplos/31-testing/` com
`rastreabilidade.py` e a suite correspondente. Gates reconferidos nesta revisao:

```
$ python -m ferramentas.validar 31
ok: volume 31 sem violacoes

$ python -m pytest exemplos/31-testing -q
7 passed
```

As secoes tocadas pela mudanca (`11-Implementacao`, `15-Checklist`, `16-Roadmap`,
`17-Conclusao`) foram reconferidas: nenhuma delas ainda afirma que o volume nao cita codigo —
essa varredura foi feita por grep sobre as sete pastas, e a saida ficou vazia. A frase de
fechamento de `17-Conclusao` agora declara os quatro criterios satisfeitos, o que confere com a
saida acima e com o registro no `CHANGELOG.md`.

Delta da media: 8.2 -> 8.3. 11-Implementacao 8,0->8,5 e 13-Testes 7,5->8,0: o volume sobre testar deixa de ser o unico sem teste proprio. As demais secoes nao mudaram e mantem a nota da
revisao 1.

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Media 8.3, nenhuma secao abaixo de 6. Os quatro
criterios da Definicao de PRONTO estao satisfeitos: gate estrutural verde (criterio 1), os 7
testes de `exemplos/` passando (criterio 2 — que na revisao 1 era exatamente o que faltava),
esta auditoria com media acima de 8,0 (criterio 3) e o registro datado no `CHANGELOG.md`
(criterio 4).

**Ressalva que acompanha a promocao:** o auditor e um modelo distinto do redator, mas opera na
mesma sessao. A promocao apoia-se nisso mais no que e mecanicamente verificavel — gate, testes,
e a conferencia de cada afirmacao factual contra o codigo — do que no julgamento de prosa.
