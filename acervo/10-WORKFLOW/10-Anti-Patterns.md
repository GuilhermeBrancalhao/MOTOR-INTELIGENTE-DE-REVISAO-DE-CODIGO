---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 10-Anti-Patterns
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Anti-Patterns

**Aceitar saída de passo de IA sem validação de formato "porque geralmente vem certo".**
"Geralmente" não é garantia, e o custo de propagar dado malformado para um passo seguinte que
assume formato correto é normalmente maior do que o custo de validar — a validação existe
exatamente para os casos em que "geralmente" falha.

**Gravar checkpoint só ao final do workflow inteiro, em vez de a cada passo.** Isso elimina a
vantagem central do checkpoint: um workflow de longa duração que falha no passo 8 de 10 teria
que reexecutar os 7 anteriores, incluindo qualquer passo de IA caro entre eles, se o checkpoint
só existisse no fim.

**Modelar decisão de agente autônomo como passo condicional de workflow com todas as
ramificações possíveis enumeradas antecipadamente.** Se a "decisão" de fato não é conhecida a
priori — o modelo decide livremente entre um número não fixo de próximas ações — isso é
`09-ORCHESTRATOR`, não workflow; forçar esse padrão dentro de um workflow produz uma árvore de
condições que tenta prever o imprevisível.

**Deixar o gestor de sinal externo sem timeout para `AguardandoSinal`.** Um workflow esperando
aprovação humana indefinidamente, sem prazo, acumula estado pendente sem visibilidade — mesmo
quando o processo de negócio não define um prazo formal, um timeout técnico com escalonamento
(alertar, não necessariamente abortar) evita que uma espera vire silêncio permanente.

**Misturar estado de retomada com estado de negócio de forma não separável.** Se o
`estado_acumulado` do checkpoint mistura dados que são puramente técnicos (posição na sequência)
com dados de negócio (o resultado de cada passo) sem separação clara, evoluir o formato do
checkpoint entre versões do motor fica mais arriscado — mudar um sem quebrar o outro exige que
os dois sejam distinguíveis.
