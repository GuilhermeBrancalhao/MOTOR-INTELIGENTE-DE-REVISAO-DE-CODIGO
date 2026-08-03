---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 05-Diagramas
status: PRONTO
atualizado_em: 2026-08-03
---

# Diagramas

```mermaid
sequenceDiagram
    participant De as Desenhista
    participant Mo as Motor
    participant Pa as Passo (det. ou IA)
    participant Va as Validador
    participant Ck as Checkpoint

    De->>Mo: declarar(workflow)
    loop para cada passo na sequencia
        Mo->>Pa: executar(entrada do passo)
        Pa-->>Mo: saida
        alt passo e de IA
            Mo->>Va: validar formato da saida
            Va-->>Mo: valida OU invalida
            alt invalida
                Mo->>Pa: reexecutar com correcao, ou pausar
            end
        end
        Mo->>Ck: gravar checkpoint (confirmado antes de avancar)
    end
    Mo-->>De: workflow concluido
```

A validação de saída só acontece para passos de IA — um passo determinístico, se a chamada teve
sucesso, tem sua saída aceita sem essa etapa adicional, porque a garantia de repetibilidade já
vem da própria natureza do passo. O checkpoint é gravado e confirmado antes do motor avançar para
o próximo passo da sequência — essa ordem (gravar, confirmar, só então avançar) é o que garante
que uma falha entre dois passos nunca deixa o workflow num estado onde o checkpoint diz "passo N
concluído" mas o passo N+1 já começou sem isso estar registrado.

## Passo de IA com falha de validação e recuperação

```mermaid
flowchart TD
    A[Passo de IA executa] --> B{Saida bate com formato esperado?}
    B -->|Sim| C[Aceita, grava checkpoint]
    B -->|Nao| D{Workflow declara correcao automatica?}
    D -->|Sim| E[Reexecuta com instrucao de correcao]
    E --> B
    D -->|Nao| F[Pausa workflow, aguarda intervencao]
```

O fluxo mostra que a saída inválida de um passo de IA nunca é aceita silenciosamente — ou o
workflow tem uma estratégia declarada de correção automática (reexecutar com uma instrução
adicional apontando o que estava errado), ou o motor pausa e espera intervenção, nunca segue
adiante com dado que não bate com o contrato esperado pelo próximo passo. O ciclo de reexecução
com correção tem limite de tentativas (ver `08-Modelos.md` e `09-Boas-Praticas.md`) — sem esse
limite, uma saída consistentemente malformada faria o motor tentar indefinidamente sem nunca
convergir, consumindo tempo e tokens sem produzir resultado utilizável. Quando o limite se
esgota, o fluxo cai no mesmo ramo de `Pausado` que uma saída sem correção automática declarada
alcançaria diretamente — os dois caminhos convergem no mesmo estado de espera por intervenção.
