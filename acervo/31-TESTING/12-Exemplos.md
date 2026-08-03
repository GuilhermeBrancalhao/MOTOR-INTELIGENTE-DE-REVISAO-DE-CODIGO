---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 12-Exemplos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Exemplos

## Caso 1 — teste nomeado pela violação, não pela função

O padrão `test_valores_redondos_repetidos_em_dias_diferentes_nao_sao_duplicata`, usado no volume
`45-CONCILIACAO-CONTAS` do acervo-controladoria, nomeia exatamente o cenário que seria um bug se
o teste falhasse: dois valores iguais em dias diferentes sendo tratados incorretamente como
duplicata. Comparado a um nome genérico como `test_guarda_caso_2`, o primeiro permite a qualquer
leitor entender o que está sendo protegido sem abrir o corpo do teste — e permite, na revisão de
uma suíte inteira, avaliar cobertura de regra por simples leitura dos nomes.

## Caso 2 — prova por mutação revelando teste decorativo

Um teste hipotético `test_guarda_bloqueia_duplicata` que só verifica "registrar a mesma chave duas
vezes retorna verdadeiro na segunda vez" pode passar mesmo se a implementação da guarda comparar
só valor absoluto, ignorando data e contraparte — porque o teste nunca testou o caso que
distinguiria as duas implementações (dois valores iguais, contextos diferentes). Mutar a guarda
para comparar só valor e rodar a suíte revelaria que esse teste específico não captura a
regressão, mesmo que "pareça" testar duplicata — é exatamente esse tipo de descoberta que a prova
por mutação existe para produzir antes que a regressão aconteça em produção.

## Caso 3 — teste de fluxo completo capturando quebra de composição

O teste `test_fluxo_completo_de_conciliacao_com_escrita`, também em `45-CONCILIACAO-CONTAS`,
exercita cinco módulos (âncora, casamento, confiança, guarda, trilha) na ordem real de uso. Um
teste unitário de cada módulo isoladamente não capturaria uma inversão acidental na ordem de
chamada entre guarda e trilha — cada módulo, isolado, continuaria correto; só a composição
exercitada na ordem certa revela se a integração entre eles preserva a garantia de não duplicar
escrita.
