---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 01-Introducao
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Introdução

Este volume documenta o motor de workflows: a peça de engenharia responsável por
executar um processo de negócio de longa duração como uma sequência declarada de
passos, alguns determinísticos e outros não-determinísticos. Um passo determinístico
transforma dados, valida um payload ou chama uma API externa e, dado o mesmo insumo,
produz sempre a mesma saída. Um passo de IA chama um modelo de linguagem para
interpretar texto livre, decidir entre alternativas ambíguas ou gerar conteúdo, e por
natureza pode produzir saídas diferentes para o mesmo insumo, ou saídas fora do
formato esperado. O motor existe porque nenhum dos dois tipos de passo, isolado,
resolve o processo inteiro: pipelines puramente determinísticos não lidam com texto
livre, e cadeias soltas de chamadas a modelo não garantem repetibilidade nem retomada
depois de uma falha.

A unidade central do volume é o workflow como grafo de passos declarado fora do
código que executa cada passo. Essa declaração é o contrato entre quem desenha o
processo e o motor que o executa: descreve a ordem, as dependências entre passos, o
formato de entrada e saída de cada um, e qual tratamento se aplica quando um passo de
IA devolve algo que não bate com o formato esperado. O motor lê essa declaração e
avança o workflow um passo de cada vez, gravando um checkpoint do estado depois de
cada passo concluído. É esse checkpoint que permite que uma execução de dias — comum
quando um passo depende de aprovação humana ou de um processo assíncrono externo —
sobreviva a uma reinicialização do processo, a uma falha de rede ou a uma
indisponibilidade do provedor de modelo sem perder o trabalho já feito.

O volume também demarca sua fronteira com o volume 09-ORCHESTRATOR, porque os dois
termos — workflow e orquestração — são usados de forma intercambiável fora deste
acervo, e essa confusão custa decisões de arquitetura erradas. Workflow, aqui, é a
sequência de passos de um processo de negócio com início e fim definidos, onde a
ordem importa e o estado é gravável. Orquestração, no volume 09, é a coordenação de
múltiplos agentes autônomos que decidem seus próprios próximos passos dentro de um
objetivo comum. Um workflow pode conter um passo que invoca um agente orquestrado;
um orquestrador não contém um workflow dentro de si no mesmo sentido, porque a
sequência de agentes não é fixa a priori. Essa distinção volta a aparecer, com mais
detalhe, na seção 18.
