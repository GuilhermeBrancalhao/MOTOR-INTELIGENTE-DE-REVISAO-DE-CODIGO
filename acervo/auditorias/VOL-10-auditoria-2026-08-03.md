# Auditoria — Volume 10 WORKFLOW

**Data:** 2026-08-03
**Revisao:** 1
**Auditor:** Opus 5 (redator: Sonnet 5)
**Gates na entrada:**

```
$ python -m ferramentas.validar 10
ok: volume 10 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ pytest exemplos/10-workflow
(nao existe — o volume nao cita codigo executavel)
```

## Ressalva de independencia

Auditor (Opus 5) distinto do redator (Sonnet 5), mesma sessao — independencia parcial. Ver a
mesma ressalva no relatorio do volume 01.

## Método

Conferida a fronteira tripla `08`/`09`/`10` nos tres sentidos — sem contradicao. Conferida a
coerencia entre `06-Fluxogramas` (dois estados de espera) e `14-Metricas` (que mede os dois
separadamente) e `10-Anti-Patterns` (que trata colapsa-los como defeito): os tres concordam.
Conferida a existencia de "Prova por mutacao" em `13-Testes`, afirmada por `31-TESTING`.

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 9 | A melhor introducao dos sete volumes deste ciclo. Define passo deterministico e passo de IA pelo criterio operacional certo (dado o mesmo insumo, a saida se repete ou nao), e enfrenta de frente a confusao terminologica workflow/orquestracao que custa decisao de arquitetura errada. |
| 02-Objetivos | 8 | Cinco objetivos. O ultimo — decidir quando modelar como workflow em vez de agente autonomo — da ao leitor o criterio (quanto da sequencia e conhecida de antemao), nao so a definicao. |
| 03-Escopo | 8.5 | Cinco fronteiras nomeadas. A fronteira deliberada final e precisa: mesmo passo condicional e declarado com a condicao explicita; decisao nao declarada a priori e `09`. |
| 04-Arquitetura | 8.5 | O `C4Context` separa os dois tipos de passo e o sinal externo. O ponto critico do desenho — gravar, confirmar, so entao avancar — aparece ja aqui, nao so em `07-Regras`. |
| 05-Diagramas | 8 | O `sequenceDiagram` mostra que a validacao so ocorre no ramo de IA, e o `flowchart` de correcao automatica converge os dois caminhos em `Pausado`. Precisou de expansao para bater o minimo de prosa — duas vezes. |
| 06-Fluxogramas | 8.5 | A distincao entre `AguardandoSinal` (esperado pelo processo) e `Pausado` (precisa de atencao) e a contribuicao mais util do volume, e a razao operacional esta dita: os dois "param" a execucao mas pedem reacao oposta. |
| 07-Regras | 8.5 | Cinco invariantes com custo. A regra do checkpoint confirmado antes de avancar e defendida pelo contrafactual correto (estado ambiguo se o passo nao for idempotente). Matriz com tres controles, cada um com o teste que o provaria. |
| 08-Modelos | 8 | Quatro estruturas. `EsperaSinal.identificador` resolve o problema real de casar sinal com workflow quando varios esperam ao mesmo tempo. O campo `timestamp` do checkpoint tem uso declarado, nao decorativo. |
| 09-Boas-Praticas | 8 | Cinco praticas. "Preferir passo deterministico sempre que a tarefa nao exigir interpretacao de texto livre" e a que economiza mais na pratica e a que um volume sobre IA teria a tentacao de nao escrever. |
| 10-Anti-Patterns | 8.5 | Cinco padroes. "Modelar decisao de agente autonomo como condicional com todas as ramificacoes enumeradas" nomeia o custo exato — uma arvore que tenta prever o imprevisivel — e devolve o caso ao volume certo. |
| 11-Implementacao | 7.5 | Mesma limitacao estrutural dos volumes 08 e 09: sem codigo. Salva-se pela tecnica concreta de gravacao atomica (escrever o novo antes de invalidar o anterior), que e acionavel mesmo sem exemplo. |
| 12-Exemplos | 8.5 | Tres casos que reusam o mesmo workflow variando uma condicao — bom isolamento de variavel. O Caso 3 e o mais valioso: explica por que a reexecucao conservadora e correta mesmo quando desnecessaria, ligando ao contrafactual de `07-Regras`. |
| 13-Testes | 8 | Propoe testar o ponto exato entre conclusao e confirmacao de checkpoint, que e onde a garantia vive. A prova por mutacao proposta (trocar a ordem das duas operacoes) e discriminante. |
| 14-Metricas | 8 | Quatro metricas com fonte. A decomposicao do tempo total entre espera de sinal (processo de negocio) e execucao de passo (motor) separa dois problemas que pedem intervencoes diferentes. |
| 15-Checklist | 8 | **Corrigido nesta auditoria** (ver Problema 1). Oito itens verificaveis, desmarcados. |
| 16-Roadmap | 8 | Tres lacunas, incluindo compensacao/rollback (padrao saga) declarada fora do contrato minimo com a consequencia dita: quem precisar implementa fora do motor hoje. |
| 17-Conclusao | 8 | Fecha com a distincao `AguardandoSinal`/`Pausado` e com a fronteira contra `09`. Declara o proprio estado sem inflar. |
| 18-Referencias-Cruzadas | 8.5 | Tres vizinhos com a relacao explicada; a linha sobre `09` nomeia a fronteira como "central deste volume", o que e verdade e ajuda a navegacao. |

media: 8.2

## Problemas encontrados

1. **(médio — corrigido) 15-Checklist vinha com sete itens marcados `[x]`**, dois afirmando
   testes inexistentes ("Existe teste que injeta falha entre conclusao de passo e confirmacao de
   checkpoint..."). Defeito sistemico dos sete volumes deste ciclo. Corrigido nos sete.
2. **(menor — corrigido) uma ocorrencia de "excepcao"** (pt-PT) uniformizada para "excecao".
3. **(observacao) 05-Diagramas precisou de duas expansoes para atingir o minimo de prosa.** O
   conteudo acrescentado e legitimo (limite de tentativas; convergencia dos dois caminhos em
   `Pausado`), mas a secao foi a que mais raspou o piso — sinal de que os dois diagramas dizem
   quase tudo sozinhos e a prosa tem pouco a acrescentar, nao de que falte conteudo.

## Verificacao do dominio neutro

```
$ grep -rin "concilia\|controladoria\|extrato\|lancamento\|contabil\|omie\|sicoob\|boleto" 10-WORKFLOW/
(saida vazia)
```

**Limpo.** O dominio dos exemplos (processamento de documento com aprovacao humana) e inventado
e neutro.

## Veredicto

**Criterio 3 satisfeito. Volume NAO promovido.** Media 8.2, nenhuma secao abaixo de 6. O
**criterio 2 nao e satisfeito** — nao existe `exemplos/10-workflow/`. `status` permanece
`RASCUNHO`. E o volume com a melhor prosa dos sete (a `01-Introducao` e a mais forte do ciclo) e
tambem um dos que mais perderia se o componente executavel nunca vier: a garantia de checkpoint
atomico e exatamente o tipo de coisa que so um teste com falha injetada comprova.
