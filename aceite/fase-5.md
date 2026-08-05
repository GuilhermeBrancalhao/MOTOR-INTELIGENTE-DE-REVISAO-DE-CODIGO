# Aceite do P2C5 — COBAIA: um projeto de terceiro, do zero à entrega, pela CLI

**Data:** 2026-08-05
**Ciclo:** P2C5, o último do Programa 2.

Este documento é o registro do aceite. Ele não escreve produto — decide, com saída real
colada, se o ENGINE conduz um projeto **de terceiro** do zero à entrega com o veredito
decidido por execução, e não por digitação. É a resposta à pergunta que originou os dois
programas: *"o ENGINE constrói um sistema completo?"*

A fase 4 fechou dizendo, com todas as letras, o que ela **não** provava:

> **O que este aceite NAO prova.** Que o ENGINE constroi um sistema complexo real de ponta
> a ponta. […] A prova de capacidade e o passo 6 da spec — um programa real, com ciclos
> reais, num projeto-cobaia. Ate la, a resposta continua sendo "por construcao, nao por
> execucao".

É esse passo. As saídas abaixo foram rodadas nesta data, contra o código que está neste
repositório agora, num diretório-cobaia limpo, e coladas sem edição de conteúdo (só a
formatação em bloco).

Rodadas com `PYTHONUTF8=1`, pelo mesmo motivo da fase 4: a acentuação sai legível no
console do Windows. O comportamento é idêntico sem a variável.

> **Nota sobre `exit=`.** Os códigos de saída colados foram medidos sem canalizar a saída
> por outro comando. A armadilha cobrou de novo nesta sessão: a primeira execução do
> roteiro foi feita com `sh roteiro.sh | tee log | head -120`, e o `head` fechou o cano
> no passo 7 — o `tee` morreu de `EPIPE` e **o roteiro inteiro foi interrompido no meio**,
> com o log terminando sem erro nenhum aparente. O roteiro foi refeito sem cano.

---

## Suíte do motor

Antes deste ciclo:

```
python -m pytest -q
817 passed in 140.79s (0:02:20)
```

Depois (817 + os 8 testes do defeito que a cobaia revelou, ver a seção "O achado"):

```
python -m pytest -q
825 passed in 140.71s (0:02:20)
```

E a suíte da própria cobaia, no fim do programa:

```
python -m pytest -q
.....................................................                    [100%]
53 passed in 0.09s
exit=0
```

---

## A cobaia

Uma calculadora de folha de pagamento mensal CLT, em Python: INSS por faixas
progressivas, IRRF sobre a base de cálculo com dedução por dependente, e o holerite
consolidado. Código real (`Decimal` em todo o dinheiro, tabelas de 2024 declaradas no
módulo, entrada inválida recusada), testes reais em `pytest`, e **os valores esperados de
cada teste calculados à mão contra a tabela, com a conta escrita no comentário** — teste
cujo esperado sai de rodar a função não prova nada, confirma o código contra ele mesmo.

Montada fora deste repositório, num diretório temporário, e **removida ao fim**: nada da
cobaia ficou em disco. O que sobrou dela é este documento e os 8 testes novos do motor.

O plano-mestre, submetido por `programa plano plano-mestre.json`:

| Ciclo | Objetivo | Depende de | `comando_de_aceite` |
|---|---|---|---|
| C1 | INSS por faixas progressivas, com teto | — | `python -m pytest tests/test_inss.py -q` |
| C2 | IRRF sobre a base (bruto − INSS − dependentes) | C1 | `python -m pytest tests/test_irrf.py -q` |
| C3 | holerite consolidado com líquido | C1, C2 | `python -m pytest tests/test_holerite.py -q` |

**O defeito do C2 é um defeito de verdade**, do tipo que a planilha do DP comete: a faixa
do IRRF foi escolhida pelo **salário bruto** em vez de pela **base de cálculo**
(`_faixa(valor)` no lugar de `_faixa(base)`). Ele não erra sempre — erra só quando bruto e
base caem em faixas diferentes, que é a vizinhança da virada. Em 3.000,00 sem dependentes
dá 29,74 onde o devido é 36,15; em 5.000,00 com dois dependentes dá 232,05 onde o devido é
260,18. Os dois casos estão nos testes, ao lado de três casos de controle que passam nas
duas versões — e é a existência dos controles que mostra que a suíte não é um carimbo.

