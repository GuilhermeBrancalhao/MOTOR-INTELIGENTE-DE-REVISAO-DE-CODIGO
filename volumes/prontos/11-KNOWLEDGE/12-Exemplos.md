---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — ingestão limpa, sem conflito

Um documento novo sobre política de reembolso é ingerido com origem declarada (departamento
jurídico, confiança 0.95). Nenhum documento existente compartilha o mesmo `fato_chave`
("política de reembolso vigente"). Ingerido diretamente em estado `Valido`, sem sinalização.

## Caso 2 — conflito detectado e resolvido por autoridade

Um segundo documento chega meses depois, também sobre "política de reembolso vigente", com
conteúdo diferente e origem de menor confiança (0.6, de um resumo interno não oficial). O
detector sinaliza conflito; o curador resolve que o documento original (confiança 0.95) prevalece,
e o novo é rejeitado com o motivo registrado — não silenciosamente descartado.

## Caso 3 — expiração sem revalidação

Um terceiro documento, sobre uma promoção sazonal, entra com prazo de validade de 90 dias. Aos 75
dias, entra em `Expirando`; ninguém o revisa. Aos 90 dias, transita para `Expirado`
automaticamente. Uma consulta de `13-RAG` que buscaria informação sobre promoções não o recupera
mais como válido, mesmo que o documento continue fisicamente no índice de `14-VECTOR` — a
garantia de K2 opera na consulta, não na remoção física.

## Caso 4 — falha de ingestão registrada

Um quarto documento chega sem `validado_por` preenchido — um erro de integração na fonte, não
uma omissão deliberada. A tentativa de criar `Origem` levanta `OrigemIncompleta` antes mesmo de
chegar ao método `ingerir`, e a camada de integração registra a falha com o motivo exato, em vez
de descartar o documento silenciosamente e deixar a ausência ser descoberta só quando alguém
notar que falta informação numa resposta.
