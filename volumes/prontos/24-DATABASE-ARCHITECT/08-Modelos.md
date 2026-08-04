---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`Procedencia` é um par imutável (`modelo`, `versao`) — deliberadamente simples, porque sua função
é apenas identificar de forma estável o que produziu um conteúdo, não descrever configuração
completa da chamada que o gerou (isso, se necessário, pertence a um registro de auditoria mais
amplo, fora do escopo mínimo deste modelo).

`RegistroDeConteudo` carrega `campos_desconhecidos` como um dicionário separado dos campos
reconhecidos — essa separação explícita é o que torna A5 uma garantia rastreável: um campo que o
código atual não reconhece não é descartado nem confundido com um campo esperado, ele fica
visivelmente marcado como "não interpretado por esta versão do código".

`Migracao` carrega a flag `compativel_com_versao_anterior` como campo obrigatório, não com valor
padrão — forçando quem declara uma migração a decidir explicitamente sobre compatibilidade, em
vez de um padrão que poderia mascarar uma migração incompatível declarada sem essa reflexão.


Todos os quatro tipos centrais são frozen ou têm validação em `__post_init__` — nenhum permite
que um estado inválido seja construído e só detectado mais tarde, quando já foi passado adiante
para outra parte do sistema que assumiu que ele era válido.

Nenhum dos quatro tipos centrais carrega método que modifique outro objeto além de si mesmo —
`Repositorio` é o único componente com efeito colateral sobre estruturas externas
(`self.registros`, `self.politicas_de_retencao`), o que mantém `Migracao`, `Procedencia` e
`RegistroDeConteudo` simples de raciocinar isoladamente, sem depender de contexto externo para
entender seu comportamento completo.