---

## O roteiro, reproduzível

Tudo pela CLI, com `ENGINE_RAIZ` apontando para a pasta da cobaia:

```
# 1-7  abrir e planejar
engine programa "<objetivo do sistema>"
engine descoberta --programa "<o pedido, com as palavras do usuário>"        # recusa: falta a intenção
engine descoberta --programa "<o mesmo pedido>" --intencao MATERIALIZAR
engine descoberta --programa recusar LOJA_PAGAMENTOS
engine descoberta --programa responder <ID> "<resposta>"                     # x6, as bloqueantes
engine programa plano plano-mestre.json
engine programa proximo                                                      # a porta P1 barra
engine programa aprovar

# 8-11 por ciclo
engine programa proximo
engine ligar "<objetivo do ciclo>"
engine descoberta "<o pedido do ciclo>" --intencao MATERIALIZAR
engine descoberta responder <ID> "<resposta>"                                # x6
engine fase ANALISE ; engine fase PLANO ; engine fase BUILD
#   … o código e os testes do ciclo são escritos aqui …
engine fase TESTE
engine programa verificar <CICLO>
engine fase REVISAO ; engine fase DOC ; engine fase ENTREGA ; engine desligar

# 13-17 recuperação e fecho
engine programa reabrir C2 ; engine fase BUILD                               # … o conserto …
engine fase TESTE ; engine programa verificar C2
engine programa sistema ok
```

`engine` é `py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py"`.

---

## Item 1 — veredito APROVADO por comando real (código de saída 0)

```
$ engine programa verificar C1
**Verificando C1** — inss_do_salario devolve o desconto progressivo somando faixa a faixa (nao aliquota unica), respeita o teto, e recusa salario negativo.
**Comando de aceite:** python -m pytest tests/test_inss.py -q
**Código de saída:** 0  ·  **Veredito:** APROVADO  ·  **Duração:** 1.045s
**Motivo:** código de saída 0
--- saída do comando (redigida, teto de 8000 caracteres) ---
.........                                                                [100%]
9 passed in 0.03s

--- fim da saída ---

**C1 CONCLUIDO** pelo código de saída do comando de aceite.
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** EXECUCAO
**Objetivo:** calculadora de folha de pagamento mensal CLT: INSS, IRRF e holerite consolidado
**Ciclos:** 1/3 concluídos
  [x] C1: desconto de INSS por faixas progressivas, com teto de contribuicao
  [ ] C2: desconto de IRRF sobre a base (bruto - INSS - dependentes), pela tabela progressiva com parcela a deduzir  (depende de C1)
  [ ] C3: holerite consolidado com proventos, descontos e salario liquido  (depende de C1, C2)
**Próximo ciclo elegível:** C2
exit=0
```

Ninguém digitou `ok`. O único argumento do verbo é o id do ciclo.

---

## Item 2 — veredito REPROVADO por comando real (código de saída ≠ 0)

