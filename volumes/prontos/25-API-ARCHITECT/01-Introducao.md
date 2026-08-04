---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

O contrato que um produto expõe ao seu cliente é a única parte do sistema que o cliente pode
realmente enxergar — tudo o que acontece atrás dele (orquestração, persistência, chamada de IA)
pode mudar livremente desde que o contrato em si permaneça estável. Essa é a promessa que torna
possível evoluir o interior de um sistema sem quebrar quem o consome, e é também a promessa mais
fácil de violar por atalho: expor diretamente o formato de persistência interna porque "é mais
rápido", reutilizar um campo existente para um significado novo porque criar um campo novo parece
trabalho desnecessário, formatar erro de cada endpoint de um jeito diferente porque cada um foi
escrito em um momento diferente.

Este volume trata do contrato exposto ao cliente dentro do mesmo produto: versionamento
explícito, tradução obrigatória entre formato interno e formato exposto, formato de erro
consistente entre todos os endpoints, exposição de status de trabalho assíncrono como recurso
estável, e orçamento de latência declarado para toda operação síncrona.

`23-BACKEND-ARCHITECT` trata da orquestração que produz o resultado; `24-DATABASE-ARCHITECT`
trata de como esse resultado persiste; `16-INTEGRATION` trata da chamada que cruza a fronteira do
produto. Este volume trata da última etapa: o que efetivamente atravessa para o cliente, e sob
qual garantia de estabilidade.
