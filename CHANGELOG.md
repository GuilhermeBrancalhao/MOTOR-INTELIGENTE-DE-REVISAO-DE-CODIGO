# CHANGELOG

## 2026-07-31 — Hooks portáteis (Windows/macOS/Linux)

`hooks/hooks.json` lançava os cinco hooks pela forma exec do Claude Code com
`"command": "py"` — o Python Launcher, que só existe no Windows. Em macOS/Linux
o hook falhava ao iniciar, silenciosamente: sem interpretador, o classificador
de risco (`PreToolUse`) simplesmente não rodava, e nada avisava disso.

- **`hooks/engine.sh` (novo).** Lançador bash que decide o interpretador em
  runtime: tenta `py`, `python3`, `python`, nessa ordem, usando só `command -v`
  (nunca executa o candidato para sondar — o `PreToolUse` dispara a cada
  chamada de ferramenta, e sondar custaria latência em todas elas). Descarta
  qualquer caminho que contenha `WindowsApps` — o stub que o Windows registra
  quando não há Python instalado, que abre a Microsoft Store em vez de rodar
  código; confirmado nesta própria máquina (`command -v python3` resolve para
  o stub, `py` resolve para um Python de verdade). Achado o interpretador,
  `exec` troca o processo do shell pelo dele, repassando stdin/stdout/stderr e
  o código de saída intactos — só ele decide se a ação é bloqueada (`exit 2`).
  Com a flag `--travar-sem-python` (usada só no `PreToolUse`) e nenhum Python
  encontrado, sai `2` com mensagem explicando que o gate de segurança não está
  protegendo nada; sem a flag (os outros quatro hooks), sai `0` em silêncio —
  eles nunca podem atrapalhar o turno do usuário.
- **`hooks/hooks.json` migrado para a forma shell.** As cinco entradas
  perderam `args` e ganharam `"shell": "bash"` explícito; `command` passou a
  ser a string `"${CLAUDE_PLUGIN_ROOT}/hooks/engine.sh" ... "${CLAUDE_PLUGIN_ROOT}/hooks/engine_*.py"`,
  com aspas em cada caminho (`CLAUDE_PLUGIN_ROOT` tem espaço/acento nesta
  máquina). A forma shell entrega a string a um shell de verdade — Git Bash no
  Windows, `sh`/`bash` em macOS/Linux — em vez de resolver `command`
  literalmente no PATH sem shell (o que a forma exec fazia, e por isso não
  tinha como decidir o interpretador em runtime).
- **Bit de execução registrado no git** (`git update-index --chmod=+x`,
  modo `100755`) e `.gitattributes` novo forçando `eol=lf` em `*.sh` — sem
  isso, `core.autocrlf=true` (ativo neste repositório) injetaria `\r` no
  script no próximo checkout, quebrando o shebang e as comparações de string.
- **`ferramentas/tests/test_lancador.py` (novo, 5 testes).** Cobre, via
  subprocesso e PATH controlado: repasse de stdin e código de saída com Python
  disponível; trava (`exit 2`, stderr menciona Python) com PATH vazio e
  `--travar-sem-python`; saída silenciosa (`exit 0`, stdout vazio) com PATH
  vazio e sem a flag; caminho de script com espaço e acentuação; e o descarte
  do stub `WindowsApps` reproduzindo o caso real desta máquina. Todo o módulo
  é pulado se `bash` não estiver no PATH. Suíte: **266 → 271 testes verdes**.
- **`README.md`**: removido o aviso de suporte só-Windows e a seção "Outras
  plataformas"; nova seção "Requisitos" pede Git Bash no Windows (a forma
  shell cai para PowerShell sem ele, onde o lançador bash não roda) e explica
  com franqueza que a trava sem Python é intencional, não defeito.

## 2026-07-31 — Fase 2, revisão adversarial

Seis correções apontadas por revisão adversarial da branch `feat/fase-2`, todas
verificadas por execução antes de serem reportadas. Suíte: **247 → 261 testes
verdes**; `aceite/fase-2.md` reexecutado e atualizado.

