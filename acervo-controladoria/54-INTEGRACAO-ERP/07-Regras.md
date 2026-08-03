# Regras

- CSV de banco brasileiro chega com vírgula decimal como texto (`'886,39'`),
  nunca como número — filtrar coluna candidata por `is_numeric_dtype` sem
  converter primeiro descarta a coluna certa e deixa sobrar só coluna vazia.
- Coluna 100% vazia (`NaN` em toda linha) nunca pode virar candidata: soma
  de coluna vazia dá `0,00` no pandas (skipna por padrão), não `NaN` — isso
  faz validação de soma "passar" comparando vazio com vazio.
- Nome de coluna sozinho não desambigua: "% da Comissão" e "Valor Comiss"
  casam no mesmo padrão (`comiss`). Desempate por nome (percentual descarta,
  "valor" prioriza) e, na falta disso, por magnitude (percentual de
  comissão fica em 0-100, valor pago não).
- Toda transformação precisa de validação que compare contra a origem —
  soma bater, contagem de linha bater, proposta sem duplicata — porque
  silêncio (coluna errada escolhida, valor `None`) é mais perigoso que erro
  explícito.
