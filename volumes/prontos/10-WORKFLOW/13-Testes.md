---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-03
---

# Testes

## Estratégia

Testar este motor exige simular falha no ponto exato entre "passo concluído" e "checkpoint
confirmado" — não é suficiente testar só o caminho feliz de execução completa sem interrupção. A
técnica é injetar falha de processo (ou de gravação de checkpoint) em pontos programados da
execução e verificar que a retomada, a partir do checkpoint que de fato foi confirmado antes da
falha, produz o mesmo resultado final que uma execução sem interrupção teria produzido.

## O que a suíte precisa cobrir

Cada transição do `stateDiagram-v2` em `06-Fluxogramas.md`, incluindo os dois estados de espera
(`AguardandoSinal`, `Pausado`) sobrevivendo a reinício de processo simulado. A validação de saída
de IA precisa de teste com saída válida, saída inválida com correção automática disponível
(verificando reexecução com instrução de correção), e saída inválida sem correção automática
(verificando transição para `Pausado`, não descarte silencioso). A distinção entre passo
determinístico e de IA precisa de teste que confirma que um passo determinístico nunca passa pela
etapa de validação de formato — só a chamada é verificada, não o conteúdo da saída.

## Prova por mutação

Um teste forte para "checkpoint confirmado antes de avançar" é um que falha se alguém trocar a
ordem para "avançar, depois confirmar checkpoint" — testável fixando uma falha determinística
exatamente entre as duas operações e verificando que, com a ordem correta, a retomada refaz o
passo (comportamento conservador esperado), e com a ordem trocada por mutação, a retomada pularia
o passo incorretamente (comportamento que o teste deveria capturar como falha).

## Testes de integração com volumes vizinhos

Um passo que invoca `08-AGENT-ENGINE` precisa de teste de integração que verifica a tradução
completa dos três motivos de encerramento daquele motor para o contrato deste volume — sucesso
vira saída a validar, os outros dois viram falha do passo com o motivo original preservado na
trilha do workflow para auditoria posterior.
