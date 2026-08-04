---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`Template` é imutável e recusa sua própria criação sem `versao` ou `escopo_declarado` (AB1/AB6
combinados na mesma verificação), e recusa criação marcada como `depreciado=True` sem
`motivo_de_depreciacao` (AB5) — as duas verificações acontecem juntas em `__post_init__`, antes
de o template existir como entrada válida do catálogo.

A verificação de conteúdo de domínio em `Template.__post_init__` reaproveita o mesmo conjunto de
palavras (`concilia`, `controladoria`, `omie`, `sicoob`) já usado pela verificação de domínio
neutro deste acervo em todo volume promovido — não uma segunda lista paralela mantida
separadamente, mas literalmente o mesmo vocabulário proibido.

`ConteudoGeradoDeTemplate` carrega `template_versao` junto do conteúdo — a rastreabilidade entre
o que foi gerado e qual versão do template o gerou é o que torna possível verificar
compatibilidade (AB2) depois que o template evolui.


Ambos os tipos centrais são imutáveis — um `Template` ou um `ConteudoGeradoDeTemplate` representa
um fato específico de um momento, e qualquer mudança de versão produz uma nova instância, nunca
uma mutação do objeto anterior, preservando o histórico completo de versões já usadas em algum
momento por este acervo ou por qualquer outro projeto que reutilize este catálogo.

Essa disciplina de imutabilidade é a mesma já aplicada consistentemente a outros tipos que representam fato histórico em vários outros volumes deste acervo.