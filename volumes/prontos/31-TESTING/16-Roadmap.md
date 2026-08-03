---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Ferramenta de mutação automatizada (mutation testing tooling) — o processo descrito neste volume
é manual: mutar código de propósito, observar se o teste falha, revisar. Ferramentas existem em
várias linguagens para automatizar esse ciclo (gerando mutações sistematicamente e reportando
quais sobrevivem sem detecção), mas este volume não recomenda uma ferramenta específica, porque
o princípio (prova por mutação) é independente de automação — automação é aceleração da prática,
não a prática em si.

Métricas quantitativas de "qualidade de teste" alinhadas com este processo, formalizadas — hoje
`14-Metricas.md` descreve o que medir em termos qualitativos (proporção com prova registrada,
taxa de rastreabilidade), mas não define um índice único agregado; esse índice, se vier a
existir, é mais apropriadamente parte de `32-QUALITY`, que trata do indicador agregado.

## Ordem de cobertura pretendida

Este volume, sendo processo sem código próprio, não tem uma "ordem de implementação" no sentido
dos volumes de motor — sua aplicação prática já está distribuída pelos volumes essenciais deste
ciclo. O próximo passo natural é `32-QUALITY`, que consome os conceitos definidos aqui
(rastreabilidade regra-teste, distinção caminho-feliz/regressão) para definir o indicador
agregado que orienta decisão de release.

## O que este volume assume que pode mudar

O critério de "quando a prova por mutação é obrigatória" (07-Regras.md) pode ser refinado com
experiência real de aplicação — hoje o critério é qualitativo (invariante de segurança,
integridade, comportamento caro de detectar depois); um critério mais objetivo, se emergir de uso
real, substituiria o atual sem alterar o princípio central do volume.
