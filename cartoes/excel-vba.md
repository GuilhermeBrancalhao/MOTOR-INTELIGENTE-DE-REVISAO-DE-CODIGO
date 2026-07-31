---
tecnologia: excel-vba
detectar: ["*.bas", "*.cls", "*.frm", "*.xlsm"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-31
---

## Convenções
- `Option Explicit` no topo de todo módulo — sem isso, uma variável com nome digitado errado vira um `Variant` novo e vazio em silêncio, em vez de erro de compilação.
- Ler/escrever uma faixa de células de uma vez num array (`rng.Value2`), nunca célula a célula dentro de um loop.
- `Application.ScreenUpdating = False` (e `Calculation = xlCalculationManual` quando a planilha recalcula muito) no início da macro, restaurados no fim **e** no handler de erro — se a macro estoura exceção antes de restaurar, o Excel fica com a tela congelada/sem recalcular para o usuário.
- Referência de objeto totalmente qualificada (`ThisWorkbook.Worksheets("X").Range("A1")`), nunca depender do que está `ActiveSheet`/`ActiveWorkbook` no momento.

## Armadilhas
- `.Select` + `.Activate` seguidos de operação no objeto ativo é lento (cada seleção redesenha a tela) e quebra se o usuário clicar em outra célula enquanto a macro roda; opere direto no objeto (`rng.Value2 = x`) sem selecionar.
- `.Value2` não converte para os tipos `Currency` e `Date` — devolve o número puro (`Double`); é mais rápido e mais preciso que `.Value` para cálculo, mas quem espera um `Date` de volta recebe um número de série.
- Erro não tratado (`On Error GoTo` ausente) deixa `ScreenUpdating`/`Calculation` no estado alterado e a macro simplesmente para no meio, sem o usuário saber até onde ela chegou.
- Fechar o workbook/aplicação de automação (criada via `CreateObject("Excel.Application")`) sem `.Quit` e sem liberar a referência deixa o processo `EXCEL.EXE` pendurado em segundo plano.

## Checklist de review
- [ ] Todo módulo começa com `Option Explicit`.
- [ ] Nenhum `.Select`/`.Activate` antes de operar numa célula ou range.
- [ ] `ScreenUpdating`/`Calculation` restaurados também no handler de erro, não só no fim do caminho feliz.
- [ ] Leitura/escrita de range em bloco (array), não célula a célula em loop.