- **O gate nunca cobrava em operação real (CRÍTICO).** O único jeito de entrar em
  BUILD/TESTE/REVISAO é rodar `ferramentas/cli.py fase <DESTINO>` por um comando de
  shell — e esse comando dispara o `PostToolUse`, que gravava na trilha uma linha já
  carimbada com a fase NOVA. O gate lia isso como evidência de trabalho e saía 0
  sempre. Os 9 testes que passavam mudavam a fase pela API (`estado.transicionar`),
  nunca pela CLI, e por isso não viam o buraco. `engine_trilha.py` passa a marcar
  `do_motor: true` nas ações que são chamadas da própria CLI, e `engine_gate.py` as
  ignora ao procurar evidência da fase. Teste novo reproduz o caminho real
  (transição pela CLI em subprocesso → `engine_trilha` sobre o mesmo comando → Stop).
- **Segredo em texto puro na trilha (CRÍTICO).** `psql
  "postgresql://admin:senha@db.prod/app"` e `curl -H "Authorization: Bearer sk-…"`
  são `rastreado` (executam) e iam literais para `.engine/trilha.jsonl`, de onde
  `relatorio.de_fase` e o verbo `retomar` os traziam de volta ao contexto. Nova
  `trilha.redigir` substitui por `«redigido»` senha embutida em URL, valor de
  cabeçalho `Authorization:` e os padrões de credencial de `ferramentas/risco.py`
  (reutilizados por referência — `risco.py` segue selado). Aplicada em `registrar`
  (o dado não chega ao disco em claro) e também na impressão do relatório e do
  `retomar` (defesa em profundidade, para trilhas gravadas antes desta correção).
- **A trilha não separava ciclos (CRÍTICO).** `novo_ciclo` zera o estado mas não a
  trilha (append-only por contrato), e o relatório do ciclo 2 contava as ações do
  ciclo 1 — número errado, não só verboso. Cada linha passa a carregar o `ciclo` que
  a gerou; `de_ciclo`/`de_fase` filtram pelo ciclo corrente e dizem quantas linhas
  sem id ignoraram. Junto: `_arquivos_tocados` deixou de ser O(n²) e nenhum
  relatório passa de 300 linhas (corta a listagem e diz quantas omitiu). Medido numa
  trilha de 50 mil linhas: 23,5 s / 3,1 MB impressos → 0,33 s / 12,9 KB.
- **Falso positivo grosseiro na detecção de stack.** Um projeto com `main.py` +
  `dados.db` + `schema.sql` disparava `fastapi`, `postgresql` **e** `sqlite`.
  `detectar:` passa a aceitar só âncora forte (regra documentada em
  `cartoes/_catalogo.md`): saíram `main.py`/`dependencies.py` (fastapi), `*.sql`
  (postgresql), `*.db` (sqlite), `*.cls` (excel-vba, colide com LaTeX e Apex) e
  `*.ts` solto (typescript). Onde não há âncora forte possível por nome de arquivo,
  a escolha é NÃO detectar — carregar cartão errado propaga o erro para todo o ciclo.
- **`agents/sentinela.md` e `agents/designer.md` prometiam o que as `tools` proíbem.**
  O sentinela dizia invocar `ecc:security-reviewer`/`ecc:performance-optimizer` sem
  ter ferramenta de despacho; o designer dizia consumir o MCP `open-design` sem ter
  tool de MCP. O TEXTO dos dois foi ajustado ao que eles realmente fazem. O sentinela
  **continua sem Bash e sem escrita** de propósito — é a garantia estrutural de que
  ele não conserta em silêncio; despacho a partir dele fica registrado como item de
  Fase 3, não como promessa.
- **`aceite/simular_turnos.py`: verificação tautológica e gate não exercitado.** A
  verificação (a) comparava o cartão do turno 20 com a fase lida do mesmo disco —
  apagando as duas transições do meio, continuava verde. Agora afirma o valor
  literal (`PLANO`), e apagar as transições faz falhar (confirmado por execução).
  O roteiro ganhou o quinto hook: `engine_gate.py` é disparado pelo caminho real de
  entrada na fase e verifica que cobra uma vez (f) e não cobra na segunda (g).

