# Auditoria — Volume 05 BUSINESS

**Data:** 2026-08-04
**Revisão:** 1
**Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 05
ok: volume 05 sem violacoes

$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes

$ python -m pytest exemplos/05-business -q
8 passed
```

## Ressalva de independência

Auditor e redator são o mesmo modelo, mesma sessão — independência mínima, mais fraca que a dos
sete volumes auditados em 2026-08-03 (onde ao menos o redator inicial havia sido outro modelo).
A contramedida é a mesma: verificar por execução tudo que é verificável, e não confiar em leitura
de prosa isolada.

## Método

Verificadas as seis regras (B1-B6) contra `exemplos/05-business/objetivo.py`: B1 (uma única
classificação de autoridade) é garantida pelo próprio tipo, não por validação em runtime —
conferido que não há checagem redundante que sugerisse dúvida sobre essa garantia. B2 e B3
verificadas por teste que injeta objetivo sem critério e stakeholder sem autoridade `DECIDE`,
respectivamente. B4 verificada pelo teste que produz dois `DECIDE` com objetivos distintos e
confirma que o sistema registra sem escolher lado.

## Notas por seção

| Seção | Nota | Justificativa |
|---|---|---|
| 01-Introducao | 8.5 | Abre com o sintoma concreto ("stakeholders foram consultados" não distingue interesse de autoridade) antes da definição — mesmo padrão que funcionou em `02-CORE`. |
| 02-Objetivos | 8 | Cinco objetivos ligados às regras. |
| 03-Escopo | 8.5 | Quatro fronteiras nomeadas, incluindo a mais fácil de violar na prática (preferência técnica disfarçada de objetivo). |
| 04-Arquitetura | 8 | Justifica a ordem estrita das três etapas com o custo de invertê-las. |
| 05-Diagramas | 8 | Mindmap de autoridade + flowchart do teste de falsificabilidade. Precisou de duas expansões para atingir o mínimo — conteúdo acrescentado é substantivo, não enchimento. |
| 06-Fluxogramas | 8 | O fluxo completo com os dois pontos de travamento nomeados; a nota final sobre por que o ciclo de hierarquia vem antes de capturar objetivo é a observação mais forte da seção. |
| 07-Regras | 8.5 | Seis regras, todas com consequência prática nomeada. |
| 09-Boas-Praticas | 8 | Cinco práticas, incluindo a revalidação de autoridade entre fases — ponto que nenhum outro volume deste padrão tinha coberto ainda. |
| 10-Anti-Patterns | 8.5 | Cinco padrões, incluindo o mais sutil: confundir facilidade de medição com relevância. |
| 11-Implementacao | 8.5 | Cita o exemplo e explica a integração real com `03-DISCOVERY`/`04-REQUIREMENTS` — que campo vira entrada de qual volume vizinho. |
| 12-Exemplos | 8.5 | Três casos, com o Caso 3 mostrando a devolução para refinamento de forma concreta (a resposta inicial não observável, a resposta corrigida). |
| 13-Testes | 8 | Declara honestamente o que a suíte não cobre (equivalência semântica entre objetivos parecidos) em vez de fingir cobertura completa. |
| 14-Metricas | 8 | Quatro métricas, incluindo uma que mede o custo real de pular o processo (retrabalho em `04-REQUIREMENTS` atribuível a objetivo mal capturado). |
| 15-Checklist | 8 | Oito itens desmarcados, seguindo a convenção correta desde a escrita — não precisou de correção nesta auditoria. |
| 16-Roadmap | 8 | Três lacunas reais, incluindo a mais honesta: não há mecanismo de desempate quando não existe hierarquia natural entre dois `DECIDE`. |
| 17-Conclusao | 8.5 | Fecha com a formulação mais precisa do valor do processo: ele não elimina discordância, move o momento em que ela aparece para o ponto mais barato. |
| 18-Referencias-Cruzadas | 8 | Fronteira com `02-CORE` explicitamente marcada como não-relação, o que evita a confusão mais provável (objetivo de negócio virando prescrição técnica). |

media: 8.2

## Problemas encontrados

Nenhum defeito de conteúdo sobrevivente. Durante a escrita, `01-Introducao.md` não foi salvo na
primeira tentativa (erro de ferramenta, não de conteúdo) e ficou como esqueleto até o gate
apontar — corrigido antes desta auditoria fechar.

## Verificação do domínio neutro

```
$ grep -rin "concilia|controladoria|extrato|lancamento|contabil|omie|sicoob|boleto" 05-BUSINESS/ exemplos/05-business/
(saida vazia)
```

**Limpo.**

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.2, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 8 testes de `exemplos/05-business` passando,
auditoria acima de 8,0, registro no `CHANGELOG.md`.
