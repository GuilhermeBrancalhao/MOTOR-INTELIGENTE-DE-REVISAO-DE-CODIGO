---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-03
---

# Regras

## Invariantes

**Sucesso técnico da chamada nunca é tratado como equivalente a resultado correto.** Um passo de
IA que responde sem erro de rede ou de formato ainda pode ter produzido conteúdo incorreto — a
instrumentação deste volume trata esses dois níveis (sucesso de chamada, correção de resultado)
como sinais distintos, nunca colapsados num único indicador de "deu certo".

**Todo sinal que cruza o limiar de alerta notifica, nunca fica só registrado esperando consulta
manual.** A diferença entre "observável" e "alertável" é ativa: alertável significa que alguém é
avisado no momento em que o limiar é cruzado, não que o dado está disponível para quem quiser
olhar depois.

**Limiar de alerta é calibrado a partir de distribuição real observada, nunca fixado por
adivinhação antes de existir dado.** Um limiar sem base em observação real tende a alertar demais
(gerando fadiga que faz sinais reais serem ignorados) ou muito pouco (deixando anomalia real sem
aviso).

**Decomposição de custo e latência por tipo de etapa (IA versus determinística) é obrigatória
para qualquer sinal de tempo ou custo agregado.** Um número agregado sem essa decomposição não
orienta ação — não diz se o investimento de otimização deveria ir para revisão de modelo/prompt
ou para código/infraestrutura convencional.

**Falha do próprio mecanismo de alerta (canal de notificação indisponível, supressão manual
esquecida) é, em si, um sinal monitorado.** Um sistema de alerta que pode falhar silenciosamente
sem que ninguém saiba que ele falhou reintroduz exatamente o risco que a instrumentação existe
para eliminar.

## Matriz de controles

| Controle | Risco mitigado | Como é verificado |
|---|---|---|
| Distinção entre sucesso técnico e correção de resultado em todo sinal de IA | Falha de qualidade mascarada por sucesso de infraestrutura | Teste que injeta saída tecnicamente válida mas semanticamente incorreta e verifica que o sinal de "correção" a captura separadamente do sinal de "sucesso de chamada" |
| Notificação ativa para todo sinal que cruza limiar | Anomalia detectada mas não comunicada, atrasando resposta | Teste que força um sinal a cruzar o limiar configurado e verifica que uma notificação é de fato disparada, não só registrada |
| Monitoramento do próprio canal de alerta | Falha silenciosa do mecanismo de aviso, deixando o sistema "cego" sem que ninguém saiba | Verificação periódica (heartbeat) do canal de notificação, com alerta reverso se o heartbeat falhar |
| Decomposição de custo/latência por tipo de etapa em todo painel agregado | Investimento de otimização direcionado para a etapa errada | Revisão de painel exigindo a decomposição como campo obrigatório, não opcional |
