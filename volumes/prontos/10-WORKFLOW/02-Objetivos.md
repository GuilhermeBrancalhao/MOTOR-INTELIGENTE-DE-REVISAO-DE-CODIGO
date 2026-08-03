---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-03
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Declarar um workflow como sequência de passos tipados**, cada um marcado como determinístico
ou de IA, com formato de entrada e saída explícito — e explicar por que essa declaração vive fora
do código que executa cada passo, não embutida numa cadeia de chamadas de função.

**Explicar o papel do checkpoint de estado** — gravado depois de cada passo concluído — e por que
ele é o que permite a um workflow de longa duração (horas ou dias, quando há espera por aprovação
humana ou processo assíncrono externo) sobreviver a reinício de processo, falha de rede, ou
indisponibilidade temporária de um provedor de modelo sem perder o progresso já feito.

**Tratar a saída de um passo de IA como não confiável até validação**, diferente de um passo
determinístico cuja saída, dado o mesmo insumo, é sempre confiável por construção — e descrever
o que o motor faz quando a saída de IA não bate com o formato esperado pelo próximo passo.

**Traçar a fronteira com `09-ORCHESTRATOR` de forma precisa**: workflow é sequência de passos de
processo de negócio com início e fim definidos, onde a ordem é fixada na declaração; orquestração
é coordenação de agentes que decidem seus próprios próximos passos, sem sequência fixa a priori.
Um workflow pode ter um passo que invoca um agente orquestrado; o inverso não é o mesmo padrão.

**Decidir quando um processo de negócio deveria ser modelado como workflow em vez de como agente
autônomo** — a resposta depende de quanto da sequência é conhecida de antemão versus decidida em
tempo de execução pelo próprio sistema.
