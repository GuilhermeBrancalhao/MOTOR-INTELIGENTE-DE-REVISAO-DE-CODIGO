---
volume: "08"
volume_nome: AGENT-ENGINE
tipo: ENGINE
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-03
---

# Arquitetura

```mermaid
C4Context
    title Contexto do motor de execução de agente
    Person(chamador, "Quem invoca", "Orquestrador (09), workflow (10), ou código de aplicação")
    System(motor, "Agent Engine", "Ciclo de vida do agente: loop decisao-acao-observacao, orcamento")
    System_Ext(modelo, "Modelo de linguagem", "Decide a proxima acao a cada passo, via 27-LLM-ROUTER")
    System_Ext(ferramentas, "Ferramentas disponiveis", "Executam a acao decidida e devolvem observacao")
    System_Ext(trilha, "Trilha de auditoria", "Registra cada passo, decisao e motivo de encerramento")
    Rel(chamador, motor, "Objetivo + ferramentas disponiveis + orcamento")
    Rel(motor, modelo, "Historico + ferramentas + orcamento restante, por passo")
    Rel(motor, ferramentas, "Executa a acao decidida")
    Rel(motor, trilha, "Registra cada passo")
    Rel(motor, chamador, "Resultado final + motivo de encerramento")
```

O motor fica entre quem invoca (que decide *que* agente rodar e com que objetivo) e três
dependências externas: o modelo de linguagem (que decide a ação a cada passo, mas não sabe nada
sobre orçamento além do que o motor informa), as ferramentas (que executam e devolvem
observação, sem saber que fazem parte de um agente), e a trilha (que registra para auditoria
posterior). Nenhuma dessas três dependências decide quando o ciclo termina — essa decisão é
exclusivamente do motor, aplicando as regras de orçamento e de objetivo atingido descritas em
`07-Regras.md`.

## Componentes internos

O **executor de passo** monta o prompt do passo (histórico + ferramentas + orçamento restante),
chama o modelo, e valida a resposta contra o contrato (uma ação por passo). O **despachante de
ferramenta** recebe a ação decidida, localiza a ferramenta correspondente, executa, e captura
tanto sucesso quanto erro como observação — erro de ferramenta nunca aborta o loop sozinho, ele
volta como observação para o próximo passo decidir o que fazer, a menos que o erro seja marcado
como não recuperável. O **guardião de orçamento** decrementa passos/tokens/tempo a cada passo e
força encerramento quando qualquer dimensão chega a zero, independente do que o modelo decidiu.
O **registrador de trilha** grava cada passo, cada decisão do guardião de orçamento, e o motivo
final de encerramento — é esse componente que faz a diferença entre "terminou" e "terminou por
quê" existir na auditoria.
