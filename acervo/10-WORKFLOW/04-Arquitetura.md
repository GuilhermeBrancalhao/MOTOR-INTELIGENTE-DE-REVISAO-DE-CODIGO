---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 04-Arquitetura
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Arquitetura

```mermaid
C4Context
    title Contexto do motor de workflow
    Person(desenhista, "Quem declara o workflow", "Define a sequencia de passos fora do codigo de execucao")
    System(motor, "Workflow Engine", "Executa passos, valida saida de IA, grava checkpoint")
    System_Ext(passo_det, "Passo deterministico", "Transformacao, validacao, chamada de API — saida repetivel")
    System_Ext(passo_ia, "Passo de IA", "Via 08-AGENT-ENGINE ou chamada direta a modelo — saida nao garantida")
    System_Ext(checkpoint, "Armazenamento de checkpoint", "Estado do workflow apos cada passo concluido")
    System_Ext(sinal, "Sinal externo", "Aprovacao humana ou callback assincrono que libera um passo em espera")
    Rel(desenhista, motor, "Declaracao do workflow (sequencia + tipos de passo)")
    Rel(motor, passo_det, "Executa, saida sempre aceita se formato bate")
    Rel(motor, passo_ia, "Executa, saida validada contra formato esperado")
    Rel(motor, checkpoint, "Grava apos cada passo concluido")
    Rel(sinal, motor, "Libera passo em espera de aprovacao/callback")
```

O motor recebe uma declaração de workflow — não decide a sequência, só a executa. Cada passo é
despachado para uma de duas categorias: determinístico (cuja saída é aceita se o formato bate,
sem verificação de conteúdo além disso) ou de IA (cuja saída passa por validação de formato antes
de alimentar o próximo passo, porque o modelo pode devolver algo fora do esperado mesmo quando a
chamada em si tem sucesso). Depois de cada passo concluído, o motor grava um checkpoint — estado
suficiente para retomar exatamente do próximo passo sem reexecutar os anteriores.

## Componentes internos

O **executor de passo** despacha para o tipo correto (determinístico ou IA) e aplica a validação
de saída apropriada. O **validador de saída de IA** compara a saída devolvida contra o formato
declarado para aquele passo — se não bate, decide entre reexecutar o passo (com uma instrução de
correção, se o desenho do workflow especificar isso) ou pausar o workflow para intervenção. O
**gestor de checkpoint** serializa o estado necessário para retomada e o grava de forma durável
antes de avançar para o próximo passo — a gravação precisa ser confirmada antes do avanço, não
depois, porque um avanço sem checkpoint confirmado perderia a garantia de retomada segura. O
**gestor de sinal externo** pausa a execução num passo declarado como "espera aprovação" e
retoma quando o sinal correspondente chega, independente de quanto tempo isso leva.
