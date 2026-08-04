---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Consolidação de conflito quando um terceiro documento chega sobre um `fato_chave` que já tem
conflito registrado — o exemplo mínimo cria um novo `Conflito` sobreposto em vez de atualizar o
existente, o que fragmentaria a visão do curador em três ou mais documentos concorrentes vistos
como dois conflitos separados.

Resolução automática de conflito por regra declarada (por exemplo, "origem X sempre prevalece
sobre origem Y") — hoje toda resolução passa por decisão humana ou por confiança numérica simples,
sem uma linguagem de regra mais expressiva para casos recorrentes.

Versionamento de documento (histórico de mudanças de um mesmo documento ao longo do tempo, além
de expiração binária) — hoje um documento revalidado simplesmente volta a `Valido`, sem manter
rastro de que versão anterior existia e o que mudou.

Integração formal com `30-AI-GOVERNANCE` para documento que contém dado sensível — o volume
assume que a autoridade de origem é suficiente sinal, mas não especifica o gatilho exato de
quando isso aciona revisão de governança.

## Ordem de cobertura pretendida

Primeiro, código de referência mínimo (`Documento`, `Origem`, ciclo de vida, detecção de
conflito), testado por mutação nas seis regras. Depois, integração real com `14-VECTOR` (o
momento exato em que documento validado é entregue para indexação) e `13-RAG` (consulta de
estado de ciclo de vida no momento da recuperação).

## O que este volume assume que pode mudar

O modelo de três estados (válido/expirando/expirado) é o mínimo suficiente hoje — um domínio com
regulação mais estrita pode exigir estados adicionais (por exemplo, "sob revisão legal"), sem
que isso quebre o princípio central de K2.
