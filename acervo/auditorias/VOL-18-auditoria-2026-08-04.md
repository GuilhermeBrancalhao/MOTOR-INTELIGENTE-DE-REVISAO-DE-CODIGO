# Auditoria — Volume 18 DEVSECOPS

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 18
ok: volume 18 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/18-devsecops -q
6 passed
```

## Método

Verificadas as seis regras (D1-D6) contra `gate.py`: D1/D6 (controle sem automação vira lacuna,
não aprovação) via `Controle.tem_automacao` e o teste dedicado; D2 (bloqueio por padrão) via
`GateDeSeguranca.avaliar` e o teste de falha sem waiver; D3 (waiver expirado tratado como
inexistente) via `Waiver.esta_ativo` e o teste que avança a data de avaliação. Verificada a
fronteira com `17-SECURITY` (política vs. processo de enforcement) em todas as seções que a
mencionam — consistente com a distinção do `ROADMAP.md` (grupo 3: "o que precisa ser verdade"
contra "como se verifica continuamente").

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8 | Contraste concreto entre auditoria periódica e prevenção no momento da mudança. |
| 02-Objetivos | 8 | Os cinco objetivos explicitados como cadeia dependente, não lista solta. |
| 03-Escopo | 8.5 | Três fronteiras nomeadas (17, 31/32, 19), incluindo a mais fácil de confundir (teste de segurança é teste, não categoria separada). |
| 04-Arquitetura | 8 | Gate deliberadamente não executa verificação, só consolida — separação justificada. |
| 05-Diagramas | 8 | Ausência proposital de caminho "aprovado sem check" explicada. |
| 06-Fluxogramas | 8 | Distinção entre lacuna (não bloqueia sozinha) e falha (bloqueia) justificada contra um incentivo perverso real. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática; D3 é a mais forte do volume. |
| 09-Boas-Praticas | 8 | Cinco práticas, incluindo prazo curto renovável como preferência deliberada. |
| 10-Anti-Patterns | 8 | Cinco padrões, incluindo o mais fácil de cometer sem perceber (motivo de waiver copiado). |
| 11-Implementacao | 8 | Justifica a escolha de comparação lexicográfica de data em vez de tipo dedicado. |
| 12-Exemplos | 8 | Quatro casos cobrindo as três saídas possíveis mais a transição de expiração do waiver. |
| 13-Testes | 8.5 | Prova por mutação nomeada em cada docstring; nota a ausência de dependência de tempo real. |
| 14-Metricas | 8 | Quatro métricas, incluindo o alerta de queda súbita sem melhoria correspondente. |
| 15-Checklist | 8 | Nove itens desmarcados, convenção correta desde a escrita. |
| 16-Roadmap | 8 | Três lacunas reais e específicas (notificação de expiração, métrica de idade da lacuna, revisão periódica automatizada). |
| 17-Conclusao | 8.5 | Fecha nomeando o ponto mais fácil de negligenciar (expiração do waiver) sem meio-termo. |
| 18-Referencias-Cruzadas | 8 | Quatro vizinhos, `depende_de: ["17"]` justificado no próprio texto. |

media: 8.1

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 18-DEVSECOPS/ exemplos/18-devsecops/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 6 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
