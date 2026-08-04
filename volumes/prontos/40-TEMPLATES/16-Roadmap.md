---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Ferramenta de migração automática entre versões de template, aplicando transformação declarada
sobre conteúdo já gerado pela versão anterior — hoje `verificar_compatibilidade` apenas detecta
divergência, sem oferecer caminho de correção automática.

Extração automática da lista de variáveis obrigatórias a partir do corpo do template (análise de
placeholder), em vez de declaração manual separada — hoje as duas listas (corpo e
`variaveis_obrigatorias`) podem divergir se alguém esquecer de atualizar uma delas.

Integração formal com a ferramenta de scaffold deste acervo (`ferramentas/scaffold.py`,
`ferramentas/gerador_scaffold.py`) para que os templates reais já em uso sejam catalogados
formalmente por este volume, não apenas documentados em prosa.

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (template versionado, variável validada, neutralidade de
domínio, depreciação explícita), testado por mutação nas seis regras. Depois, integração real
com `ferramentas/scaffold.py` deste próprio acervo.

## O que este volume assume que pode mudar

O modelo de substituição de string simples (`str.format`) é o mínimo suficiente hoje — um motor
de template mais expressivo (condicional, laço) pode ser necessário conforme a complexidade dos
templates catalogados cresce, sem alterar o princípio central de variável declarada, versão, e
neutralidade de domínio.
