# Aceite da Fase 4 — modo PROGRAMA

**Data:** 2026-08-05
**Spec:** `docs/specs/2026-08-05-engine-fase-4-programa.md`

Este documento e o registro do aceite. Ele nao escreve produto — decide, com saida real
colada, se a Fase 4 esta pronta. As saidas abaixo foram rodadas nesta data, neste
repositorio, num diretorio-cobaia limpo, e coladas sem edicao de conteudo (so a
formatacao em bloco de codigo).

Rodadas com `PYTHONUTF8=1` para a acentuacao sair legivel no console do Windows (cp1252
mostra mojibake sem isso). O comportamento e identico com ou sem a variavel — ela so
afeta a exibicao.

> **Nota sobre `exit=`.** Os codigos de saida colados foram medidos sem canalizar a saida
> por outro comando. Num `cmd | head`, `$?` e o codigo do `head`, nao o do comando — essa
> armadilha ja produziu uma medicao errada neste repositorio antes.

---

## Suite

```
python -m pytest -q
507 passed
```

Eram 478 antes da Fase 4; os 29 testes novos de `ferramentas/tests/test_programa.py`
entraram sem quebrar nenhum existente.

---

## Prova por mutacao

Testes que nunca ficaram vermelhos sao hipoteses. Quatro mutacoes foram aplicadas ao
`programa.py` original, uma de cada vez, e a suite foi rodada em cada uma:

| Mutacao aplicada | Resultado |
|---|---|
| `registrar_aceite` sempre marca `CONCLUIDO` | **2 falhas** (A2) |
| `_recusar_ciclo_no_grafo` removido de `validar_plano` | **2 falhas** (A3) |
| `propor_plano` vai direto para `EXECUCAO` (anula a porta P1) | **9 falhas** (A4) |
| `concluir` ignora o veredito do aceite de sistema | **1 falha** (A7) |

O original foi restaurado e as 29 voltaram a passar.

---

## Fluxo de ponta a ponta

### Passo 1 — abrir o programa
```
**PROGRAMA aberto:** 2026-08-05-1  ·  **Estado:** CONCEPCAO
**Objetivo:** plataforma de conciliacao bancaria multi-banco

Conduza a macro-DESCOBERTA e o PLANO_MESTRE. A decomposição precisa de um critério de aceite falsificável por ciclo, e de um aceite de sistema.
```

### Passo 2 — submeter e validar a decomposicao
```
**Plano-mestre registrado e validado** (DAG e critérios de aceite).
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** PLANO_MESTRE
**Objetivo:** plataforma de conciliacao bancaria multi-banco
**Ciclos:** 0/4 concluídos
  [ ] C1: ingestao e normalizacao de extratos CSV
  [ ] C2: motor de casamento com niveis de confianca  (depende de C1)
  [ ] C3: trilha auditavel imutavel  (depende de C1)
  [ ] C4: API e tela de revisao  (depende de C2, C3)

**Porta do plano-mestre.** Nada executa até o usuário rodar `programa aprovar`.
```

### Passo 3 — a porta trava a execucao (A4)
```
ENGINE: o programa está em PLANO_MESTRE; ciclos só ligam em EXECUCAO (o plano-mestre precisa ter sido aprovado)
exit=1
```

### Passo 4 — aprovar (so o usuario roda)
```
**Plano-mestre aprovado.** O programa entra em EXECUCAO.
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** EXECUCAO
**Objetivo:** plataforma de conciliacao bancaria multi-banco
**Ciclos:** 0/4 concluídos
  [ ] C1: ingestao e normalizacao de extratos CSV
  [ ] C2: motor de casamento com niveis de confianca  (depende de C1)
  [ ] C3: trilha auditavel imutavel  (depende de C1)
  [ ] C4: API e tela de revisao  (depende de C2, C3)
**Próximo ciclo elegível:** C1
```

### Passo 5 — encadeamento respeita dependencias (A1)
```
**Próximo ciclo:** C1 — ingestao e normalizacao de extratos CSV
**Aceite:** pytest tests/ingestao -q sai 0 com 3 bancos
-- apos C1 ok:
**Próximo ciclo:** C2 — motor de casamento com niveis de confianca
**Aceite:** pytest tests/casamento -q sai 0
```

### Passo 6 — aceite vermelho bloqueia dependentes (A2)
```
-- C3 reprovado; C4 depende de C2+C3:
ENGINE: nenhum ciclo elegível. Há ciclo REPROVADO bloqueando dependentes — use `programa reabrir <CICLO>`.
exit=1
```

### Passo 7 — aceite de sistema exige todos os ciclos (A7)
```
ENGINE: ACEITE_SISTEMA exige todos os ciclos CONCLUIDO; faltam: C3, C4
exit=1
```

### Passo 8 — reabrir, concluir, e aceite de sistema VERMELHO nao conclui (A7)
```
**Aceite de sistema REPROVOU.** O programa volta a EXECUCAO — nada é dado como concluído.
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** EXECUCAO
**Objetivo:** plataforma de conciliacao bancaria multi-banco
```

### Passo 9 — aceite de sistema VERDE conclui
```
**PROGRAMA CONCLUÍDO.** Aceite de sistema verde.
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** CONCLUIDO
**Objetivo:** plataforma de conciliacao bancaria multi-banco
**Ciclos:** 4/4 concluídos
```

### Passo 10 — durabilidade: processo novo, so o disco (A5)
```
**PROGRAMA:** 2026-08-05-1  ·  **Estado:** CONCLUIDO
**Objetivo:** plataforma de conciliacao bancaria multi-banco
**Ciclos:** 4/4 concluídos
  [x] C1: ingestao e normalizacao de extratos CSV
  [x] C2: motor de casamento com niveis de confianca  (depende de C1)
  [x] C3: trilha auditavel imutavel  (depende de C1)
  [x] C4: API e tela de revisao  (depende de C2, C3)
```

---

## Veredito

**Fase 4 aprovada.** Os oito casos de aceite da spec estao cobertos:

| Caso | Onde foi provado |
|---|---|
| A1 encadeamento respeita dependencias | Passo 5 + `test_encadeia_tres_ciclos_em_ordem_de_dependencia` |
| A2 aceite vermelho nao avanca | Passo 6 + mutacao 1 |
| A3 DAG validado na porta | mutacao 2 + 6 testes de `validar_plano` |
| A4 execucao exige aprovacao | Passo 3 + mutacao 3 |
| A5 sobrevive a sessao nova | Passo 10 (processo novo, so o disco) |
| A6 desvio e conjunto fechado | `test_desvio_com_motivo_livre_e_recusado` |
| A7 aceite de sistema | Passos 7, 8 e 9 + mutacao 4 |
| A8 grafo recusa transicao invalida | `test_transicao_fora_do_grafo_e_recusada` |

**O que este aceite NAO prova.** Que o ENGINE constroi um sistema complexo real de ponta
a ponta. Ele prova que a *maquina* do programa esta correta: encadeia, bloqueia, valida,
sobrevive e recusa concluir sem evidencia. A prova de capacidade e o passo 6 da spec — um
programa real, com ciclos reais, num projeto-cobaia. Ate la, a resposta continua sendo
"por construcao, nao por execucao".
