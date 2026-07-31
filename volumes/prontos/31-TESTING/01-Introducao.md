---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-07-30
---

# Introdução

Uma suíte de teste verde não prova que o comportamento certo está protegido -- prova
que nenhum dos testes escritos até agora quebrou. As duas afirmações parecem a mesma
coisa e não são: a primeira depende de que alguém tenha escrito o teste certo, no
lugar certo, sem depender de relógio real, sem depender de ordem de execução, e sem
verificar detalhe de implementação que pode mudar sem que o comportamento mude. Este
volume trata da segunda parte -- como escrever, organizar e manter o teste -- e
deliberadamente não trata da primeira frase sozinha, que é "quanto do sistema está
coberto e a cobertura está subindo ou caindo": esse indicador agregado é `32-QUALITY`,
o vizinho mais próximo deste volume, e a fronteira entre os dois está declarada em
`03-Escopo.md`.

O defeito que motiva este volume tem três formas concretas, e as três reaparecem nos
três módulos de exemplo:

1. **Teste que depende de tempo real.** Um teste que chama `time.sleep()` ou lê
   `datetime.now()` sem controlar o relógio é lento quando passa e instável quando a
   máquina está sob carga -- a falha intermitente não indica bug no código, indica bug
   no teste.
2. **Teste que depende de detalhe de implementação em vez de comportamento.** Um teste
   que verifica *como* uma função calcula em vez de *o que* ela devolve para uma
   entrada de fronteira quebra a cada refatoração que não muda o comportamento nenhum.
3. **Duplo de teste que substitui verificação por teatro.** Um mock configurado para
   sempre devolver o que o teste espera não verifica interação nenhuma -- só confirma
   que o duplo faz o que foi programado para fazer.

Este volume é para quem está prestes a escrever a suíte de um módulo novo e precisa de
taxonomia, estrutura e critério de aceite para essa suíte -- não para quem quer um
painel de tendência de cobertura ao longo do tempo.
