---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste do exemplo é nomeada no docstring, não deixada implícita.

`test_controle_sem_verificacao_e_reportado_como_lacuna` prova D1/D6: se o gate tratasse ausência
de `verificacao_automatizada` como aprovação, este teste falharia — a mutação que ele mata é
"assumir enforçado quando não há check".

`test_falha_sem_waiver_bloqueia` prova D2: a mutação alvo é o gate permitir a mudança prosseguir
mesmo sem waiver — o teste falha se o bloqueio por padrão for removido.

`test_waiver_expirado_nao_impede_bloqueio` prova D3: a mutação alvo é o gate continuar honrando
um waiver após sua data de expiração — o teste avança a data de avaliação para depois da
expiração e confirma que a falha volta a bloquear.

`test_waiver_ativo_permite_prosseguir_com_excecao_registrada` prova que a exceção, quando válida,
de fato aparece no resultado — não apenas que a mudança passa, mas que ela passa com o waiver
nomeado visível, não silenciosamente.

`test_controle_automatizado_que_passa_e_aprovado` e `test_waiver_de_outro_controle_nao_cobre_falha`
cobrem os casos que não são regra isolada, mas a composição correta de mais de uma regra ao mesmo
tempo — o segundo prova que um waiver nomeado para um controle específico nunca vaza para cobrir
a falha de outro controle diferente, mesmo quando os dois estão sendo avaliados na mesma chamada.

Nenhum teste depende de tempo real (`datetime.now()` ou equivalente) — a data de avaliação é
sempre passada explicitamente como argumento, o que torna o teste de expiração determinístico e
livre de instabilidade por horário de execução, em vez de depender de quando a suíte roda.