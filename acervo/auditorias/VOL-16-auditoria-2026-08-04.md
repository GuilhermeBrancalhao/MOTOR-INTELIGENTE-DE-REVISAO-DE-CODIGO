# Auditoria — Volume 16 INTEGRATION

**Data:** 2026-08-04 | **Revisão:** 1 | **Auditor:** Opus 5 (redator: Opus 5, mesma sessão)

```
$ python -m ferramentas.validar 16
ok: volume 16 sem violacoes
$ python -m ferramentas.validar --cross-refs
ok: referencias cruzadas sem violacoes
$ python -m pytest exemplos/16-integration -q
6 passed
```

## Método

Verificadas as seis regras (I1-I6) contra `gateway.py`: I1 (versão verificada antes de consumir)
via `VersaoContrato.compativel_com` e o teste de major incompatível; I2 (idempotência) via
`cache_idempotencia` e o teste que conta chamadas reais ao executor injetado; I3 (retry sem
padrão implícito) via `__post_init__` de `PoliticaDeRetry` rejeitando timeout zero; I4 (falha
isolada) via `CircuitBreaker` e o teste de abertura após limiar de falhas consecutivas. Verificada
a fronteira com `22`-`25` em todas as seções que a mencionam (01, 07, 18) — mesmo critério prático
repetido sem contradição: "o outro lado pode mudar sem que eu saiba antes?".

## Notas por seção

| Seção | Nota | Observação |
|---|---|---|
| 01-Introducao | 8.5 | Contraste concreto (mesma mecânica de chamada, garantia diferente) antes da prescrição. |
| 02-Objetivos | 8 | Objetivos ligados diretamente às seis regras. |
| 03-Escopo | 8 | Fronteira com 22-25 explícita desde o escopo, não só nas referências cruzadas. |
| 04-Arquitetura | 8 | Gateway como ponto único de verificação, sem lógica de negócio própria. |
| 05-Diagramas | 8 | Diagrama de sequência e diagrama de estado do circuit breaker explicitamente conectados como duas vistas complementares (uma chamada vs. histórico de chamadas). |
| 06-Fluxogramas | 8 | Ordem da checagem de idempotência antes da chamada externa justificada por custo evitável, com paralelo explícito ao nó de circuito. |
| 07-Regras | 8.5 | Seis regras, cada uma com consequência prática nomeada; I5 delimita a fronteira em vez de prescrever comportamento. |
| 08-Modelos | 8 | `VersaoContrato` e `PoliticaDeRetry` como tipos que recusam estado inválido na construção. |
| 09-Boas-Praticas | 8 | Práticas amarradas às regras I1-I4. |
| 10-Anti-Patterns | 8 | Padrões evitáveis nomeados com a regra que cada um violaria. |
| 11-Implementacao | 8 | Cita o exemplo real e a integração testada por mutação. |
| 12-Exemplos | 8.5 | Quatro casos, incluindo o mais sutil (Caso 4: falha de rede sem duplicação, onde o consumidor nunca sabe que algo falhou). |
| 13-Testes | 8.5 | Prova por mutação nomeada nos docstrings dos testes (chave gerada de novo, versão incompatível aceita). |
| 14-Metricas | 8 | Métricas ligadas a I1-I4. |
| 15-Checklist | 8 | Checklist desmarcado, convenção correta. |
| 16-Roadmap | 8 | Três lacunas reais e específicas (descoberta automática de depreciação, fallback funcional sob circuito aberto, coordenação de versão entre múltiplos consumidores internos). |
| 17-Conclusao | 8 | Fecha reafirmando o critério de fronteira sem ambiguidade. |
| 18-Referencias-Cruzadas | 8.5 | Quatro vizinhos, incluindo a distinção com `17-SECURITY` (robustez da chamada vs. sensibilidade do dado que atravessa). |

media: 8.1

## Verificação do domínio neutro

```
$ grep -rli "concilia|controladoria|omie|sicoob" 16-INTEGRATION/ exemplos/16-integration/
(saida vazia)
```

## Veredicto

**Aprovado. Volume promovido a PRONTO.** Média 8.1, nenhuma seção abaixo de 6. Os quatro
critérios satisfeitos: gate estrutural verde, 6 testes passando, auditoria acima de 8,0, registro
no `CHANGELOG.md`.
