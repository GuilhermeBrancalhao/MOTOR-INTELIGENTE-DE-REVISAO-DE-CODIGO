---
tecnologia: pytest
detectar: ["pytest.ini", "pyproject.toml", "tests/**/test_*.py"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-30
---

## Convenções
- Arquivo `test_*.py`, função `test_*`, um comportamento por teste.
- O nome do teste descreve o comportamento, não a função chamada: `test_arquivo_novo_e_livre`, não `test_classificar_2`.
- `tmp_path` para qualquer coisa que toque disco. Teste que escreve no repositório é teste quebrado.
- Tabela de casos com `@pytest.mark.parametrize` e `ids=` legíveis — o `id` é o que aparece quando falha.

## Armadilhas
- Teste que depende da ordem de execução de outro teste é falso-verde.
- `assert x` sem mensagem numa tabela parametrizada esconde qual caso quebrou; passe a mensagem.
- Mockar o que se está testando transforma o teste em tautologia.
- Ajustar o teste para o código passar destrói o único contrato que existe.

## Comandos
- Suíte: `python -m pytest -q`
- Verboso com os nomes dos casos: `python -m pytest -v`

## Checklist de review
- [ ] Cada teste falha se o comportamento que ele descreve for removido.
- [ ] Nenhum teste escreve fora de `tmp_path`.
- [ ] Casos parametrizados têm `ids` legíveis.
