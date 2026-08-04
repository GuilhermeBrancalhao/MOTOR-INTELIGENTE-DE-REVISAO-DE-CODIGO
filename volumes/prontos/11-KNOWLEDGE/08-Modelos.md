---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

## Documento

`Documento(id: str, conteudo: str, origem: Origem, fato_chave: str | None, estado: EstadoCiclo)`
— `fato_chave` é usado pelo detector de conflito para agrupar documentos que afirmam algo sobre o
mesmo assunto; `None` significa documento sem fato singular associado (não participa de detecção
de conflito).

## Origem

`Origem(fonte: str, validado_por: str, confianca: float)` — os três campos obrigatórios de K1.
`confianca` é um valor entre 0 e 1, usado para desempate quando um conflito não tem resolução
humana explícita ainda.

## EstadoCiclo

`Valido`, `Expirando`, `Expirado` — os três estados de K2, com transição unidirecional exceto
`Expirando -> Valido` (revalidação explícita, K6).

## Conflito

`Conflito(documentos: tuple[str, ...], fato_chave: str, resolvido: bool, prevalece: str | None)`
— `prevalece` é `None` até resolução humana (ou automática por confiança mais alta, se a política
permitir), nunca preenchido por acidente de ordem de ingestão. O campo `documentos` guarda, num
único registro, todos os documentos ainda válidos que competem sobre o mesmo `fato_chave` no
momento em que o novo chega — uma limitação conhecida do exemplo mínimo é que um terceiro
documento sobre o mesmo fato gera um novo `Conflito` sobreposto ao anterior em vez de atualizar
o registro existente, o que um motor real precisaria consolidar (ver `16-Roadmap.md`).

## Por que `fato_chave` é opcional em `Documento`

Nem todo documento compete com outro sobre uma afirmação específica — um documento de referência
geral (um manual, por exemplo) pode não ter um `fato_chave` singular. Tornar o campo obrigatório
forçaria uma categorização artificial nesses casos; deixá-lo `None` e excluir esses documentos da
detecção de conflito é a modelagem mais honesta do domínio real.
