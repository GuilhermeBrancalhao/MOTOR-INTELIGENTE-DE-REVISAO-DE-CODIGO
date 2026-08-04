---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Escrever teste de migração que roda contra dado no formato antigo, confirmando que o código novo
consegue ler e escrever corretamente antes de qualquer consumidor ser migrado — a compatibilidade
declarada em A1 deveria ser verificada, não apenas assumida pela boa intenção da mudança.

Registrar proveniência mesmo quando parece óbvio qual modelo gerou o conteúdo — o "óbvio" de hoje
se torna ambíguo assim que um segundo modelo entra em uso, e reconstruir proveniência
retroativamente raramente é possível com precisão.

Tratar todo conflito de concorrência (A3) como sinal de que passou tempo suficiente entre leitura
e escrita para outra mudança acontecer — se conflitos são frequentes, vale investigar se a janela
entre ler e escrever pode ser reduzida, não apenas tratar cada conflito individualmente.

Revisar política de retenção junto de mudança de schema relacionada, não como processo
totalmente separado — um campo novo às vezes muda o que faz sentido reter e por quanto tempo.


Registrar, junto de cada migração aplicada, a data e quem a aplicou — mesmo que o modelo mínimo
deste exemplo não exija esses campos, um histórico de migração real precisa dessa informação para
que uma investigação futura consiga reconstruir a sequência exata de mudanças que um schema
específico atravessou.