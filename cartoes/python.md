---
tecnologia: python
detectar: ["pyproject.toml", "setup.py", "requirements*.txt", "**/*.py"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-30
---

## Convenções
- PEP 8; nomes em `snake_case`; classes em `CapWords`.
- `from __future__ import annotations` no topo de módulo que usa anotação de tipo moderna.
- Caminho de arquivo com `pathlib.Path`, nunca por concatenação de string.
- Escrita de arquivo sempre com `encoding="utf-8"` explícito — no Windows o default não é UTF-8.

## Armadilhas
- Argumento default mutável (`def f(x=[])`) é compartilhado entre chamadas.
- `except Exception` sem re-levantar engole o erro; só é aceitável quando a falha segura é o requisito, e aí precisa de comentário dizendo isso.
- `os.replace` é atômico; `shutil.move` entre volumes diferentes não é.
- Comparar float com `==` falha; use `math.isclose`.

## Comandos
- Suíte: `python -m pytest -q`
- Um teste: `python -m pytest caminho/test_x.py::test_y -v`

## Checklist de review
- [ ] Toda exceção capturada é tratada ou re-levantada.
- [ ] Nenhum caminho de arquivo montado por concatenação.
- [ ] Nenhuma escrita de arquivo sem `encoding`.
- [ ] Funções com uma responsabilidade; arquivo grande foi dividido.