```
$ engine programa verificar C2
**Verificando C2** — irrf_do_salario escolhe a faixa pela BASE de calculo (bruto menos INSS menos deducao por dependente), nunca pelo salario bruto, e aplica a parcela a deduzir da faixa escolhida.
**Comando de aceite:** python -m pytest tests/test_irrf.py -q
**Código de saída:** 1  ·  **Veredito:** REPROVADO  ·  **Duração:** 1.207s
**Motivo:** código de saída 1
--- saída do comando (redigida, teto de 8000 caracteres) ---
..FF.....                                                                [100%]
================================== FAILURES ===================================
____________________ test_faixa_vem_da_base_e_nao_do_bruto ____________________

    def test_faixa_vem_da_base_e_nao_do_bruto():
        # O caso que separa o certo do errado.
        # bruto 3.000,00 | INSS 258,82 | base 2.741,18
        # o BRUTO cai na faixa de 15% (2.826,66 a 3.751,05);
        # a BASE cai na faixa de 7,5% (2.259,21 a 2.826,65), que e a que vale.
        # 2.741,18 x 7,5% = 205,5885 - 169,44 = 36,1485 -> 36,15
>       assert irrf_do_salario("3000.00") == Decimal("36.15")
E       AssertionError: assert Decimal('29.74') == Decimal('36.15')
E        +  where Decimal('29.74') = irrf_do_salario('3000.00')
E        +  and   Decimal('36.15') = Decimal('36.15')

tests\test_irrf.py:46: AssertionError
________________ test_faixa_vem_da_base_tambem_com_dependentes ________________

    def test_faixa_vem_da_base_tambem_com_dependentes():
        # O segundo caso que separa o certo do errado.
        # bruto 5.000,00 | INSS 518,82 | 2 dependentes = 379,18
        # base = 5.000,00 - 518,82 - 379,18 = 4.102,00
        # o BRUTO cai na faixa de 27,5%; a BASE cai na de 22,5% (3.751,06 a 4.664,68).
        # 4.102,00 x 22,5% = 922,95 - 662,77 = 260,18
>       assert irrf_do_salario("5000.00", dependentes=2) == Decimal("260.18")
E       AssertionError: assert Decimal('232.05') == Decimal('260.18')
E        +  where Decimal('232.05') = irrf_do_salario('5000.00', dependentes=2)
E        +  and   Decimal('260.18') = Decimal('260.18')

tests\test_irrf.py:55: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_irrf.py::test_faixa_vem_da_base_e_nao_do_bruto - AssertionE...
FAILED tests/test_irrf.py::test_faixa_vem_da_base_tambem_com_dependentes - As...
2 failed, 7 passed in 0.20s

--- fim da saída ---

**C2 REPROVADO** pelo código de saída do comando de aceite. Os dependentes seguem bloqueados até `programa reabrir` e nova verificação.
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** EXECUCAO
**Objetivo:** calculadora de folha de pagamento mensal CLT: INSS, IRRF e holerite consolidado
**Ciclos:** 1/3 concluídos
  [x] C1: desconto de INSS por faixas progressivas, com teto de contribuicao
  [!] C2: desconto de IRRF sobre a base (bruto - INSS - dependentes), pela tabela progressiva com parcela a deduzir  (depende de C1)
  [ ] C3: holerite consolidado com proventos, descontos e salario liquido  (depende de C1, C2)
exit=1
```

O modelo escreveu esse código e o considerava certo. Quem discordou foi o `pytest`.

---

## Item 3 — o dependente bloqueado pelo ciclo reprovado

Três portas, e as três fechadas:

```
$ engine programa proximo
ENGINE: nenhum ciclo elegível. Há ciclo REPROVADO bloqueando dependentes — use `programa reabrir <CICLO>`.
exit=1

$ engine programa verificar C3
ENGINE: o ciclo 'C3' não pode ser verificado agora: depende de C2, que ainda não está(ão) CONCLUIDO. Nada foi executado e nada foi registrado.
  - dependência REPROVADA? `programa reabrir <CICLO>`, conserte, e `programa verificar <CICLO>` de novo;
  - dependência ainda por fazer? `programa proximo` diz qual é a vez.
exit=1

$ engine programa aceite C3 ok --porque o holerite ja esta pronto na minha cabeca
ENGINE: o ciclo 'C3' não pode ser dado por CONCLUIDO: depende de C2, que ainda não está(ão) CONCLUIDO. Um verde medido sobre dependência aberta não prova o sistema — feche a dependência primeiro (`programa reabrir` + `programa verificar`, se ela reprovou).
exit=1

$ engine programa sistema ok
ENGINE: ACEITE_SISTEMA exige todos os ciclos CONCLUIDO; faltam: C2, C3
exit=1
```

**A segunda e a terceira recusas não existiam quando este ciclo começou.** Ver "O
achado", abaixo.

---

## Item 4 — o programa só conclui depois do conserto

O conserto é uma linha: `_faixa(valor)` → `_faixa(base)`, em `folha/irrf.py`.

