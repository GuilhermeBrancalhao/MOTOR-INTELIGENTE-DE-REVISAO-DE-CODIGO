---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/40-templates/catalogo_de_templates.py -->

`catalogo_de_templates.py`, citado acima, formaliza AB1-AB6: `Template.__post_init__` recusa
criação sem `versao` ou `escopo_declarado` (AB1/AB6), recusa `depreciado=True` sem
`motivo_de_depreciacao` (AB5), e recusa corpo contendo termo de domínio proibido
(`ConteudoDeDominioDetectado`, AB4); `renderizar` recusa uso com variável obrigatória ausente
(`VariavelAusente`, AB3); `verificar_compatibilidade` recusa `ConteudoGeradoDeTemplate` cuja
versão diverge do template atual (AB2).

`_PALAVRAS_DE_DOMINIO_PROIBIDAS` é definida como constante de módulo, não espalhada por múltiplas
funções — essa centralização é o que torna trivial manter sincronizada com a lista real usada
pela auditoria de volume deste acervo, evitando duas fontes de verdade divergentes para o mesmo
conjunto de termos proibidos ao longo do tempo.

Isso reduz drasticamente a chance de uma futura atualização da lista de termos proibidos esquecer de atualizar um dos dois lugares onde ela é consultada.

Um sistema real que precisasse de configuração por ambiente diferente poderia externalizar essa
constante, sem alterar a lógica central de verificação que já existe aqui, mantendo o restante
do módulo completamente intacto durante essa eventual mudança de configuração futura, sem
qualquer necessidade de reescrever a assinatura pública das funções já expostas por este módulo,
nem exigir que quem consome `Template` e `renderizar` precise ajustar o próprio código de uso já
escrito anteriormente contra a interface pública atual deste módulo específico do acervo.