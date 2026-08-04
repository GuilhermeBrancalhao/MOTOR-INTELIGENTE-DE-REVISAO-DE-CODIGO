# Estado do acervo de Controladoria — medição de 2026-08-04

Este arquivo registra o resultado da **primeira validação já executada** sobre
`acervo-controladoria/`. Até esta data, nenhuma ferramenta, teste ou gate deste repositório
apontava para cá: os 12 volumes existiam sem que seu estado tivesse sido medido uma única vez.

O laudo abaixo é medição, não opinião. Todos os números são reproduzíveis pelos comandos citados.

## Como reproduzir

```
cd acervo
python -m ferramentas.validar --raiz ../acervo-controladoria --tudo
python -m ferramentas.validar --raiz ../acervo-controladoria 45
cd .. && python -m pytest acervo-controladoria/exemplos -q
```

## Resultado por volume

| Volume | Tipo (contrato) | Violações | Prosa | Exemplo | Estado real |
|---|---|---:|---:|---|---|
| 43-CONTABILIDADE-BASICA | ENGINE | 38 | 287 | — | esqueleto |
| 44-INDICADORES-KPI | PROCESSO | 36 | 283 | — | esqueleto |
| **45-CONCILIACAO-CONTAS** | **ENGINE** | **0** | **5.665** | **6 módulos** | **conforme** |
| 46-ORCAMENTO-FORECAST | PROCESSO | 36 | 279 | — | esqueleto |
| 47-FLUXO-CAIXA | PROCESSO | 36 | 279 | — | esqueleto |
| 48-CUSTOS-ABC | ENGINE | 38 | 275 | — | esqueleto |
| 49-ANALISE-FINANCEIRA | PROCESSO | 36 | 283 | — | esqueleto |
| 50-COMPLIANCE-FISCAL | GOVERNANCA | 38 | 283 | — | esqueleto |
| 51-RELATORIOS-GERENCIAIS | PROCESSO | 36 | 275 | — | esqueleto |
| 52-CONSOLIDACAO-CONTAS | ENGINE | 38 | 275 | — | esqueleto |
| 53-AUDITORIA-TRILHA | GOVERNANCA | 38 | 275 | — | esqueleto |
| 54-INTEGRACAO-ERP | ARQUITETURA | 39 | 1.344 | 2 módulos | parcial |
| **TOTAL** | | **420** | **9.803** | **30 testes** | |

## Leitura do resultado

**Um volume está conforme.** `45-CONCILIACAO-CONTAS` passa o gate estrutural com zero violações,
tem 5.665 palavras de prosa real e seis módulos de exemplo. É trabalho legítimo e completo pelo
critério 1 da Definição de PRONTO.

**Um volume está parcial.** `54-INTEGRACAO-ERP` tem 1.344 palavras e um exemplo real
(`normalizar.py`, normalização de CSV de banco/fintech sem API, testado contra dado real), mas
15 das 18 seções estão abaixo do mínimo de substância.

**Dez volumes são esqueletos.** Cerca de 280 palavras distribuídas em 18 seções — aproximadamente
15 palavras por seção. `43-CONTABILIDADE-BASICA/01-Introducao.md`, por exemplo, tem cinco linhas:
título, uma frase de escopo, o tipo e a frase "Volume essencial para Controladoria moderna". Não
há front-matter em nenhuma das 18 seções desses volumes.

Isto é exatamente a patologia que o `ROADMAP.md` do acervo principal registrou em 2026-08-03 —
"esqueletos gerados em lote, não conteúdo real" — repetida aqui por outra sessão.

## O curto-circuito que escondia 234 violações

A primeira medição acusou **186** violações. O número verdadeiro é **420**.

A diferença tem causa mecânica: seis volumes declaravam `tipo: PROCESSO` no `_VOLUME.yml`
enquanto o `contrato.json` os define como `ENGINE`, `GOVERNANCA` ou `ARQUITETURA`. O validador
reprova por `volume-tipo` e **para ali**, sem chegar a examinar as 18 seções. Um volume inteiro
de esqueletos aparecia como "1 violação".

Os stubs carimbaram `PROCESSO` em todos os 12 volumes indiscriminadamente — o gerador escreveu a
linha `Tipo: PROCESSO` até dentro do corpo de `01-Introducao.md`. O único volume escrito de
verdade, o `45`, declara `ENGINE` e casa com o contrato. Isso identifica com segurança qual lado
estava errado: o `contrato.json` é a fonte única de verdade, e os `_VOLUME.yml` dos stubs foram
alinhados a ele.

Um sétimo volume, o `54`, falhava por outra causa: `escopo:` usava bloco YAML `>`, que o
front-matter restrito da plataforma não aceita (só `chave: valor`). Colapsado para uma linha.

**É a mesma classe de defeito do bug de BOM UTF-8 de 2026-08-03**, que fazia 39 violações
aparentes esconderem 657 reais: um erro que reprova cedo mascara todo o resto. Vale como regra
geral para este repositório — sempre que um gate reprovar por metadado, desconfiar do total até
que o metadado esteja correto.

## Os 30 testes órfãos

`acervo-controladoria/exemplos/` tem 30 testes que passam, e **nenhuma suíte os coleta**:

| Suíte | Testes | Como roda |
|---|---:|---|
| motor | 449 | `pytest` na raiz |
| acervo | 789 | `pytest` de dentro de `acervo/` |
| controladoria | 30 | **nenhuma** — só manualmente |

A raiz coleta só a suíte do motor por decisão documentada no `pytest.ini` (dois pacotes
`ferramentas` colidem numa sessão só). O acervo roda de dentro de si. O acervo de controladoria
não foi contemplado por nenhum dos dois arranjos, então seus testes existem sem nunca serem
executados por rotina — passam hoje por coincidência de ninguém ter mexido no código, não por
verificação.

## O que falta para conformidade

Levar os 11 volumes não-conformes ao padrão do `45` significa escrever aproximadamente **55 mil
palavras** de doutrina contábil densa (contabilidade geral, KPI, orçamento, fluxo de caixa,
custeio ABC, análise financeira, compliance fiscal, relatórios gerenciais, consolidação, trilha
de auditoria, integração ERP), mais exemplo executável, testes e auditoria por volume.

**Esse trabalho não deveria ser feito por geração automática**, e a razão está na decisão
fundadora desta plataforma: perseguir a contagem de volumes força conteúdo genérico, o que
contradiz a regra "nunca gere conteúdo superficial". Os dez esqueletos existem precisamente
porque uma sessão anterior tentou o atalho. Repetir o atalho em escala maior produziria 55 mil
palavras de texto plausível e sem autoridade — pior que o esqueleto, porque o esqueleto ao menos
é honesto sobre estar vazio.

Contabilidade e controladoria são domínio de expertise do autor. A prosa desses volumes precisa
da autoridade dele, não de paráfrase de manual.

## Decisão pendente do autor

Registrado, não decidido:

1. **Incorporar** — `acervo-controladoria/` entra no contrato e nas ferramentas, com os 11
   volumes voltando a `RASCUNHO` declarado e sendo escritos ao longo do tempo, um a um, como
   foram os 42 do acervo principal.
2. **Separar** — vira repositório próprio, com contrato, ferramentas e suíte próprios.
3. **Reduzir ao que é real** — preservar `45` e `54`, que são trabalho legítimo, e remover os dez
   esqueletos até que haja intenção concreta de escrevê-los.

Enquanto não se decide, os 30 testes continuam fora de qualquer rotina e os dez esqueletos
continuam convivendo com conteúdo verificado — a ambiguidade que a Definição de PRONTO existe
para eliminar.
