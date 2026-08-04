---
volume: "54"
volume_nome: INTEGRACAO-ERP
tipo: ARQUITETURA
secao: 13-Testes
status: RASCUNHO
atualizado_em: 2026-08-04
---

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

## Dívida conhecida: nenhuma suíte automática coleta estes testes

`acervo-controladoria/exemplos/` não é alcançado por `pytest` na raiz do motor (que só coleta o
pacote `ferramentas` de lá) nem por `pytest` de dentro de `acervo/` (que coleta o pacote dele).
Os 7 testes deste volume, junto com os 23 de `45-CONCILIACAO-CONTAS`, passam hoje porque alguém
rodou `python -m pytest acervo-controladoria/exemplos -q` manualmente — não por garantia mantida
pelo repositório, registrado como dívida em `acervo-controladoria/ESTADO.md`.

Cada um dos 7 testes existe porque reproduz um comportamento que já quebrou de verdade, não
porque cobre uma linha de código por obrigação — a lista de bugs reais em `10-Anti-Patterns.md`
tem correspondência direta com a lista de testes aqui, e essa correspondência é intencional: um
teste sem bug real por trás tende a virar manutenção sem valor, e um bug real sem teste
correspondente tende a voltar sem aviso na próxima mudança.