```
$ engine programa reabrir C2
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** EXECUCAO
**Objetivo:** calculadora de folha de pagamento mensal CLT: INSS, IRRF e holerite consolidado
**Ciclos:** 1/3 concluídos
  [x] C1: desconto de INSS por faixas progressivas, com teto de contribuicao
  [ ] C2: desconto de IRRF sobre a base (bruto - INSS - dependentes), pela tabela progressiva com parcela a deduzir  (depende de C1)
  [ ] C3: holerite consolidado com proventos, descontos e salario liquido  (depende de C1, C2)
**Próximo ciclo elegível:** C2
exit=0

$ engine programa verificar C2
**Verificando C2** — irrf_do_salario escolhe a faixa pela BASE de calculo (bruto menos INSS menos deducao por dependente), nunca pelo salario bruto, e aplica a parcela a deduzir da faixa escolhida.
**Comando de aceite:** python -m pytest tests/test_irrf.py -q
**Código de saída:** 0  ·  **Veredito:** APROVADO  ·  **Duração:** 1.024s
**Motivo:** código de saída 0
--- saída do comando (redigida, teto de 8000 caracteres) ---
.........                                                                [100%]
9 passed in 0.03s

--- fim da saída ---

**C2 CONCLUIDO** pelo código de saída do comando de aceite.
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** EXECUCAO
**Objetivo:** calculadora de folha de pagamento mensal CLT: INSS, IRRF e holerite consolidado
**Ciclos:** 2/3 concluídos
  [x] C1: desconto de INSS por faixas progressivas, com teto de contribuicao
  [x] C2: desconto de IRRF sobre a base (bruto - INSS - dependentes), pela tabela progressiva com parcela a deduzir  (depende de C1)
  [ ] C3: holerite consolidado com proventos, descontos e salario liquido  (depende de C1, C2)
**Próximo ciclo elegível:** C3
exit=0
```

C3 destravado, construído e verificado:

```
$ engine programa verificar C3
**Verificando C3** — holerite devolve bruto, inss, irrf e liquido, com liquido == bruto - inss - irrf no centavo.
**Comando de aceite:** python -m pytest tests/test_holerite.py -q
**Código de saída:** 0  ·  **Veredito:** APROVADO  ·  **Duração:** 1.081s
**Motivo:** código de saída 0
--- saída do comando (redigida, teto de 8000 caracteres) ---
...................................                                      [100%]
35 passed in 0.08s

--- fim da saída ---

**C3 CONCLUIDO** pelo código de saída do comando de aceite.
```

E o fecho:

```
$ engine programa proximo
Todos os ciclos concluídos. Rode `programa sistema {ok|falhou}`.
exit=0

$ engine programa sistema ok
**PROGRAMA CONCLUÍDO.** Aceite de sistema verde.
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** CONCLUIDO
**Objetivo:** calculadora de folha de pagamento mensal CLT: INSS, IRRF e holerite consolidado
**Ciclos:** 3/3 concluídos
  [x] C1: desconto de INSS por faixas progressivas, com teto de contribuicao
  [x] C2: desconto de IRRF sobre a base (bruto - INSS - dependentes), pela tabela progressiva com parcela a deduzir  (depende de C1)
  [x] C3: holerite consolidado com proventos, descontos e salario liquido  (depende de C1, C2)
exit=0
```

Os quatro vereditos, na trilha da cobaia, com o código de saída que os produziu:

```
2026-08-05T10:12:47 C1 APROVADO   codigo_saida=0 risco=rastreado | python -m pytest tests/test_inss.py -q
2026-08-05T10:12:51 C2 REPROVADO  codigo_saida=1 risco=rastreado | python -m pytest tests/test_irrf.py -q
2026-08-05T10:13:45 C2 APROVADO   codigo_saida=0 risco=rastreado | python -m pytest tests/test_irrf.py -q
2026-08-05T10:13:50 C3 APROVADO   codigo_saida=0 risco=rastreado | python -m pytest tests/test_holerite.py -q
```

---

## O achado: a cobaia encontrou um defeito real no ENGINE

**A2 — "aceite vermelho não avança" — valia só para quem pedia licença.**

