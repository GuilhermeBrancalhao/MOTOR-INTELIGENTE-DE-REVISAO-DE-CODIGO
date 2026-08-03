# ENGINE

Um motor de engenharia persistente para o [Claude Code](https://claude.com/claude-code),
empacotado como plugin.

## O problema que ele resolve

Um "modo de engenharia" para o Claude Code costuma ser tentado como **um prompt longo** colado
numa skill. Isso não funciona, e o motivo é mecânico e não estético: a skill carrega **uma
única vez**, no turno em que é invocada. A cada mensagem seguinte o texto afunda no contexto,
perde peso relativo, e na primeira compactação desaparece. Na prática você observa um
comportamento excelente por três ou quatro turnos, seguido de regressão silenciosa ao padrão —
sem nenhum aviso de que o modo caiu.

O ENGINE troca texto por **estado em disco**. O ciclo vive em `.engine/estado.json` no projeto
onde você trabalha, e um hook `UserPromptSubmit` relê esse arquivo e reinjeta um cartão de no
máximo 40 linhas **a cada turno**. Não é o texto de nenhuma skill que sustenta o modo; é o
hook.

## O que ele faz

**Um ciclo de fases** que uma máquina acompanha, não uma instrução que o modelo pode esquecer:

```
DESCOBERTA → ANÁLISE → [EVOLUÇÃO, se o projeto já existe] → PLANO → ⟨porta⟩
  → BUILD ⇄ TESTE → REVISÃO → DOC → ENTREGA
```

Transição fora desse grafo é recusada em código. A **porta** depois do PLANO é a única parada
obrigatória por fase: o motor apresenta arquitetura, stack e a justificativa de cada decisão, e
espera.

**Nove papéis**, despachados por fase — `descobridor`, `cartografo`, `arquiteto`, `designer`,
`implementador`, `testador`, `revisor`, `sentinela`, `documentador`. Só o `implementador` tem
escrita ampla; quem revisa não conserta em silêncio, e essa garantia é estrutural (o `revisor`
não recebe ferramenta de execução), não uma instrução que ele possa contrariar.

**Doze cartões de tecnologia**, carregados sob demanda conforme a stack detectada no projeto.
Tecnologia nova custa um arquivo de ~60 linhas, não um agente novo.

**Cinco motores de critério** em `motores/` — `revisar-codigo`, `otimizar-performance`,
`arquitetar-sistema`, `materializar-ideia`, `diagramar`. O cartão de cada turno lista os
motores consultáveis da fase atual (nome + `description` do `SKILL.md` de cada um):

| Fase | Motores consultáveis |
|---|---|
| PLANO | `arquitetar-sistema`, `materializar-ideia` |
| EVOLUÇÃO | `arquitetar-sistema` |
| BUILD | `materializar-ideia`, `revisar-codigo` |
| REVISÃO | `revisar-codigo`, `otimizar-performance` |
| DOC | `diagramar` |

Fora de DESCOBERTA e ANÁLISE, o hook também analisa o `git diff` local e, quando o padrão do
código pede um motor específico, acrescenta a sugestão ao cartão.

**Volumes de conhecimento PRONTO**, detectados dinamicamente — nenhuma lista hardcoded no
código. Todo diretório em `volumes/prontos/<NOME>/` entra no cartão como consultável se o seu
`_VOLUME.yml` declara `status: PRONTO` (qualquer outro status fica de fora; sem `_VOLUME.yml`,
vale o fallback: basta ter `README.md` ou capítulos `.md`). O resumo mostrado vem do campo
`escopo:` do `_VOLUME.yml`, senão da primeira linha não-vazia do `README.md`. Criar um volume
novo não exige mudar código nenhum — a descoberta usa cache com TTL de 300 s.

**Quem escreve esses volumes mora aqui também**, em `acervo/` — a plataforma de engenharia de
projetos de IA, com o seu contrato legível por máquina, os seus três gates e os seus 42
volumes. `volumes/prontos/` deixou de ser cópia mantida à mão e passou a ser **artefato
derivado**: quem gera é `ferramentas/sincronizar.py`, a partir do `status` que o acervo declara.

```bash
py -m ferramentas.sincronizar --verificar   # a cópia está em dia com o acervo?
py -m ferramentas.sincronizar               # regenera
```

Não edite nada dentro de `volumes/prontos/`: a próxima sincronização sobrescreve, e o teste
`test_a_copia_do_plugin_esta_em_dia` reprova a suíte se os dois lados divergirem. Foi
exatamente essa deriva que motivou a unificação — a cópia chegou a carregar `31-TESTING`
marcado `PRONTO` enquanto a fonte dizia `RASCUNHO`, e a nunca entregar `03-DISCOVERY`, que era
`PRONTO` de verdade.

As duas suítes rodam separadas, porque cada uma tem o seu próprio pacote `ferramentas`:

```bash
py -m pytest                  # motor  — 449 testes
cd acervo && py -m pytest     # acervo — 455 testes
```

**Um classificador de risco** que roda antes de cada ação:

| Nível | O que acontece |
|---|---|
| `travado` | bloqueia e pede confirmação humana |
| `rastreado` | executa, e aparece no relatório da fase |
| `livre` | executa em silêncio |

## A decisão de projeto que mais importa

**Comando de shell nunca é `livre`** — ou trava, ou é rastreado. Só operação de arquivo pode
ser livre.

Isso não foi a intenção original. O classificador nasceu como uma lista de proibições, e sete
rodadas de revisão adversarial encontraram doze contornos — cada rodada achava outro:
`bash -c "rm"`, `echo $(rm -rf)`, quebra de linha depois de um `echo`, `cmd /c del`,
`git -c core.fsmonitor=./script status`, `git diff --output=`.

A causa é estrutural, não descuido: **cada comando de shell é ele próprio uma linguagem**, com
aspas, substituição, apelidos e variantes por plataforma. Enumerar o que é perigoso não
termina. Então o default foi invertido — o que não é comprovadamente inócuo é auditado, e um
teste (`test_nenhum_comando_de_shell_e_livre`) trava essa política contra reintrodução
acidental.

O mesmo raciocínio produziu a família **R9**: escrita em `.engine/` é travada, porque sem ela
gravar `{"ativo": false}` no estado desligava os dois hooks — o motor não protegia o próprio
painel de controle. Uma auditoria adversarial posterior acrescentou mais três famílias pelo
mesmo caminho: **R10** (escrita em caminho de execução persistente — `.git/hooks/`,
`.claude/`, init de shell — que a política de "arquivo novo é livre" deixava invisível),
**R11** (destruição de dados sem verbo de apagar: `truncate`, `dd of=`, `robocopy /MIR`,
`format`) e **R12** (comando acima do teto de 20.000 caracteres **trava** em vez de ser
analisado — travar é o lado certo do erro, porque varrer as famílias sobre um comando
gigante era um vetor de negação de serviço por regex). A lista fechada hoje vai de R1 a R12;
a seção 5 da especificação documenta cada uma com o vetor que a motivou.

## Requisitos

- [Claude Code](https://claude.com/claude-code).
- Python 3.11+, alcançável no PATH como `py` (Windows), `python3` ou `python` — o lançador
  (`hooks/engine.sh`) tenta os três, nessa ordem.
- **No Windows, [Git Bash](https://git-scm.com/downloads/win)** (instalado junto com o Git para
  Windows). Os cinco hooks usam a forma shell do `hooks.json`, que no Windows roda em Git Bash;
  sem ele, o Claude Code cai para PowerShell, onde `hooks/engine.sh` — um script bash — não
  executa.

Se nenhum interpretador Python for encontrado no PATH, o hook `PreToolUse` (o classificador de
risco) **trava toda ação de ferramenta de propósito**, com uma mensagem em stderr explicando o
motivo. Isso é comportamento desejado, não defeito: um gate de segurança que não consegue rodar
tem que bloquear, nunca liberar em silêncio. Os outros quatro hooks (`UserPromptSubmit`,
`PostToolUse`, `PreCompact`, `Stop`), em contraste, saem em silêncio quando não acham Python —
eles nunca podem atrapalhar o turno do usuário.

## Instalação

```bash
git clone https://github.com/AlphaContabilidade/planejamento-do-motor-de-revisao-de-codigo.git ENGINE
```

Depois, dentro do Claude Code (use o **caminho absoluto**; caminho relativo tem bug conhecido):

```bash
/plugin marketplace add C:\caminho\completo\para\ENGINE
```

```bash
/plugin install engine@engine-marketplace
```

Escolha escopo **user** para o plugin valer em todos os seus projetos. Abra uma janela nova —
plugin só carrega no início da sessão.

Confirme com:

```bash
claude plugin details engine
```

Você deve ver `Skills (2)`, `Agents (9)` e `Hooks (5)`.

## Uso

```bash
/engine:engine <o que você quer construir>
```

O motor entra em DESCOBERTA, e a partir daí o cartão de estado aparece a cada turno.

| Comando | Efeito |
|---|---|
| `/engine:engine <pedido>` | liga o motor e cria o ciclo |
| `/engine:engine <pedido> --dry` | ciclo em modo seco: planeja e relata, **não escreve nada** |
| `/engine:engine status` | fase, ciclo, decisões, arquivos tocados, pendências |
| `/engine:engine relatorio` | relatório do ciclo (ou de uma fase) a partir da trilha |
| `/engine:engine retomar` | reconstrói o estado numa sessão nova |
| `/engine:engine off` | desliga e gera o relatório do ciclo |

O modo seco é o jeito de conhecer o motor sem risco: ele percorre as fases, apresenta o
plano e relata, mas o classificador de risco rebaixa toda escrita para travada.

## Testes

```bash
python -m pytest ferramentas/tests -v
```

436 testes, apenas biblioteca padrão do Python — nenhuma dependência de runtime.

Além deles, dois scripts de aceite disparam os hooks de verdade como subprocesso:

```bash
python aceite/verificar_familias.py
python aceite/simular_turnos.py
```

## Estado

**Fases 1 e 2 completas**, mescladas em `master`. Estão no repositório e cobertos por testes:
`ferramentas/` (configuração, classificador de risco, máquina de fases, detecção de stack,
trilha, relatório e a CLI), os cinco hooks (`PreToolUse`, `UserPromptSubmit`, `PostToolUse`,
`PreCompact`, `Stop`), a skill, os nove papéis, os doze cartões e o empacotamento como plugin.

**O que já foi observado em sessão real.** Em 2026-07-31 o plugin foi instalado e rodou
dentro de uma sessão real do Claude Code, e três coisas foram observadas — não simuladas:
o hook `UserPromptSubmit` injetou o cartão `== ENGINE ativo ==` no contexto do turno; o
hook `PreToolUse` travou um `git push` pela família R2 (inclusive o push do próprio
código-fonte deste projeto); e o mesmo hook travou um `python -c` pela família R8 — um
falso positivo, corrigido depois: a string `'EXEC(ruim)'` casava `\bexec\(` porque o
padrão era compilado sem distinguir maiúsculas. Isso prova que o **mecanismo** funciona
numa sessão real; não é uma declaração de vitória.

**O que ainda não foi provado.** A **durabilidade**: o motor nunca atravessou uma sessão
longa com compactação de verdade. `aceite/simular_turnos.py` simula vinte turnos e uma
compactação chamando os hooks reais, o que demonstra a mecânica — mas simulação não é
sessão. Até que isso seja verificado, trate "sobrevive à compactação" como projeto, não
como fato observado.

Também pendente: os quatro cenários de aceite com projetos-cobaia. O lançador
(`hooks/engine.sh`) tem suíte automatizada (`ferramentas/tests/test_lancador.py`) cobrindo os
cenários de PATH via subprocesso, mas **nunca rodou numa máquina macOS ou Linux de verdade** —
só sob Git Bash no Windows, onde a forma shell também roda.

## Documentação

| | |
|---|---|
| Especificação de desenho | `docs/specs/2026-07-30-engine-design.md` |
| Plano de implementação | `docs/plans/` |
| Histórico e decisões | `CHANGELOG.md` |
| Registros de aceite | `aceite/` |

A especificação explica cada decisão com a alternativa que foi descartada e a razão. Se você
for mexer no classificador de risco, leia a seção 5 antes — ela documenta por que a política
atual é a que é, e sete rodadas de revisão estão por trás dela.

## Licença

MIT. Veja [LICENSE](LICENSE).
