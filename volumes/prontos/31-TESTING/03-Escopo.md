---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-07-30
---

# Escopo

| Fica dentro deste volume | Fica fora, e vai para |
|---|---|
| Taxonomia de teste por camada (unitário, integração, contrato) e critério de quando usar cada uma | -- |
| Estrutura de um teste (arranjo-ação-verificação), nomenclatura e organização de suíte | -- |
| Taxonomia de duplo de teste (dummy, stub, fake, spy, mock) e critério de escolha | -- |
| Causa raiz e correção de teste instável (flaky), incluindo dependência de tempo real, de ordem de execução e de rede | -- |
| Teste de fronteira e de classe de equivalência para função pura | -- |
| Percentual de cobertura como indicador, sua tendência ao longo do tempo, e gate de release baseado nele | `32-QUALITY` -- é o indicador agregado; este volume produz o teste, não o painel que soma cobertura de todos eles |
| Política de segurança e os controles que precisam ser verdade sobre o sistema | `17-SECURITY` -- este volume ensina a estrutura de um teste automatizado; qual controle de segurança precisa de teste é decisão daquele volume |
| O processo que roda os controles de `17-SECURITY` a cada mudança no pipeline | `18-DEVSECOPS` -- é o processo; a prática de escrever o teste que ele executa continua sendo deste volume |
| Teste de carga e de performance sob volume alto de requisição | `33-PERFORMANCE` -- a taxonomia de teste unitário/integração daqui se aplica, mas o desenho de carga, os números de SLO e a infraestrutura de execução são de outro domínio |
| Avaliação de qualidade de prompt por caso de ouro (golden case), específica de `07-PROMPT-ENGINE` | `07-PROMPT-ENGINE/13-Testes.md` -- aquele volume já tem seção de testes própria, porque a unidade testada (um prompt) não é código determinístico da mesma forma que os três módulos deste volume; duplicar a taxonomia genérica aqui e a específica lá seria o mesmo conteúdo em dois lugares |
| Teste de contrato entre produtos/times diferentes, com tolerância a falha do lado externo | `16-INTEGRATION` -- a estrutura de teste (arranjo-ação-verificação, dublê) continua valendo, mas o que caracteriza contrato entre fronteiras de produto é assunto daquele volume |

## Fronteira interna: o que este volume não resolve por dentro

Os três módulos de `exemplos/31-testing/` foram escolhidos para cobrir três decisões de
teste distintas (função pura, código dependente de tempo, dependência substituível) --
não para formar um sistema coerente entre si. `validador_cpf`, `limitador_de_taxa` e
`notificacao` não se chamam entre si e não deveriam: cada um existe para que uma seção
deste volume tenha algo concreto para citar, e forçar os três a compor um único sistema
inflaria a superfície de código sem acrescentar lição de teste nova.
