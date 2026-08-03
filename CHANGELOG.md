# Changelog - AI Engineering Motor (ENGINE)

**Version**: 4.0.0  
**Status**: ✅ Production Ready

---

## 2026-08-03 — Unificação: a plataforma de acervo entra no motor

O motor e a plataforma que produz os volumes de conhecimento eram dois repositórios, e o motor
carregava uma **cópia manual** dos volumes em `volumes/prontos/`. A cópia derivou, e a medição
foi o que motivou a unificação:

| Sintoma | O que estava acontecendo |
|---|---|
| `31-TESTING` | na cópia com `status: PRONTO`; na fonte, `RASCUNHO` — o cartão de contexto carregava rascunho como conhecimento pronto |
| `03-DISCOVERY` | `PRONTO` na fonte, **nunca** chegou na cópia |
| `07-PROMPT-ENGINE` | 5 arquivos com conteúdo diferente da fonte |
| `12-MEMORY` | 3 arquivos com conteúdo diferente da fonte |

**O que mudou**

- `acervo/` — a plataforma inteira (302 arquivos), importada com o histórico preservado a
  partir do seu repositório público (`bf95c57`). Ela continua sendo a dona dos volumes.
- `ferramentas/sincronizar.py` — gera `volumes/prontos/` a partir de `acervo/`, incluindo
  apenas o que a fonte declara `PRONTO`. `--verificar` só compara e devolve 1 se divergiu.
- `ferramentas/tests/test_sincronizar.py` — a porta. `test_a_copia_do_plugin_esta_em_dia` roda
  contra o repositório real; editar um byte de `volumes/prontos/` deixa a suíte vermelha
  (provado por mutação). As outras reproduzem de propósito cada forma de deriva já observada.
- `volumes/_catalogo.md` passou a ser gerado, para não virar o próximo arquivo mantido à mão.
- `pytest.ini` — a raiz coleta só a suíte do motor. Os dois pacotes `ferramentas` (o do motor e
  o do acervo) colidem numa sessão única de pytest; o acervo roda de dentro de `acervo/`.

**Correção que apareceu no caminho:** `shutil.which("bash")` devolvia, no Windows sem WSL, o
stub da Microsoft Store — que responde a `which` mas imprime "instale uma distro" em UTF-16 e
sai 1 sem ler o script. Os 17 testes de `test_lancador.py` falhavam por isso, e não por defeito
do lançador. `hooks/engine.sh` já descartava esse stub para o Python; a mesma regra faltava no
teste.

**Suítes:** 449 (motor) + 455 (acervo) = 904 testes verdes.

**O que a unificação NÃO fez:** não renomeou o repositório, não reapontou o plugin e não mexeu
no manifesto — o acervo entrou dentro do motor, e não o contrário.

---

## 2026-07-31 — Primeira execução em sessão real do Claude Code

O plugin foi instalado e rodou dentro de uma sessão real do Claude Code — o item "instalação
real do plugin" deixado explicitamente não verificado pela Fase 2 está fechado. Três coisas
foram **observadas**, não simuladas:

- O hook `UserPromptSubmit` injetou o cartão `== ENGINE ativo ==` no contexto do turno.
- O hook `PreToolUse` travou um `git push` pela família R2 — inclusive o push do próprio
  código-fonte deste projeto.
- O mesmo hook travou um `python -c` pela família R8. Era um falso positivo, corrigido
  depois: a string `'EXEC(ruim)'` casava `\bexec\(` porque o padrão era compilado sem
  distinguir maiúsculas.

Isso prova que o **mecanismo** funciona numa sessão real, e nada além disso. O que continua
sem prova é a **durabilidade**: o motor nunca atravessou uma sessão longa com compactação de
verdade (`aceite/simular_turnos.py` simula vinte turnos e uma compactação chamando os hooks
reais, mas simulação não é sessão), e o lançador nunca rodou numa máquina macOS ou Linux
real.

Junto com a instalação, a skill foi corrigida no mesmo espírito dos hooks:
`skills/engine/SKILL.md` mandava invocar a CLI com `py` direto — o Python Launcher, que só
existe no Windows — enquanto os cinco hooks já passavam pelo lançador. Todas as invocações
da skill agora passam por `hooks/engine.sh` (sem `--travar-sem-python`: essa flag é
exclusiva do `PreToolUse`; para a CLI, sair 0 em silêncio quando não há Python é o certo).

## 2026-07-31 — Auditoria adversarial: três famílias novas (R10–R12) e a guerra aos falsos positivos

Quatro revisores adversariais rodaram em paralelo, cada um sobre uma superfície: o
lançador (`hooks/engine.sh`), o classificador (`ferramentas/risco.py`), os hooks e os
módulos de dados (`estado.py`, `trilha.py`, `config.py`). Suíte: **280 → 388 testes
verdes**; `aceite/verificar_familias.py` ganhou os casos de R10, R11 e R12 e a seção 5
da especificação foi atualizada.

Os achados que mais importaram, com o vetor concreto de cada um:

- **A caixa do nome derrotava a família do painel de controle.** `Write` em
  `.ENGINE/estado.json` saía `livre` — o filesystem do Windows não distingue
  maiúsculas, então era o mesmo arquivo real, e gravar `{"ativo": false}` nele
  desligava o motor inteiro sem travar nem aparecer no relatório. `_sob_painel`
  passou a comparar componente por componente ignorando a caixa (`.engineering`
  segue de fora).
