# Auditoria — Volume 06 ENTERPRISE-ARCHITECTURE

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 06
ok: volume 06 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/06-enterprise-architecture -q
7 passed
```

## Método

Verificadas as seis regras (E1-E6) contra `inventario.py`: E1 (dependência obrigatória) via
`__post_init__` de `Sistema`; E2 (decisão sempre com consequência nomeada) via `__post_init__`
de `DecisaoDePortfolio`; E3 (custo agregado é soma, não maior isolado) provado por teste com
três sistemas de dois fornecedores; E5 (duplicação por categoria) provado com par positivo e
negativo. Verificada a coerência da fronteira com `02-CORE` (interna vs. portfólio) em todas as
seções que a mencionam — sem contradição entre elas.

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8.5 | Sintoma concreto (dependência de fornecedor não decidida) antes da prescrição. |
| 02-Objetivos | 8 | Cinco objetivos ligados às regras. |
| 03-Escopo | 8.5 | Quatro fronteiras nomeadas, incluindo a mais fácil de confundir (30-AI-GOVERNANCE). |
| 04-Arquitetura | 8 | Componente central (inventário) explicitamente passivo — não decide, só torna visível. |
| 05-Diagramas | 8 | Reaproveita a mesma estrutura de contagem para concentração e duplicação, com a diferença de implicação explicada. |
| 06-Fluxogramas | 8 | O nó de filtro (`B`) evita revisão de portfólio desnecessária; a propriedade de "decisão nunca desacompanhada do fato" é a observação mais forte. |
| 07-Regras | 8.5 | Seis regras com consequência prática cada. |
| 08-Modelos | 8 | Justifica a ausência de campo de aprovação embutido com o argumento de E6. |
| 09-Boas-Praticas | 8 | Cinco práticas. |
| 10-Anti-Patterns | 8.5 | Cinco padrões, incluindo o mais provável na prática (exigir aprovação de portfólio para tudo). |
| 11-Implementacao | 8.5 | Cita o exemplo e a integração real com `16-INTEGRATION`. |
| 12-Exemplos | 8.5 | Três casos, incluindo veto legítimo (Caso 2) e duplicação descoberta tarde (Caso 3). |
| 13-Testes | 8 | Prova por mutação nomeada (soma vs. maior isolado). |
| 14-Metricas | 8 | Quatro métricas, incluindo uma sobre fadiga de sinal (paralelo com 21-OBSERVABILITY). |
| 15-Checklist | 8 | Oito itens desmarcados, convenção correta desde a escrita. |
| 16-Roadmap | 8 | Três lacunas reais (descomissionamento, verificação cruzada, critério de veto). |
| 17-Conclusao | 8.5 | Fecha com a distinção mais importante do volume dita sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, fronteira com 02-CORE explícita. |

media: 8.2

## Verificação do domínio neutro

```
$ grep -rin "concilia|controladoria|omie|sicoob" 06-ENTERPRISE-ARCHITECTURE/ exemplos/06-enterprise-architecture/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.2, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 7 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
