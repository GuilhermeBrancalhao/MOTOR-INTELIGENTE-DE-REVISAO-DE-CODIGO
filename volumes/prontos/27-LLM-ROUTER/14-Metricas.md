---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de chamadas roteadas para fallback versus principal, por tarefa.** Um valor alto e
sustentado é sinal de que o candidato "principal" declarado talvez devesse ser reavaliado como
principal de fato.

**Número de transições entre principal e fallback numa janela de tempo (indicador de
flapping).** Deveria ser raro; um número alto indica que os limiares de degradação ou a janela de
estabilidade precisam de calibração.

**Tempo médio em estado de fallback antes de recuperar.** Contextualiza o impacto real de uma
degradação — recuperação rápida é diferente, para fins de decisão operacional, de uma degradação
que persiste por horas.

**Cobertura de tarefas com fallback declarado e efetivamente testado sob roteamento real.**
Complementa a métrica equivalente do `26-AI-MODELS` — fallback declarado mas nunca de fato
roteado na prática é um risco não verificado.


Estas quatro métricas, lidas junto das métricas equivalentes do `26-AI-MODELS`, formam uma visão
completa da confiabilidade de modelo: seleção correta de candidato de um lado, comportamento de
roteamento saudável e estável do outro — nenhuma delas sozinha conta a história inteira.

Um sistema que otimiza métricas de roteamento isoladamente, sem olhar para as métricas de seleção do 26, corre o risco de mascarar um problema de um lado com um ajuste do outro.