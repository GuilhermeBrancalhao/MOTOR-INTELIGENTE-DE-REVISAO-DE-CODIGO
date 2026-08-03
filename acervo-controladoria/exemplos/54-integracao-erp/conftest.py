"""Poe normalizar.py no caminho de import da suite.

Mesmo motivo do `conftest.py` de `exemplos/45-conciliacao-contas`: duas pastas
`exemplos/<vol>/tests/` sem `__init__.py` importam cada arquivo de teste pelo
nome-base, unico no acervo, e isso evita a colisao de nome de pacote `tests`
entre pastas de exemplos diferentes.
"""
import sys
from pathlib import Path

_AQUI = str(Path(__file__).parent)
if _AQUI not in sys.path:
    sys.path.insert(0, _AQUI)
