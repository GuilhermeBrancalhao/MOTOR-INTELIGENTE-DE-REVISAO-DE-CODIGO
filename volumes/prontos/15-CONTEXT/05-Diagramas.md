---
volume: "15"
volume_nome: CONTEXT
tipo: ENGINE
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
sequenceDiagram
    participant Sis as Instrucao do sistema
    participant His as Historico
    participant Rag as Documentos (13-RAG)
    participant Ges as Context Engine
    participant Mo as Modelo

    Sis->>Ges: conteudo, prioridade maxima
    His->>Ges: turnos de conversa, prioridade declarada
    Rag->>Ges: documentos recuperados, prioridade declarada
    Ges->>Ges: soma tokens, compara contra orcamento total
    alt excede o orcamento
        Ges->>Ges: descarta por ordem de prioridade inversa, registra o descartado
    end
    Ges->>Mo: janela montada dentro do orcamento
```

A instrução do sistema entra com prioridade máxima declarada explicitamente, não por estar
tecnicamente "primeira" na montagem — um gestor que prioriza por ordem de chegada em vez de
prioridade declarada corre o risco de descartar instrução crítica só porque ela chegou depois de
um histórico longo, o que inverteria exatamente a intenção de quem desenhou o sistema.

## Gatilho de compactação

```mermaid
flowchart LR
    A[Consumo atual da janela] --> B{Proximo do limite, com margem definida?}
    B -->|Nao| C[Segue acumulando normalmente]
    B -->|Sim| D[Aciona compactacao do historico mais antigo]
    D --> E[Historico antigo vira resumo, ou e descartado com registro]
    E --> C
```

A margem em `B` existe para que a compactação em si tenha espaço para operar sem competir pelo
espaço que está tentando liberar — acionar compactação só quando o limite já foi atingido deixaria
o processo de compactação (que também consome tokens, se envolver geração de resumo) sem
orçamento disponível para funcionar.

## Por que a instrução de sistema nunca aparece no ramo de descarte

O diagrama de sequência não mostra nenhum caminho em que a instrução de sistema seja avaliada
para descarte — essa omissão é proposital, refletindo C6: a instrução só entra em consideração de
remoção no caso extremo (e tratado à parte) de exceder o orçamento total sozinha, nunca como
parte do ciclo normal de descarte por pressão de outras categorias. Um leitor que procurasse, no
diagrama, uma seta de "descarta instrução" não encontraria nenhuma — e essa ausência é a prova
visual de que a garantia não depende de disciplina externa, está embutida na própria forma do
fluxo descrito.
