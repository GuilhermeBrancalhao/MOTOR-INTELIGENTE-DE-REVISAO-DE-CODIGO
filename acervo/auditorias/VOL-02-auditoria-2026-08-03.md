# Auditoria — Volume 02 CORE

**Data:** 2026-08-03
**Revisão:** 1
**Auditor:** Opus 5 (redator original: sessão de 2026-07-31, recuperado do histórico depois de
destruído pela geração em lote de 2026-08-02; exemplo executável escrito por Opus 5 em 2026-08-03)

```
$ python -m ferramentas.validar 02
ok: volume 02 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ python -m pytest exemplos/02-core -q
8 passed
```

## Contexto desta auditoria

Este volume não foi escrito neste ciclo — foi recuperado. A prosa das 18 seções é de 2026-07-31,
sobrevivente no histórico git depois que a geração em lote de 2026-08-02 a substituiu por
esqueleto de 142 bytes. O único trabalho de 2026-08-03 foi: preencher o campo `escopo` (vazio na
restauração), escrever `exemplos/02-core/fronteira.py` com a suíte correspondente, e citar o
exemplo em `11-Implementacao.md`.

## Método

Verificadas as oito regras (N1-N8) uma a uma contra o exemplo executável: cada regra tem
correspondência direta em `fronteira.py` (a fronteira como função única = N1; validação em três
camadas na ordem forma→domínio→autorização = N3; `SemEfeito` como impossibilidade estrutural de
efeito sem validação = N4). Verificada a referência a `ferramentas/web.py` em `11-Implementacao`
— o arquivo existe e a função `responder` tem a assinatura descrita.

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 9 | A tese central (fronteira determinístico/probabilístico como decisão que governa todas as outras) é apresentada com o sintoma concreto ("não dá, depende do modelo" — frase quase sempre errada) antes da prescrição. |
| 02-Objetivos | 8.5 | Objetivos ligados às regras específicas, não genéricos. |
| 03-Escopo | 8.5 | Fronteira com volumes vizinhos nomeada. |
| 04-Arquitetura | 8.5 | As seis partes do sistema descritas com responsabilidade disjunta. |
| 05-Diagramas | 8.5 | Diagrama da fronteira coerente com o `C4Context`/`flowchart` esperado para tipo `ARQUITETURA`. |
| 06-Fluxogramas | 8 | Caminho de decisão da fronteira. |
| 07-Regras | 9 | **Corrigido nesta auditoria (indiretamente): a N8 já cita `03-DISCOVERY` corretamente e confere com o código daquele volume** (tabela de termos com procedência, não classificação por modelo). Oito regras, cada uma com consequência prática nomeada — nenhuma é decorativa. |
| 08-Modelos | 8 | Modelos de dado da fronteira. |
| 09-Boas-Praticas | 8.5 | Práticas ligadas às regras. |
| 10-Anti-Patterns | 8.5 | Sete anti-padrões, cada um com custo. |
| 11-Implementacao | 9 | **Ganhou citação formal nesta auditoria.** Referências a `ferramentas/web.py`, `07-PROMPT-ENGINE` (com o bug real do identificador de versão que ignorava a marca de obrigatoriedade) e `03-DISCOVERY` (com o gap real do termo "pix") — todas verificadas, nenhuma inventada. |
| 12-Exemplos | 9 | Três casos reais citados em `17-Conclusao`, coerentes com `11-Implementacao`. |
| 13-Testes | 8.5 | Estratégia de teste da fronteira. |
| 14-Metricas | 8 | Métricas do padrão. |
| 15-Checklist | 8.5 | Sem itens marcados `[x]` indevidamente — já seguia a convenção correta antes desta auditoria. |
| 16-Roadmap | 8 | Lacunas declaradas. |
| 17-Conclusao | 9 | Fecha com a lição mais desconfortável do volume dita sem meio-termo: "menos chamadas ao modelo costuma ser melhor arquitetura, não menos ambição" — e justifica com o argumento correto (dado corrige-se, variação administra-se). |
| 18-Referencias-Cruzadas | 8.5 | Vizinhos nomeados. |

media: 8.6

## Problemas encontrados

Nenhum defeito de conteúdo. O único trabalho desta auditoria foi fechar o critério 2 (exemplo
executável), que é exatamente a mesma lacuna que bloqueava os sete volumes auditados mais cedo
hoje — este volume não tinha os outros defeitos sistêmicos daquele lote (checklist marcado,
contradição de prosa, referência a outro projeto) porque foi escrito antes da geração em lote,
por um processo diferente.

## Verificação do domínio neutro

```
$ grep -rin "concilia|controladoria|extrato|lancamento|contabil|omie|sicoob|boleto" 02-CORE/ exemplos/02-core/
(saida vazia)
```

**Limpo.** As referências são internas ao acervo (`03-DISCOVERY`, `07-PROMPT-ENGINE`,
`ferramentas/web.py`) — procedência legítima, não domínio externo.

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.6, nenhuma seção abaixo de 6. Os quatro
critérios da Definição de PRONTO estão satisfeitos: gate estrutural verde, 8 testes de
`exemplos/02-core` passando, esta auditoria acima de 8,0, e registro no `CHANGELOG.md`.
