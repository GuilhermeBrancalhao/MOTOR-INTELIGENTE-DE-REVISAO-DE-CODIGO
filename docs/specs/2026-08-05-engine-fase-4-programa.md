# ENGINE — Fase 4: modo PROGRAMA

- **Data:** 2026-08-05
- **Estado:** desenho proposto, implementação não iniciada
- **Autor das decisões:** o usuário; escolhas registradas na seção 3
- **Pré-requisito:** Fases 1–3 em `master` (`154526f`), 478 testes verdes

---

## 1. Problema

O ENGINE hoje conduz **um ciclo**. Um sistema de alta complexidade não é um ciclo — é uma
sequência deles, com dependências entre si.

Na prática isso significa que, para construir um sistema inteiro, o usuário precisa ser o
operador: ligar o ciclo, atravessar as fases, desligar, decidir qual é o próximo objetivo,
ligar de novo. O motor garante o rigor **dentro** de cada ciclo e não tem opinião alguma
sobre a sequência. Toda a memória de "onde estamos no sistema" vive fora da máquina — na
cabeça do usuário ou num documento que ninguém valida.

Isso tem três consequências mensuráveis:

1. **A decomposição não é auditada.** Nada verifica se os ciclos planejados cobrem o sistema,
   nem se as dependências entre eles fazem sentido. A doutrina do volume `38-PROJECT-PLANNER`
   existe no acervo e não é exercida por nenhuma máquina.
2. **Não existe critério de "o sistema está pronto".** Cada ciclo fecha com sua própria
   ENTREGA. Vinte ciclos verdes não provam que o sistema liga — provam que vinte pedaços
   passaram nos próprios testes. É o mesmo defeito que a auditoria de 2026-08-03 encontrou no
   acervo: 42 volumes "entregues" que eram esqueletos.
3. **A parada obrigatória no PLANO, por ciclo, é cara no lugar errado.** Ela existe para o
   usuário aprovar arquitetura. Num programa de 20 ciclos, 19 dessas paradas são conformidade
   com uma arquitetura que ele já aprovou uma vez.

A Fase 4 resolve isso acrescentando **uma camada acima do ciclo** — não alterando o ciclo.

## 2. Escopo

**É:** um modo de operação (`programa`) em que o motor conduz uma sequência de ciclos
derivada de um plano-mestre aprovado pelo usuário, encadeando-os automaticamente enquanto a
execução for conforme ao plano, e fechando com um aceite de sistema.

**Não é:**
- Um afrouxamento das portas de risco. As famílias R1–R9 valem **idênticas** em modo programa.
  Autonomia de processo não é autonomia de risco (ver D3 da spec de desenho original).
- Um substituto do julgamento de arquitetura. A porta do plano-mestre permanece obrigatória.
- Uma promessa de que o modelo escreve sistemas complexos sem erro. O motor garante que
  **nada avança sem evidência**; a qualidade do que é escrito continua sendo do modelo.

**Fronteira com o ciclo atual.** O ciclo (`DESCOBERTA → … → ENTREGA`) fica **inalterado**:
mesmo grafo, mesmas fases, mesmos papéis, mesmos gates. O programa é um orquestrador que liga
ciclos, observa suas ENTREGAs e decide o próximo. Nenhuma linha de `TRANSICOES` muda.

## 3. Decisões fixadas

| # | Decisão | Alternativas descartadas | Razão |
|---|---|---|---|
| P1 | **Porta única no plano-mestre.** O usuário aprova a decomposição e a arquitetura uma vez; os ciclos seguintes encadeiam sem parada | parada por ciclo; autonomia total sem porta | a parada por ciclo vira aprovação automática — o defeito que D3 já identificou; autonomia total deixa arquitetura errada correr até o fim |
| P2 | **Parada por exceção, não por etapa.** O motor só interrompe se o ciclo precisar desviar do plano-mestre | notificação a cada ciclo | interrupção que sempre acontece deixa de ser sinal; ver a lição do falso positivo em R8 |
| P3 | **Estado do programa em arquivo próprio** (`.engine/programa.json`), separado de `estado.json` | um só arquivo com tudo | o ciclo já tem cadeado e semântica próprias; misturar faria um `desligar` de ciclo destruir o programa |
| P4 | **ACEITE-DE-SISTEMA é fase do programa, não de ciclo** | confiar na soma das ENTREGAs | N ciclos verdes não provam integração; sem essa fase o programa herda o defeito dos "42 volumes entregues" |
| P5 | **Critério de aceite por ciclo é declarado no plano-mestre e é falsificável** | descrição em prosa livre | volume `04-REQUIREMENTS`: requisito é enunciado que pode ser falso; sem isso o encadeamento não tem como decidir se o ciclo passou |
| P6 | **Gates R1–R9 inalterados em modo programa** | relaxar R2 para permitir push automático | o que é caro de desfazer continua caro de desfazer, e ninguém está olhando — em modo autônomo o gate vale *mais*, não menos |
| P7 | **O programa é retomável** — sessão nova reentra pelo `programa.json` | manter em memória de sessão | é a mesma propriedade que faz o cartão sobreviver à compactação: função apenas do disco |

