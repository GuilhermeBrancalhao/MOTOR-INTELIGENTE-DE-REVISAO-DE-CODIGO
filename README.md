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

Fase 1 (núcleo) em andamento. Prontos: configuração, classificador de risco, máquina de
fases e estado em disco, os dois hooks (`PreToolUse` e `UserPromptSubmit`), a skill
`/engine`, e este empacotamento como plugin instalável. Faltam, ainda dentro da Fase 1: os
quatro papéis por fase (`agents/`), os cartões de stack (`cartoes/`) e o aceite formal
(`aceite/`). Fases 2 e 3 descritas na seção 15 da especificação.
