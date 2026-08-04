---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 05-Diagramas
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Desenvolvedor externo", "Instala e integra o SDK no proprio codigo")
    System(sdk, "SDK", "Superficie publica minima, versao semantica, erro acionavel")
    System_Ext(api, "API do produto (25)", "Contrato de rede que o SDK encapsula")
    System_Ext(docs, "Exemplos de uso", "Verificados contra o codigo real do SDK")

    Rel(dev, sdk, "Importa e chama a superficie publica")
    Rel(sdk, api, "Encapsula chamada de rede real")
    Rel(sdk, docs, "Fornece exemplo verificado, nunca documentacao que diverge")
    Rel(dev, docs, "Consulta exemplo antes de integrar")
```

O `SDK` nunca expõe o contrato de rede do `25-API-ARCHITECT` diretamente — ele encapsula essa
chamada atrás da superfície pública deliberada, o que permite ao SDK evoluir sua implementação
interna (incluindo como fala com a API) sem quebrar o código do desenvolvedor externo, desde que
a superfície pública em si permaneça estável dentro da mesma versão maior.

```mermaid
sequenceDiagram
    participant Dev as Desenvolvedor externo
    participant SDK as SDK
    participant API as API do produto (25)

    Dev->>SDK: chama metodo publico
    SDK->>SDK: valida entrada
    alt entrada invalida
        SDK-->>Dev: ErroDoSDK (o que falhou + como corrigir)
    else entrada valida
        SDK->>API: encapsula chamada de rede real
        API-->>SDK: resposta
        SDK-->>Dev: resultado na superficie publica do SDK
    end
```

O erro retornado ao desenvolvedor nunca é a exceção bruta de rede ou de biblioteca interna — o
SDK sempre traduz para `ErroDoSDK`, carregando orientação de correção, mesmo quando a causa raiz
é uma falha de rede que o desenvolvedor externo não tem como diagnosticar sozinho sem essa
tradução.

Essa distinção de responsabilidade entre `SDK` e a `API do produto` que ele encapsula é o que
permite ao time responsável pelo SDK reagir a uma mudança na implementação interna sem quebrar
nenhum código de terceiros, desde que a superfície pública do SDK em si permaneça estável durante
essa mesma versão maior — o encapsulamento é o que absorve a mudança interna antes que ela chegue
ao desenvolvedor externo.

Os dois diagramas juntos mostram a jornada completa: o `C4Context` situa o SDK entre o
desenvolvedor externo e a API real que ele encapsula, enquanto o `sequenceDiagram` detalha o que
acontece dentro de uma única chamada, incluindo o caminho de erro traduzido.