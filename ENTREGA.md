# ENTREGA — ENGINE + 10 volumes essenciais

## Status real (atualizado 2026-08-03, após auditoria externa)

**O motor está pronto. O acervo de conhecimento não está — e esta entrega redefine o escopo
para refletir isso, em vez de declarar os 42 volumes como entregues.**

Uma auditoria externa (Codex) encontrou que a entrega anterior deste arquivo ("PRONTO PARA
AUDITORIA", "Estrutura Completa") estava incorreta: os 39 volumes marcados RASCUNHO eram
esqueletos gerados em lote, com seções de ~20 palavras, a maioria sem front-matter, muito abaixo
do mínimo de substância que o próprio contrato exige. A auditoria também encontrou um bug real:
os `_VOLUME.yml` desses 39 volumes tinham um BOM UTF-8 no início do arquivo, o que fazia o
validador reportar "campo `volume` ausente" mesmo com o campo presente — mascarando o tamanho
real do problema. Corrigido o BOM, o gate estrutural passou de 39 para **657 violações reais**.

### Decisão de escopo, tomada com o autor em 2026-08-03

Em vez de tentar completar 42 volumes de conhecimento genérico, o escopo desta entrega passa a
ser: **o motor (produto principal, já pronto) + 10 volumes essenciais de conhecimento**, com o
restante do acervo declarado explicitamente como biblioteca evolutiva em RASCUNHO — sem
promessa de conclusão nesta entrega.

## O motor — pronto e testado

- `ferramentas/` (configuração, classificador de risco, máquina de fases, detecção de stack,
  trilha, relatório, CLI), os 5 hooks, a skill, os 9 papéis, os 12 cartões, o empacotamento
  como plugin.
- **449 testes** verdes (`python -m pytest ferramentas/tests`).
- Observado em sessão real do Claude Code em 2026-07-31 (ver `README.md`, seção Estado).

## Os 10 volumes essenciais

| # | Volume | Tipo | Status |
|---|---|---|---|
| 01 | FUNDACAO | GOVERNANCA | a escrever |
| 03 | DISCOVERY | PROCESSO | ✅ PRONTO (auditoria 8,9) |
| 07 | PROMPT-ENGINE | ENGINE | ✅ PRONTO — padrão-ouro |
| 08 | AGENT-ENGINE | ENGINE | a escrever |
| 09 | ORCHESTRATOR | ENGINE | a escrever |
| 10 | WORKFLOW | ENGINE | a escrever |
| 12 | MEMORY | ENGINE | ✅ PRONTO (auditoria 8,7) |
| 17 | SECURITY | GOVERNANCA | a escrever |
| 21 | OBSERVABILITY | GOVERNANCA | a escrever |
| 31 | TESTING | PROCESSO | a escrever |

3 já estão PRONTO. Os 7 restantes seguem o mesmo processo do `03-DISCOVERY`: front-matter
completo, prosa real específica ao tema, diagramas Mermaid exigidos pelo tipo com descrição,
sem marcador de trabalho inacabado, gate estrutural (`ferramentas.validar`) verde antes de
qualquer promoção — e só passam a `PRONTO` de fato depois da auditoria por outro modelo com
média ≥ 8,0, conforme a Definição de PRONTO em `acervo/00-INTRODUCAO/Convencoes.md`.

## O que fica fora deste ciclo, declarado — não escondido

Os outros **32 volumes** (02, 04, 05, 06, 11, 13-16, 18-20, 22-30, 32-42) permanecem
`RASCUNHO`, registrados no contrato, sem conteúdo substantivo ainda. Não são apagados nem
prometidos — ficam como biblioteca evolutiva, cada um a ser reescrito quando houver material
real para extrair e generalizar, na mesma ordem de critério que `acervo/ROADMAP.md` já
documentava antes desta auditoria (prioridade para volume com código real para extrair, não
ordem numérica).

## Lição registrada

"449 testes passando" nunca foi prova de que o conteúdo dos volumes estava completo — só provava
que o motor (o código) funciona. Confundir os dois é exatamente o erro que a entrega anterior
cometeu ao declarar "PRONTO PARA AUDITORIA" com 39 volumes vazios por dentro.

---
Auditoria externa: Codex, 2026-08-03 | Decisão de escopo: autor, 2026-08-03
