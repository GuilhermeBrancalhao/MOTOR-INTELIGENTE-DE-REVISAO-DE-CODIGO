---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 03-Escopo
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Escopo

## Dentro deste volume

A governança da própria plataforma de documentação: papéis (quem escreve, quem audita, quem
decide escopo), o ciclo de vida de um volume (`RASCUNHO` → `REQUER_REVISAO`/`PRONTO`), a matriz
de controles que determina quando uma mudança exige revisão adicional, e os quatro critérios da
Definição de PRONTO. Este volume é a explicação em prosa do que `00-INTRODUCAO/contrato.json` e
`00-INTRODUCAO/Convencoes.md` implementam de forma executável — quando os dois divergem, o
contrato vence, e é isso que o teste `test_convencoes_nao_derivou` (fora do escopo deste volume,
mora no motor) verifica.

## Fora deste volume, e para onde vai

**A arquitetura técnica de qualquer motor de IA específico** (prompt, agente, orquestrador) não
é assunto de FUNDACAO — é assunto dos volumes que descrevem cada motor (`07-PROMPT-ENGINE`,
`08-AGENT-ENGINE`, `09-ORCHESTRATOR`). FUNDACAO governa *como qualquer volume é escrito e
aprovado*, não *o que um motor de IA faz*.

**A arquitetura corporativa e o encaixe da plataforma num portfólio de TI maior** é
`02-CORE` e `06-ENTERPRISE-ARCHITECTURE` — FUNDACAO não decide onde o acervo se encaixa fora de
si mesmo, só como ele se governa internamente.

**Segurança e controles de um sistema de IA em produção** é `17-SECURITY` — a matriz de
controles deste volume é sobre o processo de *documentar*, não sobre o sistema de IA que a
documentação descreve. As duas matrizes de controle não se confundem: uma audita texto, a outra
audita comportamento de sistema.

**Observabilidade e métricas de produção** é `21-OBSERVABILITY` — `14-Metricas.md` deste volume
mede a saúde do próprio processo de documentação (quantos volumes estão `PRONTO`, quanto tempo
uma auditoria leva), não a telemetria de um sistema rodando.

## Fronteira deliberada

FUNDACAO não define conteúdo técnico de nenhum domínio — ele define a régua com que todo
conteúdo técnico é medido. Um volume que precisa saber "o que é um bom exemplo de código citável"
lê a regra de código em `Convencoes.md`; um volume que precisa saber "quem decide se este texto
está bom o bastante" lê este volume.
