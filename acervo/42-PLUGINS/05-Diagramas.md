---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 05-Diagramas
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Diagramas

```mermaid
C4Context
    Person(dev, "Desenvolvedor de plugin", "Publica extensao para o host")
    System(host, "Host", "Contrato de extensao versionado, isolamento de falha")
    System_Ext(plugin, "Plugin de terceiro", "Declara contrato alvo, capacidades, ponto de entrada")
    System_Ext(sdk, "SDK (41)", "Disciplina de superficie publica reaproveitada pelo contrato de extensao")

    Rel(dev, plugin, "Desenvolve e publica")
    Rel(plugin, host, "Declara-se para ativacao")
    Rel(host, plugin, "Chama hook isolado, concede so capacidade declarada")
    Rel(host, sdk, "Reaproveita disciplina de versionamento do contrato de extensao")
```

O `Host` nunca chama um hook de `Plugin de terceiro` diretamente sem passar pela camada de
isolamento — toda chamada atravessa `executar_hook_isolado`, o que garante que uma falha dentro
do plugin nunca se propague além dessa fronteira, mesmo quando o plugin em si nunca foi
inspecionado linha a linha por quem mantém o host.

```mermaid
sequenceDiagram
    participant Host as Host
    participant Reg as Registro de ativacao
    participant Plugin as Plugin de terceiro

    Host->>Reg: ativar_plugin(contrato_do_host, declaracao)
    alt contrato incompativel
        Reg-->>Host: ContratoIncompativel (AD1)
    else contrato compativel
        Reg-->>Host: plugin ativado
        Host->>Plugin: executar_hook_isolado(hook)
        alt hook lanca excecao
            Plugin-->>Host: ResultadoDeHook(sucesso=False, erro=...)
        else hook funciona
            Plugin-->>Host: ResultadoDeHook(sucesso=True, valor=...)
        end
    end
```

Note que o caminho de falha do hook nunca interrompe o fluxo do `Host` com uma exceção não
tratada — o resultado estruturado é sempre retornado, sucesso ou falha, permitindo que o host
decida o que fazer (registrar, desativar o plugin, seguir adiante) sem nunca arriscar propagação
não controlada de erro de terceiro.

Note que nenhum dos dois diagramas mostra o `Plugin de terceiro` chamando o `Host` diretamente —
toda interação passa por uma camada intermediária (registro de ativação, ou execução isolada de
hook), o que é exatamente o ponto: o host nunca confia ciegamente no código de terceiro, mesmo
depois de ativado com sucesso.

A ordem das setas no `sequenceDiagram` é deliberada: verificação de contrato sempre antes de
qualquer chamada de hook, nunca depois — inverter essa ordem tornaria possível, ainda que
brevemente, executar código de um plugin já sabido incompatível antes de rejeitá-lo, um risco que
o diagrama torna explícito para quem for implementar essa mesma sequência de eventos.