# Auditoria — Volume 04 REQUIREMENTS

**Data:** 2026-08-03
**Revisão:** 1
**Auditor:** Opus 5 (redator original: sessão de 2026-07-31, recuperado do histórico depois de
destruído pela geração em lote de 2026-08-02; exemplo executável escrito por Opus 5 em 2026-08-03)

```
$ python -m ferramentas.validar 04
ok: volume 04 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ python -m pytest exemplos/04-requirements -q
9 passed
```

## Contexto desta auditoria

Volume recuperado do histórico (destruído pela geração em lote de 2026-08-02, restaurado de
`ecd5fdd`). Trabalho de 2026-08-03: campo `escopo` preenchido, `exemplos/04-requirements/
requisito.py` escrito com a suíte, citado em `11-Implementacao.md`.

## Método

Verificadas as oito regras (Q1-Q8) contra o exemplo: Q1 (falsificabilidade) formalizada em
`CriterioDeAceite.verificar`; Q2 (lacuna sem resposta vira `Pendencia`, nunca `Requisito`) — os
dois são tipos distintos no módulo, estruturalmente impossível confundir um com o outro; Q3
(rastro para trás e para frente) verificado em `Requisito.__post_init__` (exige `lacuna_id` salvo
origem humana) e `Conjunto.sem_rastro_para_frente`; Q4 (identificador nunca reciclado) verificado
por teste que tenta readicionar id aposentado. Verificada a referência a `03-DISCOVERY` em
`11-Implementacao` — as três propriedades citadas (origem, trecho, decisão aberta com peso)
existem de fato naquele volume, conferido contra `03-DISCOVERY/08-Modelos.md`.

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 9 | Define requisito por falsificabilidade com exemplo do dano real (a disputa "rápido" na entrega, onde ninguém mentiu e a discussão é irresolúvel por falta de critério) — não é definição abstrata. |
| 02-Objetivos | 8.5 | Objetivos ligados às regras. |
| 03-Escopo | 8.5 | Fronteira com `03-DISCOVERY` (entrada) e outros volumes nomeada. |
| 04-Arquitetura | 8 | As cinco partes do processo. |
| 06-Fluxogramas | 8 | Fluxo de nascimento de um requisito, da lacuna à verificação. |
| 07-Regras | 9 | Oito regras, cada uma com consequência prática. Q8 (falha de verificação exige decidir entre defeito e requisito errado) é a mais sofisticada — nomeia os dois erros de reflexo possíveis e por que ambos são ruins. |
| 09-Boas-Praticas | 8.5 | Práticas ligadas às regras. |
| 10-Anti-Patterns | 8.5 | Sete anti-padrões. |
| 11-Implementacao | 9 | **Ganhou citação formal nesta auditoria.** A referência a `03-DISCOVERY` como fonte das três propriedades (origem, trecho, decisão aberta) é verificada e precisa — não repete o que aquele volume já construiu. |
| 12-Exemplos | 8.5 | Casos de requisito verificável e não verificável. |
| 13-Testes | 8.5 | Estratégia de teste do processo. |
| 14-Metricas | 8 | Métricas do processo, incluindo a leitura correta e não-óbvia: zero decisão aberta declarada é sinal de alguém ter preenchido, não de completude real. |
| 15-Checklist | 8.5 | Sem itens marcados `[x]` indevidamente. |
| 16-Roadmap | 8 | Lacunas declaradas. |
| 17-Conclusao | 9 | Fecha com a terceira ideia do volume — a decisão entre corrigir sistema ou corrigir requisito quando uma verificação falha, e por que decidir por reflexo é errado nos dois sentidos. |
| 18-Referencias-Cruzadas | 8.5 | Vizinhos nomeados, incluindo `03-DISCOVERY` como pré-requisito real (`depende_de: ["01", "03"]`). |

media: 8.5

## Problemas encontrados

Nenhum defeito de conteúdo. Mesma situação do volume 02: o único trabalho desta auditoria foi
fechar o critério 2, ausente porque o volume foi escrito antes deste ciclo de exemplos.

## Verificação do domínio neutro

```
$ grep -rin "concilia|controladoria|extrato|lancamento|contabil|omie|sicoob|boleto" 04-REQUIREMENTS/ exemplos/04-requirements/
(saida vazia)
```

**Limpo.**

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.5, nenhuma seção abaixo de 6. Os quatro
critérios estão satisfeitos: gate estrutural verde, 9 testes de `exemplos/04-requirements`
passando, auditoria acima de 8,0, registro no `CHANGELOG.md`.
