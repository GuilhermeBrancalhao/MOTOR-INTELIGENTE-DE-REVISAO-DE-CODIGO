---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(client, "Cliente", "Consome o contrato exposto")
    System(contrato, "Contrato de API", "Versionamento, traducao, erro consistente")
    System_Ext(backend, "Backend (23)", "Orquestra trabalho, produz resultado interno")
    System_Ext(db, "Persistencia (24)", "Formato interno, nunca exposto diretamente")

    Rel(client, contrato, "Requisicao versionada")
    Rel(contrato, backend, "Consulta estado de trabalho, resultado interno")
    Rel(backend, db, "Le e grava formato interno")
    Rel(contrato, client, "Resposta traduzida, formato de erro consistente")
```

A seta entre `Persistencia (24)` e `Cliente` não existe no diagrama — deliberadamente, porque não
há caminho direto entre os dois. Toda informação que chega ao cliente passa pelo `Contrato de
API`, que é o único ponto autorizado a decidir o que do formato interno atravessa e o que não.

```mermaid
sequenceDiagram
    participant Client as Cliente
    participant Contrato as Contrato de API
    participant Backend as Backend (23)

    Client->>Contrato: requisicao (versao declarada)
    Contrato->>Backend: enfileira trabalho
    Backend-->>Contrato: id do trabalho, estado interno
    Contrato->>Contrato: traduz para RecursoDeStatusDeTrabalho
    Contrato-->>Client: id, estado, url de consulta
    Client->>Contrato: consulta status pela url
    Contrato->>Backend: consulta estado interno
    Backend-->>Contrato: estado interno (do modelo do 23)
    Contrato->>Contrato: traduz para resposta externa
    Contrato-->>Client: resposta traduzida (nunca o formato interno bruto)
```

A tradução acontece duas vezes no diagrama — na resposta inicial e na consulta de status — porque
nenhuma resposta ao cliente pula essa etapa, mesmo quando a informação de origem já está
disponível pronta internamente.


O `Backend (23)` aparece como sistema externo consultado pelo `Contrato de API`, nunca o
contrário — o backend não sabe nada sobre formato de resposta externa, apenas sobre estado
interno de trabalho; é o contrato que decide como traduzir esse estado para o que o cliente vê.

O diagrama de sequência mostra a tradução acontecendo tanto na resposta inicial quanto na
consulta de status subsequente, nunca apenas uma vez — isso comunica visualmente que a garantia
de T2 não é um evento único no momento de criar o trabalho, é uma disciplina aplicada a toda
resposta que sai do sistema, em qualquer ponto da interação com o cliente.

Isso vale mesmo quando a resposta parece trivial de montar — a disciplina de nunca pular a
tradução é o que a diferencia de um atalho que só existe até o dia em que o formato interno muda.