## 2026-07-31 — Fase 2 (elenco)

Completa o elenco do motor: 247 testes verdes (eram 152 ao fim da Fase 1) e
verificação de aceite em `aceite/fase-2.md`, incluindo um roteiro NOVO
(`aceite/simular_turnos.py`) que fecha o critério "sobrevive a 20 turnos e a uma
compactação", deixado explicitamente não verificado pela Fase 1.

- **`ferramentas/detectar.py` — detecção de stack.** Lê o front-matter restrito
  (`tecnologia`/`detectar`/`papeis`/`versao`) de cada cartão em `cartoes/` e varre o
  projeto hospedeiro (profundidade máx. 6, ignora `.git`/`node_modules`/
  `__pycache__`/`.venv`/`.engine`) para decidir quais tecnologias estão presentes.
  `estado.cartoes` é preenchido por essa detecção quando um ciclo liga.
- **`ferramentas/trilha.py` + hook `engine_trilha.py` (PostToolUse).** Trilha
  append-only em `.engine/trilha.jsonl`, uma linha JSON por ação (`quando`, `fase`,
  `ferramenta`, `alvo`, `risco`, `regra`). É a fonte de verdade para os relatórios —
  nunca o índice de uma API externa. Registrar é acessório: erro de escrita nunca
  propaga; leitura pula linha corrompida e reporta em `_avisos`, nunca interrompe.
- **`ferramentas/relatorio.py` — relatório de ciclo e de fase.** `de_ciclo` (Markdown:
  objetivo, fases percorridas, decisões, contagem de ações por nível, arquivos
  tocados, pendências) e `de_fase` (ações rastreadas daquela fase, diffs pendentes,
  pendências). Sem trilha, o relatório diz isso — nunca inventa.
- **`hooks/engine_salvar.py` (PreCompact).** Consolida no estado, antes da
  compactação, `ultima_consolidacao` (ISO) e `resumo_trilha` (contagem por nível de
  risco). Nunca bloqueia a compactação: qualquer erro sai 0 sem gravar nada.
- **`hooks/engine_gate.py` (Stop).** Cobra evidência UMA vez por fase quando a fase
  atual é BUILD, TESTE ou REVISAO e a trilha da fase não tem nenhuma ação
  registrada. O contador `cobrancas_por_fase`, gravado no estado ANTES de cobrar, é
  o que impede o laço infinito — não `stop_hook_active`, que só descreve o turno
  corrente. Nunca bloqueia por erro interno: falha segura aqui é NÃO travar a saída.
- **CLI: `retomar`, `--dry`, `relatorio`.** `ligar --dry` cria o ciclo com
  `modo="dry"` (o hook de risco já bloqueia toda escrita nesse modo, mesmo a que
  sairia LIVRE). `retomar` relê estado + trilha e imprime um resumo de reentrada
  (fase, objetivo, decisões, últimas 5 ações, pendências) para sessão nova; estado
  corrompido sai 1 com mensagem legível, sem tocar no arquivo. `relatorio
  [ciclo|fase X]` chama `ferramentas/relatorio.py`.
- **Os 5 papéis restantes:** `descobridor` (DESCOBERTA, sem escrita), `cartografo`
  (ANALISE, sem escrita), `designer` (PLANO, escreve só a direção visual, consome o
  cartão `ui-ux`), `testador` (TESTE, escreve e roda teste, nunca ajusta teste para
  o código passar), `sentinela` (REVISAO, segurança + performance, sem Bash nem
  escrita). Elenco completo: 9 agentes.
- **Os 9 cartões restantes:** `fastapi`, `excel-vba`, `office-scripts`,
  `power-query`, `react`, `typescript`, `postgresql`, `sqlite`, `mermaid`. Elenco
  completo: 12 cartões, todos lidos sem erro por `detectar.ler_cartao`.