Com C1 REPROVADO, `programa verificar C2` rodava o comando do dependente, saía 0 e
carimbava **C2 CONCLUIDO** — no parágrafo seguinte àquele em que o próprio motor
imprimiu *"Os dependentes seguem bloqueados até `programa reabrir` e nova verificação"*.
A frase era falsa. O bloqueio existia em `proximo_elegivel`, que só **sugere** o próximo
ciclo, e não em `registrar_aceite`, que é quem **decide**. `programa aceite <CICLO> ok`
tinha o mesmo buraco, e é a porta mais fácil de todas: não roda nada.

A sonda, rodada antes da correção, num programa mínimo de dois ciclos:

```
$ engine programa verificar C1
**C1 REPROVADO** pelo código de saída do comando de aceite. Os dependentes seguem bloqueados até `programa reabrir` e nova verificação.
  [!] C1: o que reprova
  [ ] C2: o dependente  (depende de C1)

--- agora o dependente C2, com C1 REPROVADO ---
**Código de saída:** 0  ·  **Veredito:** APROVADO  ·  **Duração:** 0.107s
**C2 CONCLUIDO** pelo código de saída do comando de aceite.
**Ciclos:** 1/2 concluídos
  [!] C1: o que reprova
  [x] C2: o dependente  (depende de C1)
exit=0
```

Por que isso importa, e não é preciosismo: um verde do dependente medido sobre uma
dependência quebrada não prova nada sobre o sistema — prova que o teste do pedaço passou
*apesar* de a base estar vermelha, que é justamente o caso em que o teste é o que não se
pode acreditar. E o carimbo fica: consertado C1 depois, o programa concluiria com um C2
que nunca foi verificado sobre a versão boa de C1. Nenhum dos 817 testes pegava isso —
`test_ciclo_reprovado_bloqueia_o_dependente` cobrava o bloqueio só pela via consultiva,
porque ninguém tentava fechar o dependente direto, que é o que qualquer pessoa apressada
faz quando o encadeamento reclama.

**A correção, em duas camadas.**

1. `programa.registrar_aceite` recusa `passou=True` com dependência aberta
   (`DependenciaNaoConcluida`, subclasse de `TransicaoInvalida`). O gate mora ali porque
   ali é o **único** ponto por onde passam os dois caminhos, o verificado e o digitado.
   O vermelho continua permitido: reprovar um dependente cedo é informação honesta e não
   afirma nada sobre pré-requisito satisfeito.
2. `cli._prog_verificar` faz o pré-checo **antes de executar**. Descobrir isso só no
   registro custaria o tempo de uma suíte inteira e — pior — deixaria a evidência verde
   impressa na tela e na trilha um parágrafo antes da recusa.

**Prova por mutação** (as duas camadas, uma de cada vez, sobre os 5 testes novos do
bloqueio):

| Mutação aplicada | Resultado |
|---|---|
| guarda de `registrar_aceite` desligada (CLI intacta) | **3 falhas** — as 2 de máquina e a do veredito digitado; o `verificar` seguiu barrado pelo pré-checo |
| pré-checo da CLI desligado (máquina intacta) | **1 falha** — `rodou.txt` apareceu: o comando do dependente foi executado antes da recusa |
| original restaurado | 5 passaram |

**Arquivos tocados** (única alteração de produção deste ciclo):
`ferramentas/programa.py` (exceção nova, `dependencias_pendentes`, guarda em
`registrar_aceite`), `ferramentas/cli.py` (pré-checo em `_prog_verificar`),
`ferramentas/tests/test_programa.py` (+4) e `ferramentas/tests/test_veredito_automatico.py`
(+4).

---

## O que ficou provado

