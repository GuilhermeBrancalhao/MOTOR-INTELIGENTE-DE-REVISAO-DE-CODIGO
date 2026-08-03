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

| # | Volume | Tipo | Gate 1 | Testes do exemplo | Auditoria | Status |
|---|---|---|---|---|---|---|
| 01 | FUNDACAO | GOVERNANCA | ✅ | 8 ✅ | 8,4 | ✅ **PRONTO** |
| 03 | DISCOVERY | PROCESSO | ✅ | 69 ✅ | 8,8 | ✅ **PRONTO** |
| 07 | PROMPT-ENGINE | ENGINE | ✅ | ✅ | 8,7 | ✅ **PRONTO** |
| 08 | AGENT-ENGINE | ENGINE | ✅ | 14 ✅ | 8,2 | ✅ **PRONTO** |
| 09 | ORCHESTRATOR | ENGINE | ✅ | 10 ✅ | 8,2 | ✅ **PRONTO** |
| 10 | WORKFLOW | ENGINE | ✅ | 8 ✅ | 8,3 | ✅ **PRONTO** |
| 12 | MEMORY | ENGINE | ✅ | ✅ | 8,7 | ✅ **PRONTO** |
| 17 | SECURITY | GOVERNANCA | ✅ | 21 ✅ | 8,5 | ✅ **PRONTO** |
| 21 | OBSERVABILITY | GOVERNANCA | ✅ | 8 ✅ | 8,3 | ✅ **PRONTO** |
| 31 | TESTING | PROCESSO | ✅ | 7 ✅ | 8,3 | ✅ **PRONTO** |

**Os 10 volumes essenciais estão `PRONTO`** — os quatro critérios da Definição de PRONTO
satisfeitos em cada um: gate estrutural verde, testes dos exemplos passando, auditoria com média
≥ 8,0 registrada em `acervo/auditorias/`, e registro datado no `CHANGELOG.md`. Isso cumpre
exatamente o alvo declarado do ciclo: motor + 10 essenciais, não 42.

Os sete promovidos hoje ganharam `exemplos/<vol>/` com módulo e suíte própria — 76 testes,
escritos para a mutação que cada invariante existe para impedir, não para o caminho feliz. Os
relatórios de auditoria trazem as notas por seção, os defeitos encontrados e corrigidos, e a
verificação de cada afirmação factual contra o código do motor.

**A lacuna que resta, declarada:** cada exemplo prova seu contrato isoladamente. A integração
entre os motores — traduzir o tipo de um para o do outro — ainda não tem teste que a exercite de
ponta a ponta. Está registrada no `16-Roadmap` de cada volume.

## Recuperação: 2 volumes que a geração em lote havia destruído

A auditoria descobriu que a geração de volumes em lote de 2026-08-02 sobrescreveu **quatro**
volumes já escritos, cortando seções de ~2 KB para 31 bytes de template. Dois (`01`, `31`) foram
reescritos do zero em 2026-08-03 sem que a perda fosse notada; os outros dois continuavam
esqueletos e foram recuperados do histórico:

| Volume | Antes do lote | Depois | Agora |
|---|---|---|---|
| `02-CORE` | 37.838 bytes, 18 seções | 142 bytes | **restaurado** — gate 1 verde |
| `04-REQUIREMENTS` | 33.414 bytes, 17 seções | 122 bytes | **restaurado** — gate 1 verde |

Os dois passam no gate sem nenhuma alteração e estão limpos na verificação de domínio neutro.
Permanecem `RASCUNHO` — nunca foram auditados.

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
