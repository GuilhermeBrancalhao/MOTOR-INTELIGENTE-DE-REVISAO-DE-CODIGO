---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Escrever o contexto de um ADR pensando em alguém que não estava na sala quando a decisão foi
tomada — se o contexto só faz sentido para quem já sabia da conversa, ele não cumpre a função de
preservar entendimento para o futuro.

Revisar ADRs antigos periodicamente para verificar se o contexto que os motivou ainda é
verdadeiro — um ADR nunca é editado, mas pode ser superado por um novo quando as circunstâncias
mudaram o suficiente.

Automatizar a verificação de vigência sempre que possível, em vez de depender de revisão manual
esporádica — um teste que falha quando código e documentação divergem é mais confiável do que
lembrar de checar.

Nomear claramente, no próprio título ou cabeçalho de um documento, se ele é gerado
automaticamente — quem abre o arquivo deveria saber isso antes de considerar editá-lo diretamente.


Incluir, no ADR, as alternativas consideradas e descartadas, não apenas a decisão final — mesmo
que o modelo mínimo deste volume não exija esse campo, registrar o que foi rejeitado e por quê
enriquece o contexto disponível para quem revisitar a decisão no futuro.

Um parágrafo curto listando duas ou três alternativas descartadas, com o motivo específico da rejeição, já cumpre bem essa função sem exigir um documento extenso.