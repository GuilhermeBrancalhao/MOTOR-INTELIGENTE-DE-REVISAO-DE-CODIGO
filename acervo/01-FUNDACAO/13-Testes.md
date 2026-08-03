---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 13-Testes
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Testes

A governança descrita neste volume é verificada pela suíte `ferramentas/tests/test_contrato.py`
e `ferramentas/tests/test_validar.py` (nomes ilustrativos do papel; ver o motor para os arquivos
exatos), que cobrem o comportamento de `Contrato` e `validar_volume`/`validar_tudo`/
`validar_cross_refs` descrito em `11-Implementacao.md`.

## O que os testes do contrato provam

Que `ct.secoes_de("PROCESSO")` de fato omite `08-Modelos` e que `ct.secoes_de("BIBLIOTECA")` troca
`04-Arquitetura`/`05-Diagramas` por `04-Catalogo` — comportamento que, se quebrasse, faria todo
volume desses tipos reportar seção obrigatória ausente incorretamente ou, pior, deixar de exigir
uma seção que devia ser exigida. Que `ct.volumes` contém exatamente os ids declarados no
contrato — no acervo público (`acervo/`), travado em `01` a `42` por
`test_os_42_volumes_estao_declarados`, o teste que motivou a criação do acervo irmão
`acervo-controladoria` em vez de estender esse contrato.

## O que os testes do validador provam

Que uma violação de front-matter não impede a checagem de substância de rodar (as duas são
independentes, ambas reportadas na mesma passada) — importante porque um redator corrigindo uma
violação por vez, sem ver todas de uma vez, perderia tempo re-executando o validador a cada
correção isolada em vez de corrigir o lote completo reportado. Que `validar_cross_refs` detecta
ciclo em `depende_de` mesmo quando o ciclo passa por três ou mais volumes, não só pares diretos —
relevante porque um ciclo indireto (`A depende de B depende de C depende de A`) é mais fácil de
introduzir por acidente do que um ciclo direto óbvio.

## Prova por mutação, não só caminho feliz

O padrão de qualidade deste acervo, estabelecido em `07-PROMPT-ENGINE` e repetido em
`45-CONCILIACAO-CONTAS`, é escrever o teste para a falha específica que ele existe para evitar —
não só confirmar que o caminho correto funciona. Um teste que comprovadamente falha quando o BOM
é reintroduzido de propósito em um `_VOLUME.yml` de teste é mais forte do que um teste que só
confirma leitura de um arquivo já limpo, porque o primeiro prova que o gate detectaria a
regressão exata que já aconteceu uma vez.
