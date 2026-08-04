---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de conteúdo gerado por IA com proveniência registrada.** Deveria ser 100% por
construção (A2 impede a criação de registro sem proveniência), então uma queda indica falha no
próprio processo de gravação, não apenas descuido pontual.

**Frequência de conflito de concorrência por coleção.** Um número crescente pode indicar que a
janela entre leitura e escrita está grande demais para o volume de escrita concorrente real,
merecendo revisão da lógica de orquestração que produz essas escritas.

**Tamanho de coleção ao longo do tempo, comparado contra a política de retenção declarada.** Uma
coleção crescendo além do que sua política de retenção deveria permitir é sinal de que a
expiração não está sendo de fato executada, não apenas declarada.

**Contagem de exclusões rejeitadas por referência ativa.** Um número alto pode indicar que o
fluxo de negócio deveria excluir referências antes de tentar excluir o registro alvo, ou que a
ordem de operações do processo que dispara a exclusão precisa de ajuste.


Estas quatro métricas, lidas em conjunto ao longo de várias semanas, revelam se a disciplina de
persistência está sendo mantida na prática, não apenas disponível como opção — proveniência
caindo abaixo de 100% ou coleção crescendo além da retenção declarada são os dois sinais mais
diretos de que uma das seis regras está sendo contornada em algum ponto do sistema.