| Afirmação | Onde |
|---|---|
| o ENGINE conduz um projeto de terceiro do zero à entrega, tudo pela CLI | roteiro inteiro, 17 passos |
| a macro-DESCOBERTA barra o plano até as bloqueantes serem respondidas | passos 2–5 |
| o motor **não chuta** a intenção quando o pedido não a carrega | passo 2, `exit=1` sem gravar nada |
| a porta P1 impede execução antes da aprovação do usuário | passo 6, `exit=1` |
| **APROVADO sai de código de saída 0**, sem ninguém digitar veredito | item 1 |
| **REPROVADO sai de código de saída ≠ 0**, contra código que o modelo julgava certo | item 2 |
| o dependente fica bloqueado — nas três portas | item 3 |
| o programa só conclui depois do conserto e da reverificação | item 4 |
| a cobaia é capaz de revelar defeito no próprio motor | "O achado" |

## O que este aceite NÃO prova

**O modelo continua escrevendo o código, e continua escrevendo os testes.** Não é isso que
mudou. O que mudou é que o **veredito** deixou de ser palavra dele: em `programa verificar`
não existe nenhum literal a digitar, o `Veredito` do executor recusa nascer sem código de
saída, e `julgar` olha um número e mais nada. O modelo pode escrever um teste ruim — e a
única defesa contra isso continua sendo humana, lendo a prosa do `aceite` ao lado do
comando na porta P1. Nesta cobaia a defesa foi a disciplina de calcular à mão, antes de
rodar, o valor esperado de cada caso, e de deixar a conta escrita no comentário: é o que
permite a quem audita conferir o teste **sem confiar em quem o escreveu**.

**O aceite de SISTEMA ainda é digitado.** `programa sistema ok` não roda nada. O campo
`aceite_de_sistema` é prosa: não existe `comando_de_aceite` para o sistema, não existe
`programa verificar sistema`, e o verbo nem exige `--porque` — que `programa aceite`,
para uma afirmação estritamente menor, exige. O `programa.py` diz na própria docstring que
"N ciclos verdes não provam que o sistema funciona", e é exatamente essa a afirmação que
segue sem verificação executável. **Este é o buraco que o Programa 2 não fechou.** Aqui
ele foi coberto rodando `python -m pytest -q` na cobaia à mão (53 passed) antes de digitar
`ok` — o que é disciplina de quem conduz, não propriedade da máquina. É a decisão que o
arquiteto precisa tomar; não foi tomada neste ciclo porque muda o contrato do plano.

**O `programa.json` não guarda memória da reprovação.** Depois de `reabrir` +
reverificação, C2 aparece `CONCLUIDO` e nada no arquivo diz que ele já reprovou. Só a
trilha guarda (`REPROVADO codigo_saida=1`). É defensável — o registro auditável é a trilha
—, mas quem ler só o `programa.json` vê um programa em que nunca nada deu errado.

**O palpite da elicitação errou por texto.** O pedido "folha de **pagamento** mensal" fez
o motor inferir `LOJA_PAGAMENTOS` com confiança ALTA. A inferência está errada (é folha de
salário, não loja), e o mecanismo se comportou como desenhado: palpite **não aplicado**,
listado, e resolvido por `descoberta --programa recusar LOJA_PAGAMENTOS`. Vale registrar
que, tivesse sido confirmado no automático, um bloco inteiro de perguntas sobre cobrança
teria entrado numa entrevista sobre holerite.

**Escala.** Três ciclos, um sistema pequeno, um só desenvolvedor, uma sessão. Nada aqui
diz o que acontece com vinte ciclos, dependências cruzadas e duas sessões concorrentes —
para isso existem os testes de concorrência do motor, que são outra coisa.

---

## Veredito

**P2C5 aprovado.** Os quatro itens do critério de aceite foram rodados literalmente e
estão colados acima: APROVADO por código de saída 0, REPROVADO por código de saída 1,
dependente bloqueado nas três portas, e o programa concluindo só depois do conserto.

O ciclo entregou mais do que o combinado: a cobaia encontrou um defeito real no ENGINE —
A2 aplicada apenas no caminho consultivo — que 817 testes não pegavam, e que só apareceu
porque alguém tentou fazer, num projeto de verdade, o que uma pessoa apressada faria.
Está corrigido, com prova por mutação das duas camadas, e a suíte fechou em 825 verdes.

O que continua sendo palavra do modelo, e este documento não disfarça: o **código**, os
**testes** e o **aceite de sistema**. O veredito de cada ciclo, não.
