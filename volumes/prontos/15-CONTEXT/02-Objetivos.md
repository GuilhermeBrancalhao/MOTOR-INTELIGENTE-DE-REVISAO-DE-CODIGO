---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Declarar orçamento de tokens explicitamente**, nunca deixar implícito que "cabe o que couber" —
um sistema sem orçamento declarado descobre o limite por erro de truncamento em produção, não por
decisão de desenho.

**Definir ordem de prioridade para o que entra na janela** antes que o limite seja atingido, não
no momento da pressão — instrução do sistema, histórico recente, documento recuperado e
resultado de ferramenta competem pelo mesmo espaço, e a prioridade entre eles precisa estar
decidida de antemão.

**Registrar o que é descartado quando o orçamento é excedido**, nunca descartar silenciosamente.
Um sistema que trunca histórico sem registro não tem como diagnosticar depois por que uma resposta
pareceu esquecer algo que foi dito antes.

**Decidir o gatilho de compactação** (resumir histórico antigo em vez de simplesmente descartá-lo)
antes da janela chegar ao limite, com margem suficiente para a compactação em si não competir com
o espaço que está tentando liberar.

**Aplicar orçamento de contexto mesmo em sistema sem RAG.** Este volume não pressupõe recuperação
de conhecimento — vale para qualquer sistema que acumula histórico, incluindo os mais simples.

**Diagnosticar corretamente quando uma resposta "esqueceu" algo dito antes** — verificando o
registro de descarte deste volume antes de assumir que é limitação do modelo, quando pode ser
simplesmente conteúdo descartado por orçamento sem que ninguém tenha ajustado a prioridade.
