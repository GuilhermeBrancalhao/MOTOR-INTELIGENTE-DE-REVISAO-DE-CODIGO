# Testes

7 testes em `exemplos/54-integracao-erp/tests/test_normalizar.py`, todos
unitários (sem I/O de arquivo — constroem o `DataFrame` em memória):

- Conversão de formato brasileiro (com e sem separador de milhar)
- dtype `str` nativo do pandas recente (não é `object` clássico — bug real
  que escapava do filtro antigo)
- Coluna 100% vazia não vira candidata
- Desempate correto entre "% da Comissão" e "Valor Comiss"
- Mapeamento grava o valor certo em `VAL_COMISSAO`, não o percentual
- `validar()` trava quando a coluna de comissão fica vazia

Nenhum teste roda contra o CSV real (dado de cliente, fora do
versionamento) — todos constroem o cenário mínimo que reproduz o bug.
