---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Verificação automática de que todo volume `PRONTO` tem arquivo de auditoria correspondente em
`auditorias/` — hoje `status.py` lê a nota se o arquivo existir, mas não reprova a ausência do
arquivo para um volume já marcado `PRONTO` manualmente. Um gate adicional
(`auditoria-ausente-para-pronto`) fecharia essa lacuna, mas não existe ainda.

Processo formal de revogação de `PRONTO` — hoje a Definição de PRONTO descreve como promover,
não como despromover um volume que foi marcado `PRONTO` mas cujo conteúdo citado (código de
exemplo, por exemplo) mudou depois de forma que invalida a auditoria original. Na prática isso
já aconteceu de forma informal quando o `volumes/prontos/` divergiu do acervo fonte (registrado
em `README.md`), mas o processo de "isso invalida o PRONTO, reabra auditoria" não está escrito.

## Ordem de cobertura pretendida

Primeiro, fechar os 10 volumes essenciais do ciclo atual (`01`, `03`, `07`, `08`, `09`, `10`,
`12`, `17`, `21`, `31`) — 3 já `PRONTO`, 7 a escrever, decisão registrada em `ROADMAP.md` do
acervo em 2026-08-03. Depois, revisitar os 32 volumes restantes seguindo o mesmo critério que já
guiava a ordem antes desta auditoria: prioridade para volume com código real para extrair e
generalizar, não ordem numérica.

## O que este volume assume que pode mudar

O número de "10 volumes essenciais" é decisão de escopo do ciclo atual, não constante do
contrato — um ciclo futuro pode redefinir o conjunto essencial, e quando isso acontecer, este
volume e `ROADMAP.md`/`ENTREGA.md` precisam ser atualizados juntos, com a mesma disciplina de
data e responsável que a decisão de 2026-08-03 seguiu.
