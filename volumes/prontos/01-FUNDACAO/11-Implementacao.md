---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-03
---

# Implementação

<!-- exemplo: exemplos/01-fundacao/definicao_de_pronto.py -->

A governança descrita neste volume não é aspiracional. `definicao_de_pronto.py`, citado acima, é
a forma executável dos quatro critérios — incluindo a leitura do critério 2 que manteve sete
volumes em `RASCUNHO` mesmo com auditoria acima de 8,0: não citar exemplo não é caso vacuo que
passa, é critério não satisfeito. E a governança também está implementada em três módulos do
motor, de que este texto é o manual.

`ferramentas/contrato.py` carrega `00-INTRODUCAO/contrato.json` e expõe `Contrato.secoes_de(tipo)`
(quais das 18 seções são obrigatórias para o tipo), `Contrato.diagramas_de(tipo)` (quais tipos de
diagrama Mermaid são exigidos) e `Contrato.minimo_de(secao)` (quantas palavras de prosa, com
fallback para o mínimo global). Todo consultante de regra passa por esta classe — nenhuma parte
do motor lê `contrato.json` diretamente.

`ferramentas/validar.py` implementa os quatro comandos que operam a governança:
`validar_volume(raiz, vol_id, ct)` roda o gate 1 (estrutural) num único volume;
`validar_tudo(raiz, ct)` roda o mesmo gate em todos os volumes materializados no disco, sem
levantar erro para volume "pendente" (ainda não criado); `validar_cross_refs(raiz, ct)` verifica
o grafo de `depende_de` por aciclicidade e por referência a volume declarado. Nenhuma dessas
funções corrige nada — `validar_volume` está documentada explicitamente como "Aplica todas as
regras de um volume. Nao levanta por conteudo ruim", ou seja, ela relata, o redator corrige.

`ferramentas/frontmatter.py` implementa o parser YAML restrito que lê tanto o front-matter de
seção quanto o `_VOLUME.yml` — a mesma gramática, dois contextos de uso. A restrição deliberada
(escalares, booleanos, inteiros, listas em linha) é o que permite mensagem de erro precisa por
linha, sem depender de biblioteca externa de YAML completo.

## O bug de BOM, como estudo de caso de implementação

O bug encontrado em 2026-08-03 — `_VOLUME.yml` escrito com BOM UTF-8, fazendo
`ler_volume_yml()` ver a primeira chave como `"﻿volume"` em vez de `"volume"` — não estava
no parser; estava em como os arquivos foram *escritos* originalmente (por um script gerador que
não especificou `encoding="utf-8"` sem BOM explicitamente). A correção não foi mudar o parser
para tolerar BOM — seria mascarar o sintoma em vez de consertar a causa, e teria escondido
qualquer BOM real inserido por acidente no futuro. A correção foi reescrever os 39 arquivos sem
BOM, na fonte.
