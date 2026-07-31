# Volume 40 — Controladoria (rascunho)

Conhecimento de domínio extraído de um projeto real de conciliação de
comissão bancária, para reuso em futuros projetos de controladoria.
Não é um volume PRONTO — só existem duas peças reais, documentadas
como são, sem preencher lacuna com conteúdo inventado.

## O que existe

- **`MODELO_UNIVERSAL.md`** — mapeamento de um CSV nativo de banco
  (DIGIO) para um modelo padrão de 36 colunas (`PROCESSADO`), e a
  estratégia de detecção automática de coluna crítica (comissão, data,
  proposta) por padrão de nome, para generalizar a 40+ bancos sem API.
- **`normalizar.py`** — script que implementa essa detecção e validação.
  Testado contra CSV real de produção (DIGIO, janeiro/2026): a soma de
  comissão bateu contra o valor conferido à mão no arquivo original.
- **`ler_processado.py`** — script de inspeção usado para reconstruir
  o formato PROCESSADO a partir de planilhas já existentes.

## Lições que valem para qualquer banco, não só DIGIO

1. **CSV de banco brasileiro chega com vírgula decimal como texto**
   (`'886,39'`), não como número. Filtrar coluna candidata por
   `is_numeric_dtype` sem converter primeiro descarta a coluna certa e
   deixa sobrar só coluna vazia — e soma de coluna 100% vazia dá
   `0,00` no pandas (skipna por padrão), não `NaN`. Isso faz validação
   de soma "passar" comparando vazio com vazio.
2. **Nome de coluna não desambigua sozinho.** "% da Comissão" e "Valor
   Comiss" casam no mesmo padrão (`comiss`). Desempate por nome
   (percentual descarta, "valor" prioriza) e, na falta disso, por
   magnitude (percentual de comissão fica em 0-100).
3. **BOM (`\xef\xbb\xbf`) no início do CSV pode confundir a detecção
   de separador** se a primeira tentativa de leitura (separador
   default) não levantar erro mesmo lendo tudo como 1-2 colunas em vez
   de ~29. Bug identificado, ainda não corrigido em `normalizar.py`
   (`ler_csv()`) — falha reproduzida contra
   `DIGIO - 110075 01.07.csv`.

## Pendências conhecidas

- Detecção de separador falha em CSV com BOM UTF-8 (ver item 3 acima).
- Só o mapeamento de um banco (DIGIO) foi testado contra dado real.
  Os outros 39+ bancos/fintechs citados no projeto original ainda não
  passaram por este script.
- Sem integração com banco de dados (SQLite) nem com o "PREVISTO" do
  sistema de origem (OMIE) — a comparação banco-pago x previsto, que é
  o objetivo final da conciliação, não está implementada aqui.
