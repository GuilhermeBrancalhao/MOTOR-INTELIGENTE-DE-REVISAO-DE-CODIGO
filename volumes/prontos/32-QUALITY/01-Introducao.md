---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

`31-TESTING` estabelece a tese central deste par de volumes: cobertura de linha mede execução, não
verificação — um teste pode passar por um trecho de código sem provar nada sobre a regra que
deveria proteger. Este volume trata do indicador agregado que decorre dessa tese: como medir
qualidade de forma que reflita prova real, não apenas execução; como usar essa medida para
bloquear release; como registrar dívida técnica explicitamente; e como acompanhar tendência ao
longo do tempo, não apenas uma fotografia isolada.

A distinção com o 31 é a mesma que separa prática de indicador em qualquer disciplina: o 31 é
como se escreve, organiza e mantém teste — a prática do dia a dia de quem escreve código. Este
volume é o número agregado que resulta dessa prática, e o que se faz com esse número — gate de
release, registro de dívida, decisão sobre quando investigar uma queda.

O risco central que este volume existe para evitar é o mesmo risco de qualquer indicador: que ele
vire meta em vez de medida. Um indicador de qualidade perseguido pelo número, não pelo que o
número representa, degenera exatamente como qualquer métrica otimizada isoladamente — alguém
encontra a forma de inflar o número sem melhorar o que ele deveria medir.
