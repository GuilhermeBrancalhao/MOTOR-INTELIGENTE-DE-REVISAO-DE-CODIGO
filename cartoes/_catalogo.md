# Catálogo de cartões

| Cartão | Papéis que carregam | Fase do ENGINE |
|---|---|---|
| `python` | arquiteto, implementador, revisor | 1 |
| `pytest` | arquiteto, implementador, testador, revisor | 1 |
| `ui-ux` | arquiteto, designer, implementador, revisor | 1 |
| `fastapi` | arquiteto, implementador, testador, revisor | 2 |
| `excel-vba` | arquiteto, implementador, revisor | 2 |
| `office-scripts` | arquiteto, implementador, revisor | 2 |
| `power-query` | arquiteto, implementador, revisor | 2 |
| `react` | arquiteto, designer, implementador, testador, revisor | 2 |
| `typescript` | arquiteto, implementador, testador, revisor | 2 |
| `postgresql` | arquiteto, implementador, revisor | 2 |
| `sqlite` | arquiteto, implementador, revisor | 2 |
| `mermaid` | arquiteto, documentador | 2 |

Elenco completo: 12 cartões. Os `papeis` de `pytest` e `ui-ux` foram revisados na Fase 2
(adicionado `testador` em `pytest` e `designer` em `ui-ux`, coerente com o que já valia para
os cartões novos de teste e de interface).

Na Fase 1 os cartões eram lidos diretamente pelos papéis. A partir da Fase 2, a detecção
automática de stack (`ferramentas/detectar.py`) varre o projeto hospedeiro e grava em
`estado.cartoes` a lista de tecnologias presentes; cada papel carrega só os cartões que o
listam em `papeis`.
