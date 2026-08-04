---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

O componente central é o `GateDeSeguranca`: recebe a lista de controles declarados (espelhando a
matriz do 17), o resultado de cada verificação automatizada para o commit em avaliação, e a lista
de waivers ativos. Ele não executa as verificações em si — isso é responsabilidade de cada
controle individual, tipicamente um teste ou scanner específico — o gate consolida os resultados
e decide se a mudança pode prosseguir.

Um `Controle` carrega seu nome, o vetor de risco que mitiga, e opcionalmente o identificador da
verificação automatizada que o implementa. Quando esse identificador está ausente, o controle
existe apenas como política — declarado no 17, ainda sem enforcement — e o gate trata isso como
uma lacuna visível, não como aprovação silenciosa.

Um `Waiver` liga um controle específico a um motivo e uma data de expiração. O gate consulta
waivers ativos apenas para controles que de fato falharam; um waiver para um controle que passou
não tem efeito. Passada a expiração, o waiver deixa de contar, e uma falha anteriormente
tolerada volta a bloquear — sem que ninguém precise revogar o waiver manualmente para isso
acontecer.

O resultado da avaliação (`ResultadoGate`) carrega, para cada controle que falhou e não tem
waiver válido, o nome do controle e o vetor de risco que ele mitiga — não apenas um booleano de
pass/fail, porque quem triagem a falha precisa entender o que quebrou sem abrir um segundo
documento.
