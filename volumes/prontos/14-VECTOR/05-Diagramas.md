---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
sequenceDiagram
    participant Con as 11-KNOWLEDGE
    participant Idx as Vector Engine
    participant Rag as 13-RAG

    Con->>Idx: documento validado
    Idx->>Idx: gera embedding, associa versao do modelo
    Idx->>Idx: registra na particao declarada
    Rag->>Idx: consulta (vetor de busca, metrica, particao)
    alt metrica ou particao nao declaradas
        Idx-->>Rag: rejeitado, consulta incompleta
    else consulta completa
        Idx->>Idx: compara so vetores da mesma versao de modelo e particao
        Idx-->>Rag: N vetores mais proximos, com score na metrica declarada
    end
```

A rejeição de consulta incompleta (ramo do meio) é o ponto mais importante do diagrama: um índice
que aceitasse consulta sem métrica ou partição declaradas teria que assumir um padrão implícito,
e esse padrão implícito é exatamente o tipo de decisão que deveria ser explícita — a métrica usada
na indexação, não uma suposição da camada de consulta.

## Reindexação atômica

```mermaid
flowchart LR
    A[Indice atual, versao V1] --> B[Construir indice novo, versao V2, em paralelo]
    B --> C{V2 completo e validado?}
    C -->|Nao| B
    C -->|Sim| D[Trocar ponteiro de consulta: V1 para V2, operacao unica]
    D --> E[V1 descartado apos periodo de retencao]
```

A troca em `D` é uma operação única do ponto de vista de quem consulta — nunca existe um momento
em que parte da consulta vê V1 e parte vê V2 simultaneamente. Construir o índice novo em paralelo,
sem afetar o antigo até a troca completa, é o que garante essa atomicidade sem exigir período de
indisponibilidade — o custo é espaço de armazenamento duplicado durante a construção, não tempo
de espera para quem consulta.

## Por que a validação acontece antes da troca, não depois

Um índice que trocasse o ponteiro de consulta para a versão nova antes de validá-la completamente
exporia inconsistência ao primeiro consumidor que chegasse durante a janela de validação. A ordem
`B -> C -> D` no diagrama garante que a troca em si (`D`) só acontece depois que a versão nova já
provou estar completa — o custo de validar antes de trocar é tempo adicional de construção; o
custo de trocar antes de validar seria expor erro de reindexação diretamente a quem consulta.
