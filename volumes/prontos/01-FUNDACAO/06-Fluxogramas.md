---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 06-Fluxogramas
status: PRONTO
atualizado_em: 2026-08-03
---

# Fluxogramas

O fluxo de aprovação já está em `04-Arquitetura.md` (o `flowchart` que satisfaz a exigência de
diagrama do tipo `GOVERNANCA`). Esta seção detalha em prosa o caminho de decisão que esse
fluxograma resume, com foco no que acontece em cada ramo de reprovação — porque é aí que a
maioria dos volumes deste acervo hoje se perde: a auditoria de 2026-08-03 encontrou 39 volumes
que nunca tinham passado pelo gate 1 de verdade, e o motivo raiz não foi ausência de esforço —
foi ausência de um passo explícito de "rodar o validador antes de declarar pronto".

## Caminho feliz

Um redator escreve as seções obrigatórias do tipo do volume, com front-matter completo e prosa
acima do mínimo. Roda `python -m ferramentas.validar NN` e recebe `ok: volume NN sem violacoes`.
Cita exemplo de código, se houver, com teste correspondente em `exemplos/<vol>/tests/`, e roda a
suíte de testes desse exemplo. Só então solicita auditoria — nunca antes, porque gastar o
julgamento humano ou de outro modelo em texto que ainda tem erro estrutural é desperdiçar a parte
mais cara da verificação com um problema que a máquina resolveria de graça.

## Caminho de reprovação no gate estrutural

Toda violação reportada tem formato `arquivo:linha: [regra] mensagem` — a regra nomeada é o que
ancora a correção: `substancia-curta` significa escrever mais prosa real, não adicionar
espaço em branco; `frontmatter-campo` significa um campo ausente no front-matter, não o volume
inteiro estar errado; `marcador-proibido` significa uma palavra específica (`TODO`, `PENDENTE`
etc.) fora de um code span. Corrigir sem entender qual regra disparou tende a trocar um problema
por outro — foi assim que a remoção ingênua de um BOM de `_VOLUME.yml` poderia ter sido feita
seção por seção em vez de resolvida na causa raiz (o encoding de escrita do arquivo).

## Caminho de reprovação na auditoria

Auditoria com média abaixo de 8,0, ou qualquer seção abaixo de 6, grava `REQUER_REVISAO` — nunca
mantém `RASCUNHO` (o volume já passou dos gates mecânicos, não regrediu para "nem tentado") e
nunca força `PRONTO` (a nota não atingiu o piso). O redator recebe o relatório de auditoria por
seção, corrige as seções fracas especificamente, e reenvia — não precisa refazer o volume inteiro
se só três das dezoito seções ficaram abaixo de 6.
