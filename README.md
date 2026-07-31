# ENGINE

Motor de engenharia para o Claude Code. Liga com `/engine`, desliga com `/engine off`.

O que o distingue de um prompt longo: o modo vive em `.engine/estado.json` no projeto, é
re-injetado a cada turno por um hook, e sobrevive à compactação do contexto. E cada ação
passa por um classificador de risco antes de acontecer — o que é barato desfazer acontece
sozinho; o que é irreversível para e pergunta.

- Especificação: `docs/specs/2026-07-30-engine-design.md`
- Plano da Fase 1: `docs/plans/2026-07-30-engine-fase-1.md`

## Testes

```bash
python -m pytest ferramentas/tests -v
```

## Estado atual

**Fase 1 (núcleo) completa.** Estão no repositório e cobertos por testes:

- `ferramentas/` — configuração (`config.py`), classificador de risco (`risco.py`),
  máquina de fases e estado em disco (`estado.py`) e a CLI da skill (`cli.py`);
- `hooks/` — os dois hooks (`PreToolUse` de risco e `UserPromptSubmit` de contexto) e o
  `hooks.json` que os registra;
- `skills/engine/` — a skill `/engine`, com `on`/`off`/`status`;
- `agents/` — os quatro papéis por fase: `arquiteto`, `implementador`, `revisor`,
  `documentador`;
- `cartoes/` — os cartões de stack (`python`, `pytest`, `ui-ux`) e o `_catalogo.md`;
- `aceite/` — o aceite formal da fase (`fase-1.md`) e o script `verificar_familias.py`,
  que dispara o hook de verdade como subprocesso e confirma que as famílias travadas
  travam;
- empacotamento como plugin instalável.

Ficou para a **Fase 2 (elenco)**, segundo a seção 15 da especificação: os outros cinco
papéis (`descobridor`, `cartografo`, `designer`, `testador`, `sentinela`), os nove cartões
restantes, `trilha.py` e `relatorio.py`, os hooks `trilha`, `salvar` e `gate`, e
`/engine retomar`. E para a **Fase 3 (prova)**: o modo `--dry` na skill, os quatro
cenários de aceite, os cartões de Office completos e a documentação de instalação do
plugin.
