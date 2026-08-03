---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 06-Fluxogramas
status: PRONTO
atualizado_em: 2026-08-03
---

# Fluxogramas

O fluxo central de prova por mutação já está em `04-Arquitetura.md`. Esta seção detalha o
processo de decisão de quando um teste precisa dessa prova versus quando é aceitável sem ela.

## Quando a prova por mutação é obrigatória

Todo teste que protege uma invariante de segurança, de integridade de dado, ou de comportamento
que, se quebrado silenciosamente, custaria caro para detectar depois (a classe de teste que este
próprio acervo chama de "prova por mutação" em `01-FUNDACAO`, `17-SECURITY` e em todos os
volumes de motor deste ciclo) precisa ter passado pelo ciclo de mutação pelo menos uma vez,
mesmo que a mutação não fique no código permanentemente — o registro de que a prova foi feita
(num comentário, num changelog de teste) é o que sustenta a confiança de que o teste não é
decorativo.

## Quando a prova é dispensável

Um teste puramente de caminho feliz, que documenta "entrada X produz saída Y esperada" sem
afirmar proteger nenhuma invariante específica, não precisa da mesma prova — seu valor é
documentação executável de comportamento, verificável simplesmente por rodar e ver que passa. A
distinção entre os dois tipos de teste, se não for feita explicitamente, tende a fazer toda a
suíte parecer igualmente robusta quando na verdade só uma fração dela foi de fato provada contra
regressão específica.

## O que fazer quando a mutação não quebra o teste

Se um teste continua passando depois de uma mutação deliberada que deveria violar a regra, a
ação correta é reescrever o teste (não descartar a mutação e seguir adiante) — o teste, como
estava, não protegia a regra que afirmava proteger, e deixá-lo sem correção mantém uma falsa
sensação de cobertura.
