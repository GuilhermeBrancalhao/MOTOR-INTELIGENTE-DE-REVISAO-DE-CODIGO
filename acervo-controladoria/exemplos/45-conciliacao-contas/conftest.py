"""Poe os modulos deste exemplo no caminho de import da suite.

Mesmo motivo do `conftest.py` de `acervo/exemplos/03-discovery`: duas pastas
`exemplos/<vol>/tests/` sem `__init__.py` importam cada arquivo de teste pelo
nome-base, unico no acervo, e isso evita a colisao de nome de pacote `tests`
entre pastas de exemplos diferentes. O preco e que a pasta do exemplo nao
entra no caminho de import sozinha, e este arquivo paga esse preco.
"""
import sys
from pathlib import Path

_AQUI = str(Path(__file__).parent)
if _AQUI not in sys.path:
    sys.path.insert(0, _AQUI)
