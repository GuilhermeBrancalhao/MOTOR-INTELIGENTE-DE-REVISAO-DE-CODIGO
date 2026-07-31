---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-07-30
---

# Objetivos

Depois de ler este volume, o leitor consegue fazer o que a tabela abaixo descreve --
cada linha aponta para onde a capacidade se confere na prática, dentro dos três
módulos de `exemplos/31-testing/`.

| Objetivo | Onde se confere |
|---|---|
| Classificar um teste existente por camada da pirâmide (unitário, integração, contrato) e justificar a classificação pelo que o teste toca | `13-Testes.md`, seção "Classificação por camada" e tabela de contagem por arquivo |
| Escrever um teste que não depende do relógio real para exercitar código dependente de tempo | `exemplos/31-testing/tests/test_limitador_de_taxa.py`, que usa `RelogioFalso` e não executa nenhum `time.sleep` |
| Escolher entre um dublê fake e um stub, e justificar a escolha pelo tipo de asserção que o teste precisa fazer | `exemplos/31-testing/notificacao.py` e seus testes: `NotificadorFalso` (interação) contra `NotificadorQueFalha` (propagação de erro) |
| Escrever teste de fronteira e de classe de equivalência para uma função pura, cobrindo o caso em que a fórmula "confirma" uma entrada inválida | `exemplos/31-testing/tests/test_validador_cpf.py`, em particular `test_todos_os_digitos_iguais_sao_rejeitados_apesar_do_digito_bater` |
| Diagnosticar a causa mais provável de um teste instável (flaky) a partir do sintoma relatado | `10-Anti-Patterns.md`, item 1 (relógio real) e `07-Regras.md`, regras 1 e 2 |
| Decidir se uma falha de teste é regressão de comportamento ou acoplamento a detalhe de implementação | `10-Anti-Patterns.md`, item 4 ("Verificar interação quando só o estado devolvido importa") |
| Montar um checklist de revisão de pull request que reprova suíte sem asserção, suíte lenta sem justificativa e suíte com duplo de teste mal escolhido | `15-Checklist.md` |

## O que não é objetivo deste volume

Medir e relatar percentual de cobertura ao longo do tempo, decidir gate de release por
indicador agregado, e testar carga/performance sob volume -- as três coisas têm volume
próprio (`32-QUALITY`, `33-PERFORMANCE`) e citá-las aqui como objetivo duplicaria
conteúdo que outro volume é responsável por manter atualizado.
