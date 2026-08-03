---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 07-Regras
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Regras

## Invariantes

**Checkpoint é gravado e confirmado antes do motor avançar para o próximo passo, nunca depois.**
Um avanço sem checkpoint confirmado deixaria um estado ambíguo — o passo N pode ter concluído,
mas se o processo falhar antes do checkpoint ser gravado, a retomada não saberia disso e
reexecutaria o passo N, que pode não ser idempotente.

**Saída de passo de IA nunca é aceita sem validação de formato contra o contrato do próximo
passo.** Um passo determinístico é aceito se a chamada teve sucesso, porque sua saída é
repetível por construção; um passo de IA precisa da verificação explícita, porque a mesma
chamada pode produzir saída fora do formato esperado mesmo com sucesso técnico da chamada.

**Todo checkpoint contém informação suficiente para retomada completa, nunca depende de estado
que só existe em memória do processo.** Um workflow em espera (`AguardandoSinal` ou `Pausado`)
precisa ser retomável por um processo diferente do que entrou naquele estado — reinício de
infraestrutura não pode ser motivo de perda de progresso.

**Nenhum passo já concluído é reexecutado numa retomada**, exceto quando o passo em si falhou e
está em ciclo de correção automática declarado no workflow — a retomada avança do checkpoint,
não reinicia do começo.

**Todo passo de IA que falha validação de formato produz decisão explícita**: reexecutar com
correção automática (se declarado) ou pausar para intervenção — nunca descarte silencioso da
saída inválida seguido de avanço com dado ausente ou parcial.

## Matriz de controles

| Controle | Risco mitigado | Como é verificado |
|---|---|---|
| Checkpoint confirmado antes de avançar | Estado ambíguo entre "passo concluído" e "checkpoint gravado" após falha de processo | Teste que injeta falha entre conclusão do passo e confirmação do checkpoint, e verifica que a retomada reexecuta aquele passo específico |
| Validação de formato obrigatória para todo passo de IA | Dado fora de contrato propagando para o passo seguinte sem verificação | Teste que injeta saída de IA malformada e verifica que o próximo passo nunca recebe aquele dado sem passar por decisão de correção/pausa |
| Checkpoint sem dependência de estado em memória | Perda de progresso em reinício de processo durante espera longa | Teste que serializa, descarta o processo original, e retoma num processo novo a partir do checkpoint |
