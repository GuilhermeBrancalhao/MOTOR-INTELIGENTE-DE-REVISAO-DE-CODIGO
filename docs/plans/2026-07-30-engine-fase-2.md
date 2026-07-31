# ENGINE — Plano de Implementação da Fase 2 (elenco)

> **Para trabalhadores agênticos:** use `superpowers:subagent-driven-development`.
> Método idêntico ao da Fase 1: TDD, revisão adversarial por tarefa, ledger em
> `.superpowers/sdd/progress.md`.

**Objetivo:** completar o elenco do motor — os 5 papéis restantes, os 9 cartões restantes,
a trilha auditável, o relatório de ciclo, os 3 hooks restantes e `/engine retomar` + `--dry`.

**Base:** Fase 1 mesclada em `master` (183 testes verdes). Trabalhar na branch `feat/fase-2`.

## Restrições globais (idênticas à Fase 1)

- Apenas biblioteca padrão do Python 3.11+; `pytest` só para desenvolvimento.
- Prosa e comentários em português do Brasil; I/O com `encoding="utf-8"`; datas ISO.
- **Comando de shell nunca é `livre`** — política selada, protegida por teste.
- Falha segura do hook de risco = travado; falha do hook de contexto = não injetar e sair 0.
- Escrita em `.engine/` é travada (R9) — a trilha e o estado são gravados PELOS hooks
  (processo do próprio motor), nunca por ação classificada.
