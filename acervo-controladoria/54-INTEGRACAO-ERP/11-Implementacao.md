# Implementação

`normalizar.py` é uma classe, `Normalizador`, sem dependência externa além
de pandas/openpyxl. Fluxo: `ler_csv` → `detectar_colunas` →
`mapear_para_padrao` → `validar` → `salvar_xlsx` (ou tudo de uma vez via
`executar`).

<!-- exemplo: exemplos/54-integracao-erp/normalizar.py -->

## `_para_numerico` — o conversor que faltava

Converte texto em formato brasileiro (ponto de milhar, vírgula decimal)
para número: tenta primeiro o formato direto (caso já venha com ponto
decimal) e só então aplica a troca de separador — decisão por coluna
inteira, não por valor isolado, porque uma coluna real é consistente no
próprio formato.

## `_coluna_numerica_candidata` — filtro contra coluna vazia

Só aceita como candidata uma coluna com `.notna().any()`. Sem isso, uma
coluna 100% `NaN` com dtype numérico (comum quando o banco não preenche um
campo naquele arquivo) passava no `is_numeric_dtype` antigo e virava
candidata "válida" — cuja soma vazia (`0,00`) validava contra si mesma.

## `_escolher_valor_comissao` — desempate quando duas colunas casam

Critério em cascata: (1) nome com `%`/`pcl`/`taxa` descarta; (2) nome com
`valor`/`vl` prioriza; (3) na falta de nome decisivo, magnitude —
percentual de comissão fica em 0-100, valor pago não. Ver
`test_escolhe_valor_comissao_e_nao_o_percentual`.

## `validar` — guarda contra o falso-positivo de coluna vazia

Antes de comparar soma, checa se `VAL_COMISSAO` ficou 100% vazio e trava
explicitamente — sem isso, `0,00 == 0,00` "validava" uma comissão que não
existe. Ver `test_validar_trava_se_coluna_de_comissao_ficar_vazia`.