- **Verificação em `aceite/fase-2.md`:** suíte completa (247 testes), 9 famílias
  travadas pelo hook de verdade (`aceite/verificar_familias.py`, R9 incorporada na
  correção final da Fase 1), e o roteiro NOVO de 20 turnos com compactação simulada
  (`aceite/simular_turnos.py`) — todos com saída literal colada.

### Não verificado nesta fase

- A instalação real do plugin numa sessão do Claude Code (reconhecimento de
  `hooks/hooks.json`, resolução de `${CLAUDE_PLUGIN_ROOT}`, disparo dos cinco hooks
  nos eventos certos).
- A prova de que o Claude Code de fato injeta o stdout do `UserPromptSubmit` no
  contexto de uma conversa real.
- O comportamento do `Stop` (`engine_gate.py`) bloqueando de verdade numa sessão
  real, com a mensagem de cobrança chegando legível ao modelo.
- Os quatro cenários de aceite com projetos-cobaia (Fase 3).
- **`hooks/hooks.json` usa o lançador `py`, que só existe no Windows** (e não em
  toda instalação Windows). Os testes e os três scripts de aceite usam
  `sys.executable` de propósito, mas o arquivo que o Claude Code de fato lê para
  invocar cada hook continua com `py` — uma instalação fora do Windows quebraria os
  cinco hooks por esse motivo. Risco de portabilidade conhecido, não corrigido
  nesta fase.

Detalhe completo, com saída literal de cada verificação, em `aceite/fase-2.md`.

## 2026-07-30 — Correções da revisão final da Fase 1

Sete achados fechados; 183 testes verdes (eram 152) e `aceite/verificar_familias.py`
segue sem falhas.

- **R9, família nova — o painel de controle do motor.** Qualquer escrita sob um
  diretório `.engine/` é **travada**, por `Write`/`Edit`/`NotebookEdit` e por
  redirecionamento de shell. Antes, `Edit` em `.engine/estado.json` saía `rastreado`
  (executava: `"ativo": false` desligava os dois hooks) e `Write` em
  `.engine/config.json` saía `livre`, em silêncio (`{"padroes_segredo": []}` desarmava
  a família R5 inteira). **Leitura de `.engine/` continua `livre`.**
- **`config.py` absorve por lista branca.** `cfg.update(dados)` aceitava qualquer chave
  do arquivo do hospedeiro, inclusive `_avisos`. Agora só chave presente em `PADRAO`
  pode ser sobreposta, chave desconhecida é ignorada com aviso, e `padroes_segredo` do
  arquivo é **acrescentado** ao default: ampliar a lista de segredos é legítimo,
  reduzi-la deixou de ser possível.
- **R5 passa a casar CONTEÚDO, não só caminho.** A seção 5 da spec sempre prometeu isso;
  o código só olhava o nome do arquivo, e `Write` com `AKIA…` no corpo saía `livre`.
  Padrões cobertos: `sk-`, `ghp_`, `github_pat_`, `AKIA`, `xox[baprs]-`, cabeçalho de
  chave privada PEM e JWT.
- **Sobrescrever teste que já existe é `rastreado`.** Era `livre`, o que fazia da
  violação do invariante "nunca ajustar o teste para o código passar" a única escrita
  invisível no relatório da fase. Criar teste novo continua `livre`.
- **A CLI roda como script, de qualquer diretório:**
  `ENGINE_RAIZ="$(pwd)" py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" status`. A skill
  documentava `python -m ferramentas.cli`, que da raiz de um projeto hospedeiro dá
  `ModuleNotFoundError`. As duas formas funcionam agora.
- **`desligar` não suja projeto alheio.** Sem estado em disco, imprime a linha limpa e
  sai 0 **sem gravar nada** — antes criava `.engine/estado.json` com `{"ativo": false}`
  e o `status` daquele projeto virava verboso para sempre.
- **`README.md` corrigido:** dizia que `agents/`, `cartoes/` e `aceite/` faltavam; os
  três existem e estão commitados desde `eb302cc`/`e93630e`.

## 2026-07-30 — Fase 1 (núcleo)

