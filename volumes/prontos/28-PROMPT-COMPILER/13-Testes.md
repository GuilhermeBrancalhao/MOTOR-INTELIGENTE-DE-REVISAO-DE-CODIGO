---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_compilar_prompt_nao_promovido_e_rejeitado` prova Q1: a mutação alvo é aceitar prompt fora
do estado PROMOVIDO.

`test_variavel_ausente_e_rejeitada` prova Q6: a mutação alvo é renderizar com placeholder vazio
em vez de rejeitar explicitamente.

`test_compilacao_e_deterministica_para_mesma_entrada` prova Q2: duas chamadas com argumentos
idênticos produzem `PayloadCompilado` iguais por comparação de valor.

`test_orcamento_excedido_e_rejeitado` prova Q3: a mutação alvo é aceitar payload acima do
orçamento sem erro.

`test_dois_dialetos_produzem_formatacoes_diferentes` prova Q4: confirma que a formatação vem do
adaptador injetado, não de lógica fixa dentro de `compilar`.

`test_ponto_de_cache_em_posicao_invalida_e_rejeitado` e
`test_ponto_de_cache_em_posicao_estavel_e_aceito` provam Q5 nos dois sentidos.


Nenhum teste depende de chamada real a um provedor de IA — `dialeto_simples` e
`dialeto_com_sistema` são adaptadores puramente locais que simulam formatação sem qualquer
dependência externa, o que mantém a suíte rápida e determinística mesmo ao testar Q4
especificamente.

Essa escolha de projeto reflete a mesma filosofia de outros volumes ENGINE deste acervo — comportamento verificável sem custo de infraestrutura externa.

Mesmo o teste que compara dois dialetos evita qualquer chamada de rede, bastando comparar a
estrutura de dado retornada por cada adaptador local, o que mantém o tempo total da suíte
inteira na casa dos poucos milissegundos, mesmo cobrindo as seis regras de forma bem exaustiva.