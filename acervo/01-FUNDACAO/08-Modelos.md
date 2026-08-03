---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 08-Modelos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Modelos

Os "modelos de dados" deste volume não são classes de um programa — são os contratos que
estruturam qualquer volume do acervo, implementados como parser de YAML restrito em
`ferramentas/frontmatter.py` e validados em `ferramentas/regras.py`.

## `_VOLUME.yml`

Sete campos por pasta de volume: `volume` (string de dois dígitos, sempre entre aspas — `"01"`
nunca `01` sem aspas, porque o parser mantém zero à esquerda como string e a ausência de aspas
sinalizaria inteiro na leitura humana), `nome`, `tipo` (um dos cinco válidos), `status`
(`RASCUNHO`, `REQUER_REVISAO` ou `PRONTO` — nunca `PENDENTE`, que é estado derivado calculado por
`status.py` para volume sem pasta, não um valor gravável), `perecivel` (booleano), `depende_de`
(lista de ids de dois dígitos, pode ser vazia) e `escopo` (uma frase).

## Front-matter de seção

Seis campos por arquivo `.md`: `volume`, `volume_nome`, `tipo` — os três coerentes com o
`_VOLUME.yml` da pasta, verificados pela regra `frontmatter-coerencia` — mais `secao` (idêntico
ao nome do arquivo sem `.md`), `status` e `atualizado_em` (ISO `YYYY-MM-DD`).

## Violação

`Violacao(arquivo: str, linha: int, regra: str, mensagem: str)` — a estrutura que toda regra do
validador devolve. `linha` igual a zero significa "o arquivo como um todo", não uma linha
específica; qualquer valor positivo é 1-indexed. O campo `regra` é o nome estável citado em
`10-Anti-Patterns.md` e em `06-Fluxogramas.md` — é por esse nome que uma violação se discute sem
ambiguidade, porque descreve o que a máquina de fato verificou.

## Relatório de auditoria

Não tem esquema formal em código (é markdown livre), mas tem uma convenção obrigatória lida por
`status.py`: uma linha no formato `media: <nota>` em algum lugar do arquivo
`auditorias/VOL-NN-auditoria-YYYY-MM-DD.md`. Essa é a única parte do relatório que a máquina
consome; o resto é para o redator humano, não para o parser.