- Nunca ajustar o teste para o código passar. Nada fora de `C:\Users\Usuário\Desktop\ENGINE\`.

## Tarefas

### F2-T1: `ferramentas/detectar.py` — detecção de stack
Lê o front-matter `detectar:` de cada cartão em `cartoes/` (parser de subconjunto YAML
restrito: `tecnologia:`, `detectar: [...]`, `papeis: [...]`, `versao:`), varre o projeto
hospedeiro com `pathlib` + `fnmatch` (profundidade máx. 6, ignora `.git`, `node_modules`,
`__pycache__`, `.engine`) e devolve a lista de tecnologias presentes.
- Produz: `detectar.cartoes_do_projeto(raiz_projeto: Path, raiz_plugin: Path) -> list[str]`
  (ordenada, sem duplicata) e `detectar.ler_cartao(caminho: Path) -> dict` (chaves
  `tecnologia`, `detectar`, `papeis`, `versao`; levanta `CartaoInvalido` em front-matter
  malformado).
- Testes: projeto com `pyproject.toml` detecta `python` e `pytest`; projeto vazio devolve
  `[]`; cartão sem front-matter levanta `CartaoInvalido`; glob com subdiretório
  (`tests/**/test_*.py`) casa; diretórios ignorados não são varridos.
- Ao ligar um ciclo, a CLI grava o resultado em `estado.cartoes` (integração em F2-T5).

### F2-T2: `ferramentas/trilha.py` + hook `engine_trilha.py` (PostToolUse)
Trilha append-only em `<projeto>/.engine/trilha.jsonl`, uma linha por ação:
`{"quando", "fase", "ferramenta", "alvo", "risco", "regra"}` (valores sintéticos nos testes).
- Produz: `trilha.registrar(raiz, entrada: dict)`, `trilha.ler(raiz) -> dict` (chaves
  `linhas: list[dict]` e `_avisos: list[str]`), `trilha.caminho(raiz)`. Erro de escrita
  nunca propaga para o hook (registrar é acessório).
- Hook `hooks/engine_trilha.py`: lê o evento PostToolUse (confirmar contrato na doc via
  `claude-code-guide` ANTES de implementar: chaves e se stdout/exit importam), reclassifica
  a ação com `risco.classificar` para obter nível/regra, e faz append. Motor desligado: sai
  0 sem gravar. Qualquer erro: sai 0 (nunca atrapalha o turno).
- Registrar em `hooks/hooks.json`.
- Testes: ação com motor ligado gera linha com os 6 campos; desligado não gera; JSONL
  malformado pré-existente não impede append; `ler` pula linha corrompida e reporta em
  `_avisos`.

### F2-T3: `ferramentas/relatorio.py` — relatório de ciclo e de fase
- Produz: `relatorio.de_fase(raiz, fase: str) -> str` (Markdown: ações rastreadas da fase,
  diffs pendentes, pendências) e `relatorio.de_ciclo(raiz) -> str` (Markdown: objetivo,
  fases percorridas, decisões com justificativa, contagem de ações por nível, arquivos
  tocados, pendências abertas).
- Consome `estado.carregar` + `trilha.ler`. Sem trilha → o relatório diz isso, não inventa.
- A CLI ganha o verbo `relatorio [fase|ciclo]` (F2-T5).
- Testes: relatório de ciclo com trilha sintética contém objetivo, decisões e contagens
  corretas; sem trilha, contém a frase de ausência; nunca levanta exceção com estado parcial.

### F2-T4: hooks `engine_salvar.py` (PreCompact) + `engine_gate.py` (Stop)
- **Confirmar contrato dos dois eventos na doc ANTES de implementar** (via
  `claude-code-guide`): o que chega no stdin, o que o exit code faz em cada um, e se Stop
  suporta bloquear com mensagem.
- `engine_salvar`: consolida no estado um resumo do ciclo (`ultima_consolidacao` ISO +
  contagens da trilha) antes da compactação. Erro: sai 0.
- `engine_gate`: se a fase atual exigir evidência (BUILD/TESTE/REVISAO) e a trilha da fase
  não tiver nenhuma ação registrada, cobra UMA vez por fase (mensagem pedindo evidência),
  usando `cobrancas_por_fase` no estado como contador. Segunda vez na mesma fase: sai 0
  sem cobrar. **O contador é o que impede laço infinito — teste obrigatório.**
- Registrar ambos em `hooks/hooks.json`.
- Testes: salvar grava `ultima_consolidacao`; gate cobra na 1ª e NÃO cobra na 2ª (contador
  persistido); gate não cobra em DESCOBERTA/PLANO; erro em qualquer um sai 0.

### F2-T5: CLI — `retomar`, `--dry`, `relatorio`, integração de cartões
- `ligar` ganha `--dry` (cria ciclo com `modo="dry"`; o hook de risco já bloqueia escrita
  nesse modo) e passa a chamar `detectar.cartoes_do_projeto`, gravando em `estado.cartoes`.
- Verbo novo `retomar`: relê `.engine/estado.json` + trilha e imprime um resumo de
  reentrada (fase, objetivo, decisões, últimas 5 ações, pendências) para sessão nova.
  Estado corrompido: mensagem legível, saída 1, sem tocar no arquivo.
- Verbo novo `relatorio [ciclo|fase X]` chamando `ferramentas/relatorio.py`.
- Atualizar `skills/engine/SKILL.md`: documentar `retomar`, `--dry` e `relatorio` com a
  forma de invocação que funciona (`py "${CLAUDE_PLUGIN_ROOT}/ferramentas/cli.py" ...`).
- Testes: `ligar --dry` grava `modo="dry"`; `retomar` sem estado sai 1 com mensagem;
  `retomar` com estado imprime fase e objetivo; `relatorio ciclo` imprime o Markdown.

### F2-T6: os 5 papéis restantes
`agents/descobridor.md`, `cartografo.md`, `designer.md`, `testador.md`, `sentinela.md` —
mesmo formato da Fase 1 (front-matter `name`/`description`/`tools` + missão, entradas,
saídas, limitações, critério de pronto), seguindo a tabela da seção 6 do spec:
- `descobridor` (DESCOBERTA): objetivo real, requisitos, riscos. Sem escrita. Tools: Read, Grep, Glob.
- `cartografo` (ANALISE): mapa do projeto, dependências, duplicação, cartões a carregar. Sem escrita. Tools: Read, Grep, Glob.
- `designer` (PLANO, com o arquiteto): direção visual, opções comparáveis; consome o cartão `ui-ux` e o MCP open-design quando disponível. Escreve só a direção. Tools: Read, Grep, Glob, Write.
- `testador` (TESTE): escreve e roda teste; nunca ajusta teste para código passar. Tools: Read, Grep, Glob, Write, Edit, Bash.
- `sentinela` (REVISAO): segurança + performance; invoca `ecc:security-reviewer`/`ecc:performance-optimizer` quando instalados e consolida o resultado no relatório do motor. **Sem Bash nem escrita** (mesma lição estrutural do revisor). Tools: Read, Grep, Glob.
- Atualizar `skills/engine/SKILL.md` (tabela de papéis por fase) e `cartoes/_catalogo.md`.
- Verificação: front-matter válido nos 9 agentes; nomes batem com o SKILL.md.

### F2-T7: os 9 cartões restantes
`fastapi`, `excel-vba`, `office-scripts`, `power-query`, `react`, `typescript`,
`postgresql`, `sqlite`, `mermaid` — mesmo formato da Fase 1 (front-matter `tecnologia`/
`detectar` [globs válidos!]/`papeis`/`versao` + Convenções, Armadilhas, Comandos, Checklist).
Conteúdo técnico VERIFICÁVEL; na dúvida, omitir (nunca inventar armadilha). Atualizar
`cartoes/_catalogo.md`. Verificação: `detectar.ler_cartao` aceita os 12 cartões sem erro
(teste de F2-T1 estendido aqui).

### F2-T8: aceite da Fase 2
`aceite/fase-2.md` com saídas literais: suíte completa; `verificar_familias.py` (continua
verde); um roteiro NOVO `aceite/simular_turnos.py` que simula 20 turnos chamando os hooks
reais em sequência (contexto → risco → trilha) num projeto sintético, com uma consolidação
(`engine_salvar`) no meio, e verifica que o estado e a trilha sobrevivem e o cartão sai
correto no turno 20 — **isso fecha, na mecânica, o critério "sobrevive a 20 turnos e a uma
compactação" que a Fase 1 declarou não verificado** (a prova no Claude Code real continua
sendo a instalação, Fase 3). Atualizar `CHANGELOG.md`. Registrar o que segue não verificado.

## Ordem e dependências
T1 → T5 (cartões no estado). T2 → T3, T4, T8. T3 → T5. Tudo → T8.
Sequência: T1, T2, T3, T4, T5, T6, T7, T8.
