---
volume: "40"
volume_nome: TEMPLATES
tipo: BIBLIOTECA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_template_incompleto_e_rejeitado` prova AB1/AB6: a mutação alvo é aceitar `Template` sem
`versao` ou `escopo_declarado`.

`test_depreciacao_sem_motivo_e_rejeitada` prova AB5: a mutação alvo é aceitar
`depreciado=True` sem motivo.

`test_template_com_conteudo_de_dominio_e_rejeitado` prova AB4: a mutação alvo é aceitar corpo de
template contendo termo do conjunto proibido.

`test_renderizar_sem_variavel_obrigatoria_e_rejeitado` e
`test_renderizar_com_variaveis_completas_funciona` provam AB3 nos dois sentidos.

`test_verificar_compatibilidade_detecta_versao_diferente` e
`test_verificar_compatibilidade_aceita_mesma_versao` provam AB2 nos dois sentidos.


Nenhum teste depende de motor de template real nem de sistema de renderização externo — todos
operam sobre `str.format` simples e estruturas de dado Python puras, suficientes para provar as
seis regras de governança de template sem qualquer custo de integração com biblioteca de
templating mais sofisticada ou complexa de configurar corretamente.

Essa escolha de projeto mantém a suíte determinística e extremamente rápida, seguindo a mesma filosofia de teste já estabelecida pelos demais volumes deste acervo inteiro.

Nenhuma parte da suíte depende de biblioteca de templating instalada, o que simplifica a
execução em qualquer ambiente sem configuração adicional de dependência externa, seja localmente
ou em qualquer pipeline automatizado que rode a suíte completa deste acervo de forma recorrente,
mantendo o tempo total de execução na casa dos milissegundos mesmo cobrindo tudo de ponta a ponta.