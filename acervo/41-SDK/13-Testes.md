---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 13-Testes
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_release_que_quebra_sem_bump_de_major_e_rejeitado` e
`test_release_compativel_sem_bump_de_major_e_aceito` provam AC1 nos dois sentidos.

`test_membro_publico_sem_justificativa_e_rejeitado` prova AC2: a mutação alvo é aceitar
`MembroDeSDK` público sem motivo declarado.

`test_erro_sem_orientacao_de_correcao_e_rejeitado` prova AC3: a mutação alvo é aceitar
`ErroDoSDK` sem `como_corrigir`.

`test_remocao_de_membro_publico_sem_depreciacao_e_rejeitada` e
`test_remocao_apos_depreciacao_com_major_bump_funciona` provam AC4/AC5 nos dois sentidos — a
remoção só é aceita depois do ciclo completo de depreciação e incremento de versão maior.

`test_exemplo_nao_verificado_e_rejeitado` prova AC6: a mutação alvo é aceitar
`ExemploDeUso` sem `resultado_verificado=True`.

`test_remocao_de_membro_publico_depreciado_sem_bump_de_major_e_rejeitada` prova que depreciação
sozinha não basta — a mutação alvo é aceitar remoção de membro já depreciado mas sem incremento
de versão maior, o que ainda quebraria quem não teve tempo de reagir ao aviso de depreciação.

`test_remocao_de_membro_inexistente_e_rejeitada` prova que a operação nunca falha silenciosamente
para um nome que não existe na superfície — a mutação alvo é aceitar remoção de membro fantasma
sem levantar exceção alguma.

Nenhum teste depende de publicação real em repositório de pacote nem de instalação de biblioteca
gerada — toda a suíte roda sobre estruturas de dado Python puras, mantendo o tempo de execução na
casa dos milissegundos.

`test_membro_publico_com_justificativa_funciona` e `test_erro_sem_orientacao_de_correcao_e_rejeitado`
completam o par positivo/negativo de AC2 e AC3, respectivamente, seguindo a mesma convenção de
prova nos dois sentidos já usada pelos demais volumes deste acervo inteiro.