---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Uma interface que consome uma chamada de IA tem um padrão de latência e falha diferente de uma
interface que consome uma API CRUD tradicional: a resposta pode levar segundos, pode chegar
incrementalmente em fragmentos, e pode falhar de formas que uma chamada determinística
raramente falha (o modelo se recusa, o provedor está sobrecarregado, a resposta não atende ao
formato esperado). Uma arquitetura de frontend que trata os dois casos de forma idêntica —
mesmo indicador de carregamento genérico, mesmo tratamento de erro genérico — esconde do usuário
exatamente a informação que ele precisaria para entender o que está acontecendo.

Este volume trata da camada de interface dentro do mesmo produto — como o estado do cliente
reflete uma resposta de IA que chega em stream, onde fica a fronteira entre o estado de um
componente específico e o estado global da aplicação, e o que acontece visivelmente quando a
camada de IA falha, demora ou é abandonada pelo usuário antes de terminar.

`16-INTEGRATION` trata da chamada que cruza a fronteira do produto — outro time, outro
fornecedor, outro ciclo de release. Este volume trata de camada interna do mesmo produto: a
interação entre o componente de interface e o estado que ele gerencia, mesmo quando esse estado é
alimentado por uma chamada de IA que, por baixo, atravessa a fronteira do 16.
