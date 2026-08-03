---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-03
---

# Introdução

O AI-ENGINEERING-OS é composto por quarenta e dois volumes numerados, e todos eles dependem
de uma resposta a uma pergunta que nenhum dos outros quarenta e um responde por conta própria:
quem pode escrever o quê, com que grau de revisão, e o que faz um volume passar de rascunho a
referência confiável. Sem essa resposta escrita e aplicada por máquina, cada volume inventaria
sua própria noção de "pronto", e a plataforma inteira degeneraria na mesma doença que ela existe
para corrigir em código gerado por IA: afirmação sem verificação, convincente na superfície e
vazia por dentro.

Este volume — FUNDACAO — é onde essa resposta mora. Ele não descreve nenhuma tecnologia
específica de prompt, agente ou RAG; ele descreve a engenharia da própria engenharia: os papéis
que produzem e revisam um volume, os quatro critérios que definem PRONTO, a matriz de controles
que diz quando uma mudança precisa de segundo par de olhos, e o ciclo de vida que um documento
percorre da primeira frase até virar referência confiável. Todo outro volume do acervo herda
essas regras por citação, não por repetição: o `contrato.json` em `00-INTRODUCAO` é a forma
executável delas, e este volume é a forma que explica o porquê de cada regra existir e o que
custa ignorá-la.

A razão de FUNDACAO ser o volume "01" e não ter dependências (`depende_de: []`) é literal: não
existe volume anterior a ele para depender de. Ele é lido antes de qualquer outro, porque os
demais assumem que quem os lê já sabe o que significa um volume estar `RASCUNHO`,
`REQUER_REVISAO` ou `PRONTO`, e já sabe que uma seção `07-Regras` num volume `GOVERNANCA` carrega
uma matriz de controles e não uma lista solta de boas intenções.

## Por que governança de plataforma de documentação exige o mesmo rigor que código

Uma objeção razoável é perguntar por que documentação — texto, não código executável — precisa de
papéis, matriz de controles e portas de aprovação como se fosse um sistema de produção. A resposta
é que este acervo alimenta decisões de arquitetura e de processo em outros volumes que viram
código diretamente: um volume tipo `ENGINE` mal revisado propaga um padrão de prompt ou de agente
falho para todo componente que o citar como referência normativa. O texto aqui é a especificação;
especificação errada custa mais caro do que implementação errada, porque a implementação errada
corrige uma instância e a especificação errada corrige N instâncias, uma por uma, depois que o
dano já rodou em produção nos times que confiaram no documento. Governar como se produzisse não é
exagero — é reconhecer o raio de propagação real de um volume de fundação.
