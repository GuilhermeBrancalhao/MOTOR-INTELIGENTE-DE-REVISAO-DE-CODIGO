---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-03
---

# Implementação

<!-- exemplo: exemplos/10-workflow/checkpoint.py -->

`checkpoint.py`, citado acima, é a implementação de referência da garantia central: gravar,
confirmar, só então avançar. O teste que injeta a queda de processo entre a gravação e a
confirmação prova a escolha conservadora — sem checkpoint confirmado, o passo reexecuta.

## Como um motor real implementaria este contrato

O gestor de checkpoint é o componente que mais exige disciplina de implementação: a gravação
precisa ser atômica do ponto de vista de "o passo concluiu E o checkpoint foi gravado", ou
nenhum dos dois — um checkpoint parcialmente gravado é pior que nenhum checkpoint, porque a
retomada confiaria em dado incompleto. A técnica clássica é escrever o checkpoint novo antes de
apagar ou invalidar o anterior, garantindo que sempre existe um checkpoint válido e completo
disponível, mesmo que a escrita do novo seja interrompida no meio.

O validador de saída de IA se beneficia de reaproveitar o mesmo tipo de verificação de schema que
qualquer validação de entrada de API usaria — não é uma técnica exclusiva de IA, é validação de
contrato de dados aplicada especificamente ao ponto onde a fonte da saída (um modelo) não garante
conformidade por construção, diferente de uma função determinística testada.

A ordem de implementação recomendada é: modelo de dados (`Passo`, `Checkpoint`) e gestor de
checkpoint primeiro, testado com falha injetada no meio da gravação; validador de saída de IA
segundo, testado com um conjunto de saídas malformadas conhecidas; executor de passo e gestor de
sinal externo por último, integrando os anteriores.

## Onde a integração com outros volumes acontece

Um passo de IA que invoca um agente delega a execução para `08-AGENT-ENGINE` e recebe de volta um
`ResultadoExecucao` — a tradução para o contrato deste motor segue o mesmo padrão descrito em
`09-ORCHESTRATOR/11-Implementacao.md`: `OBJETIVO_ATINGIDO` vira saída a validar contra o formato
esperado; os outros dois motivos de encerramento viram falha do passo, disparando a política de
correção ou pausa deste volume.
