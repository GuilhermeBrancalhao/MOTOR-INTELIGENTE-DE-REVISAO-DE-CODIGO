---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 18-Referencias-Cruzadas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Referências Cruzadas

## Vizinhança de assunto

O campo `depende_de` está vazio no `_VOLUME.yml` — ver o comentário lá para o motivo. A
vizinhança real, em prosa:

| Volume vizinho | Relação |
|---|---|
| `43-CONTABILIDADE-BASICA` | Fornece o plano de contas e a categoria que a escrita final usa; este volume decide *se* escrever, o 43 decide *o quê* escrever |
| `53-AUDITORIA-TRILHA` | Generaliza o padrão que `trilha.py` implementa aqui como referência concreta |
| `54-INTEGRACAO-ERP` | Fornece os dados de entrada (`Movimento`, `TituloAberto`) já normalizados; este volume não sabe nada sobre formato de extrato ou autenticação de API |
| `44-INDICADORES-KPI`, `51-RELATORIOS-GERENCIAIS` | Consomem as métricas descritas em `14-Metricas.md` para apresentação |

## Links que resolvem hoje

- [`../00-INTRODUCAO/Convencoes.md`](../00-INTRODUCAO/Convencoes.md) — o contrato deste acervo e a Definição de PRONTO
- [`../exemplos/45-conciliacao-contas/ancora.py`](../exemplos/45-conciliacao-contas/ancora.py) — âncora de saldo
- [`../exemplos/45-conciliacao-contas/casamento.py`](../exemplos/45-conciliacao-contas/casamento.py) — casamento por título
- [`../exemplos/45-conciliacao-contas/confianca.py`](../exemplos/45-conciliacao-contas/confianca.py) — classificação de confiança
- [`../exemplos/45-conciliacao-contas/guarda.py`](../exemplos/45-conciliacao-contas/guarda.py) — guarda de duplicidade
- [`../exemplos/45-conciliacao-contas/trilha.py`](../exemplos/45-conciliacao-contas/trilha.py) — trilha de auditoria
- [`../exemplos/45-conciliacao-contas/tests/test_fluxo_completo.py`](../exemplos/45-conciliacao-contas/tests/test_fluxo_completo.py) — composição ponta-a-ponta

## Navegação interna

Para implementar contra o motor: `11-Implementacao.md` seguido de `12-Exemplos.md`. Para
entender as garantias: `07-Regras.md` e `10-Anti-Patterns.md`. Para estender: `03-Escopo.md` e
`16-Roadmap.md`, nessa ordem — a fronteira antes da extensão.
