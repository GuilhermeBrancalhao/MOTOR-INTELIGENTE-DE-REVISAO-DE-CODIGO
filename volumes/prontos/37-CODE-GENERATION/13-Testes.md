---
volume: "37"
volume_nome: CODE-GENERATION
tipo: ENGINE
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_especificacao_incompleta_e_rejeitada` prova Y5/Y6: a mutação alvo é aceitar
`EspecificacaoDeGeracao` sem `versao` ou `escopo_declarado`.

`test_codigo_nao_marcado_e_rejeitado` prova Y2: a mutação alvo é aceitar código gerado sem a
marcação correspondente.

`test_codigo_sem_validacao_e_rejeitado` e `test_codigo_com_validacao_falha_e_rejeitado` provam
Y1 em dois cenários — ausência de validação e validação que de fato falhou.

`test_codigo_sem_revisao_humana_e_rejeitado` prova Y4: a mutação alvo é aceitar código gerado
sem revisão humana registrada, mesmo com validação completa.

`test_edicao_manual_de_codigo_gerado_e_rejeitada` prova Y2 na direção de edição: a mutação alvo é
permitir edição direta sobre código marcado como gerado.

`test_geracao_e_deterministica_para_mesma_especificacao` prova Y3: confirma igualdade de valor
entre duas chamadas de `gerar` com a mesma entrada.


Nenhum teste depende de compilador real nem de execução de suíte de teste externa — os
resultados de validação são construídos diretamente como valores sintéticos que representam o
cenário sendo testado, o que isola completamente a lógica de aceitação e revisão do processo,
potencialmente caro, de de fato compilar e testar código gerado real em produção.

Essa escolha de projeto reflete a mesma filosofia de teste já estabelecida por outros volumes ENGINE deste acervo, priorizando velocidade e isolamento total.

Mesmo o teste de determinismo evita qualquer dependência de tempo real ou de aleatoriedade, construindo o gerador como uma função pura completamente previsível entre chamadas sucessivas.