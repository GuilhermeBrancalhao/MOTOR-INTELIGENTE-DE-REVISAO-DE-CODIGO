"""Cobre o bug real encontrado ao rodar normalizar.py contra um CSV de
producao (DIGIO, janeiro/2026): duas colunas do banco casam com o padrao
"comiss" no nome -- "% da Comissao" e "Valor Comiss" -- e a versao antiga
pegava a primeira que aparecesse no CSV, escolhendo o percentual.

A causa raiz era mais funda: toda coluna monetaria de banco brasileiro
chega como texto com virgula decimal ('886,39'), entao o filtro antigo
por `is_numeric_dtype` excluia essas colunas dos candidatos e so sobravam
colunas numericas vazias (100% NaN) -- cuja soma, por padrao do pandas
(skipna), da 0,00 e nao NaN. Isso fazia a validacao de soma "passar"
comparando vazio com vazio.
"""
import pandas as pd

from normalizar import Normalizador


def _normalizador_com(df: pd.DataFrame) -> Normalizador:
    n = Normalizador("arquivo-fake.csv", "BANCO-TESTE")
    n.df_original = df
    return n


def test_para_numerico_converte_formato_brasileiro():
    serie = pd.Series(["886,39", "109,48", "1.528,36"])
    convertida = Normalizador._para_numerico(serie)
    assert convertida.tolist() == [886.39, 109.48, 1528.36]


def test_para_numerico_preserva_coluna_ja_numerica():
    serie = pd.Series([886.39, 109.48])
    convertida = Normalizador._para_numerico(serie)
    assert convertida.tolist() == [886.39, 109.48]


def test_para_numerico_no_dtype_str_nativo_do_pandas_recente():
    """dtype 'str' (nao o 'object' classico) escapava de um filtro
    `dtype == object` e a coluna virava all-NaN por engano -- bug real
    reproduzido rodando contra CSV do DIGIO nesta maquina."""
    serie = pd.Series(["886,39", "109,48"], dtype="str")
    convertida = Normalizador._para_numerico(serie)
    assert convertida.notna().all()
    assert convertida.tolist() == [886.39, 109.48]


def test_coluna_100_por_cento_vazia_nao_vira_candidata():
    df = pd.DataFrame({"Valor Comiss": ["886,39", "109,48"]})
    n = _normalizador_com(df)
    assert n._coluna_numerica_candidata("Valor Comiss") is not None

    df_vazio = pd.DataFrame({"Comissionado Origem Reat.": [float("nan"), float("nan")]})
    n_vazio = _normalizador_com(df_vazio)
    assert n_vazio._coluna_numerica_candidata("Comissionado Origem Reat.") is None


def test_escolhe_valor_comissao_e_nao_o_percentual():
    """Reproduz o caso real do DIGIO: '% da Comissao' e 'Valor Comiss'
    casam no mesmo padrao de nome. A escolha certa e a que tem 'valor'
    no nome, nao a primeira que aparece na ordem das colunas."""
    df = pd.DataFrame({
        "Oper.": [500003141261, 500003141425],
        "Data Base": ["02/01/2026", "02/01/2026"],
        "% da Comissao": [3.0, 3.0],
        "Valor Comiss": ["886,39", "109,48"],
    })
    n = _normalizador_com(df)
    n.detectar_colunas()

    assert n.deteccoes["comissao"] == "Valor Comiss"
    assert n.deteccoes["pcl_comissao"] == "% da Comissao"


def test_mapeamento_grava_valor_correto_nao_o_percentual():
    df = pd.DataFrame({
        "Oper.": [500003141261, 500003141425],
        "Data Base": ["02/01/2026", "02/01/2026"],
        "% da Comissao": [3.0, 3.0],
        "Valor Comiss": ["886,39", "109,48"],
    })
    n = _normalizador_com(df)
    n.detectar_colunas()
    n.mapear_para_padrao()

    assert n.df_processado["VAL_COMISSAO"].tolist() == [886.39, 109.48]
    assert n.df_processado["PCL_COMISSAO"].tolist() == [3.0, 3.0]


def test_validar_trava_se_coluna_de_comissao_ficar_vazia():
    """Insurance direta contra o falso-positivo real: soma de coluna
    100% NaN da 0,00 no pandas (skipna por padrao), nao NaN -- sem este
    guard, 0,00 contra 0,00 'validaria' uma comissao que nao existe."""
    df = pd.DataFrame({"Oper.": [1, 2], "Data Base": ["02/01/2026", "02/01/2026"]})
    n = _normalizador_com(df)
    n.deteccoes = {"comissao": "Fantasma", "pcl_comissao": None, "proposta": "Oper."}
    n._series_numericas["Fantasma"] = pd.Series([float("nan"), float("nan")])
    n.df_processado = pd.DataFrame({
        "NUM_PROPOSTA": [1, 2],
        "VAL_COMISSAO": [float("nan"), float("nan")],
    })

    assert n.validar() is False