## 4. Arquitetura

### 4.1 Máquina de estados do programa

```
                    ┌─────────────────────────────────┐
                    │                                 │
[*] → CONCEPCAO → PLANO_MESTRE → ⟨PORTA⟩ → EXECUCAO ──┴→ ACEITE_SISTEMA → CONCLUIDO
                                     ↑         │
                                     │         ↓
                                     └──── DESVIO ⟨PORTA⟩
```

| Estado | O que acontece |
|---|---|
| `CONCEPCAO` | Macro-DESCOBERTA: objetivo real do sistema, requisitos, restrições, riscos. Papel `descobridor` |
| `PLANO_MESTRE` | Decomposição em ciclos com dependências, stack e critério de aceite por ciclo. Papéis `arquiteto` + `designer` |
| ⟨PORTA⟩ | **Parada obrigatória.** Apresenta o plano-mestre e espera o usuário. Única parada garantida do programa |
| `EXECUCAO` | Liga o próximo ciclo elegível, acompanha até a ENTREGA, verifica o aceite, marca e repete |
| `DESVIO` | Um ciclo precisa contrariar o plano-mestre. Para, apresenta o conflito, espera decisão |
| `ACEITE_SISTEMA` | Todos os ciclos concluídos. Roda a suíte completa e o cenário de ponta a ponta declarado na concepção |
| `CONCLUIDO` | Aceite de sistema verde. O programa fecha com relatório |

### 4.2 `.engine/programa.json`

```json
{
  "versao": 1,
  "programa": "2026-08-05-1",
  "objetivo": "<uma frase>",
  "estado": "EXECUCAO",
  "aceite_de_sistema": "<comando ou cenário falsificável>",
  "ciclos": [
    {
      "id": "C1",
      "objetivo": "<uma frase>",
      "depende_de": [],
      "aceite": "pytest tests/ingestao -q sai 0 e cobre CSV de 3 bancos",
      "status": "CONCLUIDO",
      "ciclo_do_estado": "2026-08-05-1"
    },
    {"id": "C2", "objetivo": "…", "depende_de": ["C1"], "aceite": "…", "status": "ATIVO"},
    {"id": "C3", "objetivo": "…", "depende_de": ["C1"], "aceite": "…", "status": "PENDENTE"}
  ]
}
```

`depende_de` é **acíclico** e valida na porta — a mesma regra que o acervo já aplica a
`depende_de` de volume, e pelo mesmo motivo: ciclo de dependência trava a execução sem
mensagem clara.

### 4.3 Como o encadeamento decide

Ao fim de um ciclo (`estado.json` em `ENTREGA`), o orquestrador:

1. Lê o `aceite` do ciclo no plano-mestre.
2. Verifica a evidência **na trilha**, não na afirmação do modelo — a trilha já carimba
   `do_motor` e separa por `ciclo`, e a lição de 2026-07-31 é exatamente essa: o gate lia como
   evidência uma linha que o próprio motor havia escrito.
3. Aceite verde → marca `CONCLUIDO`, escolhe o próximo ciclo com `depende_de` satisfeito, liga.
4. Aceite vermelho → **não avança**. Reabre o mesmo ciclo em BUILD (o grafo já permite
   `TESTE → BUILD`) ou entra em `DESVIO` se o aceite for inalcançável como escrito.

### 4.4 O que dispara `DESVIO`

