---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 13-Testes
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Testes

## Estratégia

Testar a disciplina de instrumentação deste volume exige simular tanto o caminho de sinal normal
quanto os dois caminhos de falha do próprio mecanismo de observabilidade: limiar calibrado errado
e canal de notificação indisponível. Um coletor de sinal fake, que emite eventos programados nas
três categorias (`MotivoEncerramento`, `IntervencaoHumana`, `CustoLatenciaPorEtapa`), permite
testar o avaliador de limiar sem depender de um motor real gerando o sinal.

## O que a suíte precisa cobrir

Distinção entre sucesso técnico e correção de resultado: um teste que emite um sinal de "chamada
com sucesso" e verifica que, sozinho, ele não satisfaz nenhuma verificação de "resultado
correto" — os dois precisam ser sinais estruturalmente separados, não dedutíveis um do outro.
Notificação obrigatória: um teste que força um sinal a cruzar o limiar configurado e verifica que
uma chamada de notificação de fato acontece, com falha do teste se a notificação for só
registrada sem disparo real. Heartbeat do canal: um teste que simula indisponibilidade do canal
de notificação e verifica que essa indisponibilidade gera, ela mesma, um alerta reverso.

## Prova por mutação

Um teste forte para "todo sinal que cruza o limiar notifica" é um que falha se alguém trocar a
chamada de notificação por um simples registro em log — testável mockando o canal de notificação
e verificando a chamada explícita, não inferindo sucesso pela ausência de excepção. Sem esse
teste, uma refatoração que "simplificasse" o avaliador de limiar para só registrar poderia
remover silenciosamente a garantia central deste volume.

## Testes de integração com volumes vizinhos

Um teste de integração relevante verifica que o `Sinal` emitido por `08-AGENT-ENGINE` no
encerramento de uma execução chega ao coletor deste volume com a categoria e origem corretas —
a integração testa a ponta de emissão, não só a ponta de avaliação de limiar isoladamente.
