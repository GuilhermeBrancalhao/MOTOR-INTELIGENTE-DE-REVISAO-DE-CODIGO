---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Registrar autoridade de origem em todo documento ingerido** — de onde veio, quem o validou,
com que nível de confiança — como campo obrigatório, não como metadado opcional que a maioria dos
pipelines de ingestão pula.

**Definir e aplicar ciclo de vida de documento**: válido, expirando, expirado — com a garantia de
que documento expirado nunca é devolvido como válido por padrão, mesmo que continue
tecnicamente indexado.

**Detectar conflito entre documentos sobre o mesmo fato** e decidir explicitamente qual prevalece
(por autoridade, por recência, ou por decisão humana registrada) — nunca deixar o ranqueamento de
`13-RAG` decidir isso implicitamente por acidente de similaridade.

**Tratar falha de ingestão como evento explícito**, nunca como documento silenciosamente ausente
— um documento que falhou ao entrar na base precisa aparecer como falha registrada, não como
lacuna que ninguém percebe até fazer falta numa resposta.

**Traçar a fronteira com `13-RAG` e `14-VECTOR`**: este volume decide o que pode ser recuperado
(curadoria); `14` decide como é indexado; `13` decide o que de fato é recuperado e vira resposta.
As três perguntas são independentes, e confundi-las produz sistema onde ninguém sabe quem é
responsável por um documento desatualizado aparecendo numa resposta.
