---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`PromptPromovido` é a representação local do contrato consumido do 07 — carrega `hash`,
`variaveis_declaradas` e `estado`, o mínimo necessário para as verificações deste volume, sem
duplicar toda a máquina de estados que pertence ao 07.

`Dialeto` carrega `formatar_mensagens` como campo do tipo função — essa é a implementação
concreta de Q4: o próprio tipo central de dialeto é definido pela função de tradução que carrega,
não por um enum de provedores conhecidos que precisaria crescer a cada novo provedor suportado.

`PayloadCompilado` é imutável e carrega `hash_origem` junto do resultado — a rastreabilidade até
o prompt de origem é parte estrutural do tipo, não uma informação que precisa ser lembrada
separadamente.


Nenhum dos quatro tipos centrais (`PromptPromovido`, `Dialeto`, `PontoDeCache`,
`PayloadCompilado`) contém lógica de negócio própria além de armazenar dado imutável —
`compilar`, a única função com lógica de decisão, opera sobre esses tipos sem que nenhum deles
precise saber como é usado, o que os torna simples de testar isoladamente se necessário.

Essa separação entre dado imutável e lógica de decisão centralizada é o que torna cada verificação fácil de testar isoladamente, sem simular comportamento inesperado de um tipo que deveria ser passivo.

Se algum dia um desses tipos ganhar comportamento próprio, isso sinalizaria que a responsabilidade está migrando para fora de onde deveria estar.