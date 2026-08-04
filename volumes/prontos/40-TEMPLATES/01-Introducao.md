---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

Este acervo já usa template extensivamente, mesmo sem nomear a prática como tal até este volume:
o front-matter de seção (`volume`, `secao`, `status`, `atualizado_em`), o scaffold de
`_VOLUME.yml`, o `conftest.py` de três linhas copiado para cada pasta de exemplo. Cada um desses
é um template — uma estrutura reutilizável com variável obrigatória (o número do volume, o nome
da seção) preenchida a cada uso.

Um template mal disciplinado causa dois problemas opostos: se as variáveis obrigatórias não são
declaradas explicitamente, alguém só descobre o que precisa preencher lendo a saída gerada e
tentando adivinhar; se o template embute conteúdo específico de domínio — nome de cliente,
sistema específico — ele deixa de ser reutilizável e vira um documento disfarçado de template.
Este acervo já pratica a segunda disciplina há tempo: a verificação de domínio neutro, rodada a
cada volume promovido, existe precisamente para garantir que nenhum template ou conteúdo carregue
menção a projeto irmão específico.

Este volume formaliza essa prática como catálogo: toda entrada declara variável obrigatória,
versão, escopo do que produz, e nunca embute conteúdo específico de domínio — a mesma disciplina
que este acervo já aplica à sua própria produção, agora nomeada e catalogada explicitamente.

Nomear a prática explicitamente, mesmo quando ela já é seguida informalmente, tem valor próprio —
torna possível auditar, catalogar e melhorar algo que antes só existia como convenção tácita
repetida por quem escrevia cada volume novo, sem nenhum lugar único que documentasse a lista
completa de templates em uso.