- `config`, `risco`, `estado`, `cli` em Python de biblioteca padrão.
- Hooks `PreToolUse` (classificação de risco com falha segura) e `UserPromptSubmit`
  (cartão de estado com teto de linhas).
- Skill `/engine` com `ligar`, `desligar`, `status`.
- Papéis: arquiteto, implementador, revisor, documentador.
- Cartões: python, pytest, ui-ux.
- Verificação em `aceite/fase-1.md` (152 testes, verificação de aceite das sete
  famílias travadas pelo hook de verdade via `aceite/verificar_familias.py`, e o
  teste do teto do cartão de estado — todos com saída literal colada).

### A política do classificador de risco foi invertida durante a execução

`ferramentas/risco.py` não terminou a Fase 1 com a política com que começou. A versão
inicial tentava decidir se um comando de shell podia sair **livre** por prova
positiva — primeiro uma lista de comandos proibidos, depois uma lista de comandos
**permitidos**, depois essa mesma lista qualificada pela forma do argumento (nome do
comando **mais** as flags aceitas).

Sete rodadas de revisão adversarial atacaram essa lista e, em todas as sete, acharam
um caminho novo para `livre` liberando uma ação destrutiva. Os dois casos que
forçaram a virada de chave: `git diff --output=/home/user/.bashrc` (sobrescreve um
arquivo arbitrário escondido atrás do nome de um comando de leitura) e o apelido
`where` do PowerShell (que na verdade é `Where-Object`, e roda .NET arbitrário dentro
de um bloco de script). A causa não era uma flag esquecida em cada rodada — é
estrutural: **cada comando permitido é, ele próprio, uma linguagem**, com flags,
apelidos e formas de argumento que nenhuma lista fechada enumera até o fim. Enquanto
a categoria "comando liberável por prova positiva" existisse, a próxima rodada de
revisão sempre achava a próxima brecha.

A política final elimina a categoria inteira em vez de tentar fechá-la brecha por
brecha: **comando de shell nunca sai `livre`**. Ou ele casa uma das famílias fechadas
R1–R8 (rede, git destrutivo, deleção, banco, segredo, cano para interpretador,
substituição de comando, deploy/infraestrutura, instalação global) e vira
**travado**, ou vira **rastreado** — executa, e aparece no relatório de fim de fase.
Isso inclui fechar até o emissor inerte (`echo`/`printf`), que era a última válvula
capaz de liberar um segmento só por reconhecer o prefixo do comando. Só ferramenta de
**arquivo** continua podendo sair `livre` (leitura que não é segredo, escrita em
arquivo novo ou sob `tests/`).

O custo aceito, de propósito: o relatório de fim de fase fica mais longo — todo
comando de shell aparece nele, do `pytest -q` trivial ao comando perigoso. É uma
troca deliberada, registrada em `ferramentas/risco.py` e em
`docs/specs/2026-07-30-engine-design.md`: `rastreado` custa uma linha de relatório;
`livre` errado custa um estrago irreversível. `ferramentas/tests/test_risco.py::
test_nenhum_comando_de_shell_e_livre` é a trava dessa decisão — percorre comandos
cotidianos inofensivos e falha se qualquer um voltar a sair `livre`; reintroduzir uma
lista de permitidos é uma mudança de política que tem de custar esse teste vermelho
de propósito.

Essa mudança de política é também por que os números deste changelog e de
`aceite/fase-1.md` não batem com os do brief original da Tarefa 10
(`.superpowers/sdd/briefs/tarefa-10-brief.md`, escrito antes da virada): a suíte
cresceu de 68 para 152 testes cobrindo as famílias e os casos-limite achados nas
rodadas de revisão, e o script de verificação de aceite não usa mais nenhum caso de
"comando de shell liberado" como contraprova — a única superfície ainda `livre` por
natureza é leitura de arquivo comum. Detalhe completo em
`.superpowers/sdd/briefs/tarefa-10-report.md`.

**Não verificado nesta fase:** sobrevivência a 20 turnos reais e a uma compactação; os
quatro cenários de aceite com projetos-cobaia. Ambos são Fase 3.