- **Escrita de arquivo novo em qualquer ponto do disco era livre.** A política
  "arquivo novo é livre" não olhava PARA ONDE: `Write .git/hooks/pre-commit` ou
  `.claude/settings.json` instalava execução persistente — código arbitrário rodando
  a cada commit ou a cada sessão — como um inocente arquivo novo. Nasce a família
  **R10** (hooks de git, `.claude/`/`.vscode/`/`.idea/`, init de shell, perfil do
  PowerShell, `Startup`, `crontab`, `.gitconfig`, `authorized_keys`), que trava
  dentro ou fora da raiz; e arquivo novo fora da raiz do projeto deixou de ser livre.
- **ReDoS quadrática travava a sessão.** Os quantificadores ilimitados das famílias
  (`[^\n]*`) retrocediam sobre comando repetitivo: um comando de 6.400 repetições
  (32 mil caracteres) prendia o classificador por 7,7 s na medição da auditoria
  (5,7 s reproduzidos nesta máquina) — e o `PreToolUse` roda a cada ação. Todo
  quantificador virou janela limitada (`{0,200}`) e nasceu a família **R12**: comando
  acima do teto de 20.000 caracteres **trava** sem ser analisado, porque travar é o
  lado certo do erro — o humano confirma um comando anômalo em vez de a sessão
  congelar tentando entendê-lo. Junto entrou a família **R11** (destruição sem verbo
  de apagar: `truncate -s`, `dd of=`, `robocopy /MIR`, `format`, `wsl --unregister`,
  `reg delete /f`, truncamento por `>` puro), que a família de deleção nunca via.
- **O cartão de estado imprimia segredo cru no contexto a cada turno.** A trilha já
  redigia credencial (`trilha.redigir`), mas o cartão — que volta ao contexto do
  modelo TODO turno — imprimia o objetivo e as decisões sem redação nenhuma. Agora
  todo texto vindo do estado passa pela MESMA redação da trilha (por referência, não
  por cópia: duas listas de padrões divergem na primeira vez que uma ganha um padrão
  novo), e redige ANTES de cortar — token truncado ainda é reconhecível.
- **`novo_ciclo` sobrescrevia estado corrompido em silêncio.** Um `estado.json`
  ilegível era tratado como inexistente e o ciclo novo gravava por cima, destruindo a
  evidência. Agora o arquivo corrompido é preservado com renomeação
  (`estado.corrompido-<carimbo>.json`) antes de qualquer escrita.

**A mesma quantidade de trabalho foi para o outro lado do erro: os falsos positivos.**
`pip install -r requirements.txt` travava como instalação global, `pytest -k token`
travava como acesso a segredo (o argumento `token` casava `*token*`), `grep 'DELETE
FROM' log.txt` travava como SQL destrutivo — os três hoje saem `rastreado`. Isso não é
conforto, é defeito de segurança: falso positivo frequente treina o humano a aprovar no
automático, e aprovação no automático anula o gate inteiro. Cada afrouxamento é
estreito e comentado no código com o caso que o motivou (lookahead para `-r`/`-e`/`.`,
primeiro token de ferramenta de busca, identificador sensível a caixa em `_PY_PERIGO`).

**Um bug foi introduzido durante a correção — e pego pela própria suíte.** O filtro do
stub da Microsoft Store no lançador (o `python` falso de `WindowsApps`) precisava
comparar sem distinguir caixa, e a primeira versão fazia isso com o binário externo
`tr`. Com PATH restrito — exatamente o cenário que o lançador existe para aguentar — o
`tr` some, a substituição falhava em silêncio e o filtro parava de filtrar. Corrigido
com classe de caracteres em glob POSIX puro, sem depender de binário nenhum; o teste de
PATH controlado é o que denunciou.

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

---

## [4.0.0] - 2026-07-31

### ✨ Adicionado
- **Volumes Dinâmicos**: Auto-discovery sem hardcoding
- **Detector de Volumes**: Cache inteligente (TTL 300s)
- **Hook V4**: Integração com detecção dinâmica
- **18 Testes**: 8 unitários + 6 integração + 4 E2E

### 🔧 Melhorado
- Performance com cache
- Validação de estrutura
- Ordem alfabética de volumes

### 📚 Documentação
- PLUGIN-README.md
- CHANGELOG.md

### 🎯 Status
- **Testes**: 18/18 PASSARAM ✅
- **Produção**: V4 ativado

---

## [3.0.0] - 2026-07-31

### ✨ Adicionado
- **Sugestão Automática**: Análise de diff
- **AnalisadorDiff**: 5 padrões detectáveis
- **Hook V3**: Com integração
- **17 Testes**: 8 unitários + 5 integração + 4 E2E

### 🎯 Status
- **Motores**: 5/5 detectados
- **Produção**: V3 ativado

---

## [2.0.0] - 2026-07-31

### ✨ Adicionado
- **Hook V2**: Motores + volumes
- **Teto de 50 linhas**: Respeitado

### 🎯 Status
- **Produção**: V2 ativado

---

## [1.0.0] - 2026-07-31

### ✨ Adicionado
- **5 Motores**: Base completa
- **8 Fases ENGINE**: Framework completo
- **9 Agentes**: Mapeados

### 🎯 Status
- **Arquitetura**: Base de 42 volumes
- **Testes**: 9/9 PASSARAM ✅

---

**Made with ❤️ for Claude Code**
