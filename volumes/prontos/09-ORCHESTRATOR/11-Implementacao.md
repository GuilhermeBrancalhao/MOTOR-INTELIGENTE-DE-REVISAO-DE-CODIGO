---
volume: "09"
volume_nome: ORCHESTRATOR
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-03
---

# Implementação

<!-- exemplo: exemplos/09-orchestrator/grafo.py -->

`grafo.py`, citado acima, é a implementação de referência: ordenação topológica com detecção de
ciclo por marcação de três estados, política de falha por nó e resultado granular. Os testes que o
acompanham provam as invariantes de `07-Regras.md`, incluindo a que mais custa se quebrar — o
`all` do fan-in, cuja troca por `any` liberaria agregação com dado parcial.

## Como um motor real implementaria este contrato

A validação do grafo (detecção de ciclo, referência a nó inexistente) é um algoritmo clássico de
ordenação topológica com detecção de ciclo (por exemplo, busca em profundidade com marcação de
três estados: não visitado, visitando, concluído — a mesma técnica usada em
`ferramentas.validar --cross-refs` deste próprio acervo para detectar ciclo em `depende_de`,
descrita em `01-FUNDACAO/11-Implementacao.md`). A semelhança não é coincidência: qualquer grafo
de dependência acíclica se beneficia do mesmo algoritmo, seja ele um grafo de nós de execução ou
um grafo de pré-requisito de leitura entre volumes.

O executor concorrente precisa de uma estrutura de controle de concorrência (semáforo ou pool de
tarefas com limite) para não disparar mais nós simultâneos do que o limite configurado. A ordem
de implementação recomendada é: planejador topológico primeiro, com testes que provam detecção
de ciclo em grafos de profundidade variável; gestor de política de falha segundo, testado
isoladamente com nós fake que sempre falham; executor concorrente por último, integrando os dois
anteriores sob um limite de concorrência configurável e testado.

## Onde a integração com outros volumes acontece

Um nó cujo `executavel` é uma execução de `08-AGENT-ENGINE` recebe o `ResultadoExecucao` daquele
motor e precisa traduzir `MotivoEncerramento.OBJETIVO_ATINGIDO` para `Sucesso` e os outros dois
motivos para `Falha` — essa tradução é responsabilidade de quem define o nó, não deste motor, que
só entende o contrato genérico `Sucesso`/`Falha` descrito em `08-Modelos.md`.
