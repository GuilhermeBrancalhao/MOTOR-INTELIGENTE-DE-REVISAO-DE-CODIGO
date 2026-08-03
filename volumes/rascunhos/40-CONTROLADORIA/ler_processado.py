#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

xlsx_path = r"Z:\COMISSÃO\DOCS - WORK BANK 2026\DIGIO\07 - JULHO\PROCESSADOS\DIGIO - 110075 01.07 - EDITADO.xlsx"

try:
    df = pd.read_excel(xlsx_path, sheet_name=0, engine="openpyxl")
    print(f"Colunas ({len(df.columns)}):")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")

    print(f"\nPrimeiras 5 linhas:")
    print(df.head(5).to_string())

    print(f"\nDimensões: {df.shape}")
    print(f"\nTipos de dados:")
    print(df.dtypes)

except Exception as e:
    print(f"Erro: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
