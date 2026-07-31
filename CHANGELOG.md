# Changelog - AI Engineering Motor (ENGINE)

**Version**: 4.0.0  
**Status**: ✅ Production Ready

---

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
