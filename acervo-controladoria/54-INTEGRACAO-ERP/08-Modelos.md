---
volume: "54"
volume_nome: INTEGRACAO-ERP
tipo: ARQUITETURA
secao: 08-Modelos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Modelos de Dados

## O modelo `PROCESSADO` (36 colunas)

Documentado em `MODELO_UNIVERSAL.md`. Nasce de comparar o CSV nativo de um
banco (DIGIO) com a planilha `PROCESSADO` já conferida contra o banco real.
Campos que toda conciliação depende de ter certo:

- `NUM_PROPOSTA` — identificador único da operação, chave de casamento
  contra o sistema.
- `VAL_COMISSAO` — o valor pago pelo banco, não o percentual. É o campo que
  o bug real (ver `12-Exemplos.md`) escolhia errado.
- `PCL_COMISSAO` — o percentual, quando existe, guardado à parte — nunca
  confundido com `VAL_COMISSAO`.
- `DAT_CREDITO`, `VAL_BRUTO`, `VAL_BASE_COMISSAO`, `DSC_SITUACAO_BANCO` —
  completam o mínimo necessário para conciliar contra o previsto.

## Por que detecção automática, e não mapeamento manual por banco

Com 40+ bancos e sem API, mapear coluna a coluna por banco não escala, e
cada mudança de layout do banco quebraria o mapeamento manual em silêncio.
`normalizar.py` detecta a coluna certa por padrão de nome (`comiss`, `data`,
`prop`) mais validação de tipo/unicidade, e falha explicitamente
(`ValueError`) quando não acha comissão, data ou proposta — errar em
silêncio aqui é conciliação errada depois.

## Campos opcionais, presentes só quando o banco fornece

`VAL_BRUTO` e `VAL_BASE_COMISSAO` só são preenchidos quando `detectar_colunas()` encontra uma
coluna correspondente — nem todo banco expõe as duas. `DSC_SITUACAO_BANCO` e
`TIPO_COMISSAO_BANCO` seguem a mesma regra. As outras 26 colunas do modelo `PROCESSADO` (código
de loja, unidade de empresa, parcela diferida, entre outras) não são preenchidas por
`normalizar.py` hoje — ficam como colunas vazias no XLSX final, reservadas para quando alguma
fonte de dado real precisar delas, e documentadas em `MODELO_UNIVERSAL.md` como parte do
contrato de saída mesmo sem uso atual.
