---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Uma decisão que parece inteiramente técnica — "este projeto vai usar o modelo X do provedor Y" —
deixa de ser só técnica no momento em que um segundo projeto, meses depois, toma a mesma decisão
de forma independente. Sozinha, cada escolha parece barata e razoável. Somadas, produzem
dependência de um único fornecedor espalhada por dez sistemas que nenhuma pessoa enxerga de uma
vez, porque cada equipe só vê o próprio projeto.

Este volume trata do nível que enxerga essa soma: o portfólio de sistemas de uma empresa, não um
sistema isolado. A pergunta central não é "este sistema está bem arquitetado?" — isso é
`02-CORE` e os volumes de arquitetura de camada. É "este sistema, somado aos outros do
portfólio, cria uma dependência, um custo agregado, ou uma duplicação que ninguém decidiu de
propósito?".

A tensão que este volume administra é real e não se resolve escondendo um lado: decisão de
portfólio que trava toda escolha de fornecedor por projeto produz lentidão insuportável; ausência
completa de visão de portfólio produz dez fornecedores diferentes fazendo a mesma coisa, cada um
com contrato, suporte e superfície de risco próprios. A resposta deste volume é uma fronteira
específica, não um extremo: portfólio decide sobre o que tem consequência cruzando projeto
(vendor lock-in, fluxo de dado que atravessa fronteira de governança); projeto decide sobre tudo
o mais, incluindo a arquitetura técnica interna inteira.
