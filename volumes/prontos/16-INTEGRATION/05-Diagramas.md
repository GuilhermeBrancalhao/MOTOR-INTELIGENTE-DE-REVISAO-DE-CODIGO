---
volume: "16"
volume_nome: INTEGRATION
tipo: ARQUITETURA
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
sequenceDiagram
    participant Con as Consumidor
    participant Gw as Integration Gateway
    participant Ext as Sistema Externo

    Con->>Gw: chamada (chave de idempotencia, versao esperada)
    Gw->>Gw: circuit breaker fechado? (sistema externo saudavel)
    alt circuito aberto (externo degradado)
        Gw-->>Con: falha imediata, sem tentar a chamada
    else circuito fechado
        Gw->>Ext: requisicao, com timeout configurado
        alt timeout ou erro de rede
            Gw->>Gw: retry com a mesma chave de idempotencia
            Gw->>Ext: nova tentativa
        end
        Ext-->>Gw: resposta
        Gw->>Gw: verifica versao do contrato
        alt versao incompativel
            Gw-->>Con: erro explicito de incompatibilidade
        else versao compativel
            Gw-->>Con: resposta verificada
        end
    end
```

O circuito aberto (ramo superior) é a defesa que impede uma chamada nova de sequer tentar contra
um sistema já conhecido como degradado — sem essa proteção, cada chamada nova esperaria pelo
timeout completo antes de falhar, multiplicando a lentidão externa pela quantidade de chamadas
simultâneas que o sistema interno está tentando fazer.

## Ciclo do circuit breaker

```mermaid
flowchart LR
    A[Fechado: chamadas passam normalmente] --> B{Taxa de falha acima do limiar?}
    B -->|Sim| C[Aberto: falha imediata, sem tentar]
    C --> D[Apos periodo de espera, tenta uma chamada de teste]
    D --> E{Chamada de teste teve sucesso?}
    E -->|Sim| A
    E -->|Nao| C
    B -->|Nao| A
```

O estado `Aberto` nunca é permanente — o ciclo sempre volta a testar o sistema externo depois de
um período, porque a alternativa (permanecer aberto para sempre até intervenção manual) impediria
recuperação automática quando o sistema externo volta a funcionar normalmente.

## Por que o retry preserva a chave de idempotência

O `alt` de timeout no diagrama mostra a nova tentativa usando a mesma chave da tentativa
original, nunca uma chave gerada de novo — essa é a conexão direta entre o mecanismo de retry
(I3) e a garantia de idempotência (I2): sem preservar a chave entre tentativas, cada retry seria
uma operação logicamente nova aos olhos do sistema externo, e a proteção contra duplicação
deixaria de existir exatamente no cenário em que mais é necessária — falha de rede intermitente,
onde não se sabe se a operação original teve efeito ou não do outro lado. O diagrama de sequência
e o fluxograma de estados do circuit breaker se complementam: o primeiro mostra uma chamada
individual passando pelas verificações; o segundo mostra como o histórico de múltiplas chamadas
ao longo do tempo determina se a próxima sequer chega a ser tentada.
