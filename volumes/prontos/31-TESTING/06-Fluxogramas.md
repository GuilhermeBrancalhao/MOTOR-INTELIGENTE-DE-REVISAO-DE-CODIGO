---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 06-Fluxogramas
status: PRONTO
atualizado_em: 2026-07-30
---

# Fluxogramas

## O caminho de decisão de `LimitadorDeTaxa.permitir`

```mermaid
flowchart TD
    A["permitir(custo)"] --> B{"custo <= 0?"}
    B -->|sim| C["levanta CustoInvalido"]
    B -->|nao| D["_reabastecer(): se decorrido > 0, fichas += decorrido x taxa, ate o teto da capacidade"]
    D --> E{"fichas >= custo?"}
    E -->|sim| F["fichas -= custo; devolve True"]
    E -->|nao| G["devolve False; fichas permanece inalterada"]
```

O fluxo corresponde linha a linha ao corpo de `permitir` em
`exemplos/31-testing/limitador_de_taxa.py`: a checagem de custo vem antes de qualquer
leitura do relógio, porque levantar por parâmetro inválido não deveria depender de
quanto tempo passou desde a última chamada. O ramo `G` é o que
`test_recusa_nao_consome_fichas_parcialmente` trava -- uma recusa não desconta fichas
parcialmente, mesmo que o balde tivesse fichas insuficientes apenas por uma fração do
custo pedido.

## Como decidir que tipo de duplo escrever

```mermaid
flowchart TD
    A["Módulo sob teste"] --> B{"Depende de tempo real?"}
    B -->|sim| C["Injetar o relógio: parâmetro obrigatório, sem valor padrão"]
    B -->|não| D{"Depende de colaborador externo substituível?"}
    D -->|sim| E{"O teste precisa verificar o que foi chamado?"}
    E -->|sim| F["Fake ou spy: grava a interação"]
    E -->|não, só a resposta importa| G["Stub: devolve ou levanta um valor fixo"]
    D -->|não, é função pura| H["Teste direto por classe de equivalência e valor de fronteira"]
```

Este segundo fluxo é o que decidiu a forma dos três módulos de exemplo, na ordem
inversa à leitura: `validador_cpf` caiu no ramo `H` (função pura, sem colaborador);
`limitador_de_taxa` caiu no ramo `C` (o próprio módulo já nasce com o relógio como
parâmetro obrigatório, não como decisão do teste); `notificacao` caiu nos ramos `F` e
`G` ao mesmo tempo, porque tem um teste de interação (`NotificadorFalso`) e um teste de
propagação de erro (`NotificadorQueFalha`) sobre o mesmo colaborador substituível. Um
módulo real raramente cai em um ramo só -- é comum que partes diferentes da mesma
suíte precisem de duplos diferentes, e forçar todo o módulo a um único tipo de duplo é
o que gera o anti-padrão descrito em `10-Anti-Patterns.md` sob o nome de mock
universal. Os dois fluxogramas desta seção existem para tornar essa decisão explícita
antes da escrita do teste, não depois -- decidir o tipo de duplo depois de já ter
escrito um mock genérico raramente leva a desfazer o trabalho, mesmo quando um fake
mais simples serviria melhor.
