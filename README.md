# ENGINE

Um motor de engenharia persistente para o [Claude Code](https://claude.com/claude-code),
empacotado como plugin.

> ⚠️ **Hoje só funciona no Windows.** Os hooks são lançados com `py`, o Python Launcher, que
> não existe em macOS nem Linux. Veja [Outras plataformas](#outras-plataformas) — é uma linha
> para trocar, mas a troca não foi testada fora do Windows.

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
painel de controle.

## Instalação

Requer Claude Code e Python 3.11+.

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

Você deve ver `Skills (1)`, `Agents (9)` e `Hooks (5)`.

### Outras plataformas

`hooks/hooks.json` lança os cinco hooks com `"command": "py"`. Em macOS e Linux, troque `py`
por `python3` nas cinco entradas. **Isso não foi testado** — e a falha, se houver, é silenciosa
e perigosa: se o hook não iniciar, o classificador de risco simplesmente não existe, enquanto
você acredita estar protegido. Antes de confiar nele fora do Windows, rode
`python aceite/verificar_familias.py`, que dispara os hooks de verdade como subprocesso e
confirma que as famílias travadas travam.

## Uso

```bash
/engine:engine <o que você quer construir>
```

O motor entra em DESCOBERTA, e a partir daí o cartão de estado aparece a cada turno.

| Comando | Efeito |
|---|---|
| `/engine:engine <pedido>` | liga o motor e cria o ciclo |
| `/engine:engine status` | fase, ciclo, decisões, arquivos tocados, pendências |
| `/engine:engine off` | desliga e gera o relatório do ciclo |
| `/engine:engine retomar` | reconstrói o estado numa sessão nova |

## Testes

```bash
python -m pytest ferramentas/tests -v
```

266 testes, apenas biblioteca padrão do Python — nenhuma dependência de runtime.

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

**O que ainda não foi provado.** O motor nunca rodou dentro de uma sessão real do Claude Code
por tempo suficiente para provar a tese central. `aceite/simular_turnos.py` simula vinte turnos
e uma compactação chamando os hooks reais, o que demonstra a **mecânica** — mas simulação não é
sessão. Até que isso seja verificado, trate "sobrevive à compactação" como projeto, não como
fato observado.

Também pendente: os quatro cenários de aceite com projetos-cobaia, e o suporte real a
plataformas não-Windows.

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
