---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(user, "Usuario", "Interage com a interface")
    System(ui, "Componente de Interface", "Renderiza estado de RequisicaoDeIA")
    System_Ext(api, "API do produto (25)", "Contrato entre frontend e backend")
    System_Ext(integ, "Integracao externa (16)", "Chamada que cruza a fronteira do produto")
    System_Ext(global_state, "Estado Global", "Escopo compartilhado, promocao explicita")

    Rel(user, ui, "Dispara acao dirigida por IA")
    Rel(ui, api, "Consome resposta via contrato do 25")
    Rel(api, integ, "Chamada de IA pode atravessar fronteira externa")
    Rel(ui, global_state, "Promove resultado apenas com autorizacao explicita")
```

O `Estado Global`, no diagrama, recebe uma seta rotulada explicitamente como condicional — a
promoção nunca é automática, e essa é a única relação do diagrama que carrega essa ressalva,
porque é a única onde um vazamento silencioso de escopo causaria dano real a partes não
relacionadas da interface.

```mermaid
sequenceDiagram
    participant User as Usuario
    participant UI as Componente de Interface
    participant Req as RequisicaoDeIA
    participant Prov as Provedor (via 16/25)

    User->>UI: dispara acao
    UI->>Req: iniciar()
    Req-->>UI: estado = CARREGANDO
    loop enquanto fragmentos chegam
        Prov-->>Req: fragmento de resposta
        Req->>Req: receber_fragmento() (F2, incremental)
        Req-->>UI: texto_parcial() atualizado
    end
    alt resposta completa
        Req->>Req: concluir()
        Req-->>UI: estado = CONCLUIDO
    else falha do provedor
        Req->>Req: falhar(motivo)
        Req-->>UI: estado = ERRO
    else usuario abandona a acao
        UI->>Req: cancelar()
        Req-->>UI: estado = CANCELADO, fragmentos futuros ignorados
    end
```

O ramo de cancelamento não é um caso de erro — é um terceiro caminho legítimo e paralelo aos
outros dois, porque abandono de ação pelo usuário é comum o suficiente numa interface real para
merecer tratamento de primeira classe, não ser tratado como uma falha inesperada.


A separação entre `Provedor (via 16/25)` e `Componente de Interface`, no diagrama de sequência,
existe para deixar claro que a interface nunca fala diretamente com o provedor de IA — ela
sempre passa pelo contrato do 25 e, quando aplicável, pela robustez de chamada externa do 16. O
diagrama de sequência mostra a granularidade de fragmento a fragmento porque é exatamente aí que
F2 e F5 interagem: cada fragmento precisa checar se a requisição ainda está ativa antes de ser
aceito.

Nenhum dos dois diagramas modela um caso em que a interface espera pela resposta completa antes
de mostrar qualquer coisa — essa omissão é deliberada, porque esse caminho é exatamente o
anti-pattern que F2 existe para evitar, e um diagrama de arquitetura não deveria normalizar
visualmente um comportamento que o volume trata como erro.