Apenas quatro condições, todas verificáveis:

1. Um ciclo precisa de stack fora da declarada no plano-mestre.
2. Um ciclo descobre dependência não prevista (grafo muda).
3. O aceite declarado é inalcançável como escrito (requisito falso — e o volume 04 diz que
   requisito é justamente um enunciado que pode ser falso).
4. Um ciclo precisaria tocar em arquivo fora do escopo declarado (invariante 4).

Fora disso, o motor não pergunta. Pergunta que sempre acontece deixa de ser sinal.

## 5. Verbos novos

| Comando | Efeito |
|---|---|
| `cli.py programa "<objetivo>"` | Cria o programa e entra em `CONCEPCAO` |
| `cli.py programa status` | Estado do programa, ciclos, progresso |
| `cli.py programa aprovar` | Passa a porta do plano-mestre → `EXECUCAO`. **Só o usuário roda** |
| `cli.py programa proximo` | Liga o próximo ciclo elegível (usado pelo orquestrador) |
| `cli.py programa retomar` | Reentra num programa existente em sessão nova |
| `cli.py programa relatorio` | Relatório do programa inteiro, com um resumo por ciclo |
| `cli.py programa abortar` | Encerra o programa preservando a trilha |

`programa aprovar` é o único verbo do motor que **não** pode ser executado como consequência
de raciocínio do modelo — é a materialização da porta P1. A skill declara isso explicitamente.

## 6. Casos de aceite da Fase 4

Falsificáveis, no padrão das fases anteriores. Cada um nomeia a mutação que o derruba.

| # | Caso | Mutação que deve reprovar |
|---|---|---|
| A1 | `programa` com 3 ciclos encadeia C1→C2→C3 sem intervenção | remover a verificação de aceite faz C2 ligar com C1 vermelho |
| A2 | Ciclo com aceite vermelho **não** avança | trocar o predicado por `True` faz o programa concluir com teste falhando |
| A3 | `depende_de` cíclico é recusado **na porta** | remover a checagem trava a execução sem mensagem |
| A4 | `EXECUCAO` não começa sem `programa aprovar` | permitir avanço automático anula P1 |
| A5 | Programa sobrevive a sessão nova (`retomar`) | ler estado de memória em vez do disco quebra o caso |
| A6 | R1–R9 travam igual em modo programa | qualquer exceção por modo reabre o buraco que D3 fechou |
| A7 | `ACEITE_SISTEMA` vermelho impede `CONCLUIDO` | pular a fase reproduz o defeito dos "42 volumes entregues" |
| A8 | Desvio de stack para e pergunta | não parar deixa o programa mudar de arquitetura sozinho |

## 7. O que esta fase explicitamente **não** resolve

Registrado para não virar promessa implícita:

- **Não garante qualidade de arquitetura.** Garante que a arquitetura foi aprovada por um
  humano e que a execução não se desviou dela sem avisar. Arquitetura errada executada com
  disciplina perfeita continua sendo sistema errado.
- **Não paraleliza ciclos.** Ciclos independentes rodam em sequência nesta fase. Paralelismo
  exigiria vários `estado.json`, e o arquivo único acabou de ser endurecido contra
  concorrência (`131c14e`) justamente por ser único.
- **Não estima prazo nem custo.** O plano-mestre ordena e sequencia; não promete quando.
- **Não substitui o ACEITE por cliente.** O aceite de sistema é técnico (o sistema liga e
  passa no cenário declarado), não de negócio.

## 8. Ordem de implementação sugerida

1. `ferramentas/programa.py` — estado, transições, validação de DAG, cadeado (reaproveita o
   de `estado.py`).
2. Testes de `programa.py` por mutação, cobrindo A1–A8.
3. Verbos na CLI + mensagens de erro sem traceback (regra já vigente).
4. Orquestração na skill: como o modelo conduz `EXECUCAO` chamando `programa proximo`.
5. Cenário de aceite ponta a ponta em `aceite/fase-4.md`, com saída literal colada.
6. Cobaia real: a plataforma de conciliação multi-banco, em repositório próprio.

O passo 6 é o que responde, com evidência, a pergunta que originou esta fase — *"o ENGINE é
capaz de desenvolver o sistema inteiro?"*. Até ele, a resposta continua sendo "por
construção, não por execução".
