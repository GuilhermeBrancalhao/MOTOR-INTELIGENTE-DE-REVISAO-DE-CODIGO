---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(client, "Cliente da API", "Dispara operacao que envolve IA")
    System(api, "API (25)", "Recebe requisicao, retorna id de trabalho")
    System(fila, "Fila de Trabalhos", "Estado explicito, backpressure, idempotencia")
    System_Ext(workers, "Workers sem estado", "Processam trabalho, chamam IA via 16")
    System_Ext(db, "Persistencia (24)", "Armazena estado do trabalho")

    Rel(client, api, "Requisicao que dispara trabalho de IA")
    Rel(api, fila, "Enfileira trabalho, retorna id imediatamente")
    Rel(workers, fila, "Retira proximo trabalho disponivel, sem afinidade")
    Rel(fila, db, "Persiste estado do trabalho")
    Rel(client, api, "Consulta estado do trabalho pelo id, sem bloquear")
```

A API nunca bloqueia esperando o trabalho terminar — ela enfileira e retorna um identificador
imediatamente, e uma segunda interação do cliente consulta o estado quando quiser. Essa separação
entre "disparar" e "consultar" é o que torna S1 possível: se a API bloqueasse até a conclusão, o
timeout da requisição HTTP voltaria a ser o limite real de quanto tempo um trabalho pode levar,
exatamente o problema que este volume existe para evitar.

```mermaid
sequenceDiagram
    participant Client as Cliente
    participant API as API (25)
    participant Fila as Fila de Trabalhos
    participant W as Worker (sem afinidade)

    Client->>API: dispara operacao
    API->>Fila: enfileirar(trabalho, chave_idempotencia)
    Fila-->>API: trabalho (novo ou existente, nunca duplicado)
    API-->>Client: id do trabalho, estado ENFILEIRADO
    W->>Fila: retirar_proximo()
    Fila-->>W: trabalho, estado EXECUTANDO
    alt sucesso
        W->>Fila: marcar_concluido(id, resultado)
    else falha, tentativas restantes
        W->>Fila: marcar_falha(id) -> volta para ENFILEIRADO
    else falha, tentativas esgotadas
        W->>Fila: marcar_falha(id) -> FALHOU_PERMANENTEMENTE
    end
    Client->>API: consulta estado do trabalho
    API-->>Client: estado atual, sem bloquear
```

Qualquer instância de `W` no diagrama poderia ser trocada por outra sem que o fluxo mude — nenhuma
mensagem depende de qual worker específico está processando, o que é a materialização visual de
S2.


Nenhuma mensagem no diagrama de sequência é dirigida a um worker nomeado especificamente — todas
usam o rótulo genérico `W (sem afinidade)`, e essa escolha de nomenclatura no próprio diagrama já
comunica visualmente a regra S2 antes mesmo de qualquer explicação textual.

O C4Context mostra a API retornando o id do trabalho imediatamente após enfileirar, antes de
qualquer processamento acontecer — essa é a representação visual direta de S1: a resposta da API
nunca espera o resultado da IA, apenas confirma que o trabalho foi aceito para processamento. A
consulta de estado, no final do diagrama de sequência, acontece numa troca de mensagens
completamente separada da que dispara o trabalho — reforçando que "disparar" e "verificar o
resultado" são duas interações distintas, nunca uma única chamada bloqueante.