---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_nenhum_resultado_exibido_enquanto_carregando` prova F1: a mutação alvo é `resolver_exibicao`
retornar algo diferente de `None` para uma requisição ainda em CARREGANDO, o que esconderia a
diferença entre "ainda esperando" e "já tem resposta".

`test_fragmentos_acumulam_incrementalmente` prova F2: a mutação alvo é armazenar apenas o texto
final, perdendo a possibilidade de renderização incremental.

`test_falha_sem_cache_nao_produz_fallback_enganoso` e
`test_falha_com_cache_retorna_fallback_marcado` provam F3 nos dois sentidos.

`test_promocao_sem_autorizacao_e_rejeitada` e `test_promocao_autorizada_funciona` provam F4 nos
dois sentidos — a mutação alvo do primeiro é permitir promoção implícita.

`test_fragmento_apos_cancelamento_e_descartado` e
`test_cancelamento_impede_conclusao_subsequente` provam F5: a mutação alvo é continuar
acumulando fragmento ou permitir conclusão depois de `cancelar()` já ter sido chamado.

`test_adaptador_traduz_resposta_bruta_antes_da_ui` prova F6: confirma que o resultado consumido
pela interface já passou pela função de tradução, nunca é o dicionário bruto do provedor.


Nenhum teste depende de temporização real ou de um provedor de IA de verdade — todas as
transições de `RequisicaoDeIA` são síncronas e determinísticas no exemplo, o que torna possível
testar exaustivamente uma condição de corrida (fragmento chegando depois de cancelamento) sem
precisar reproduzir de fato uma corrida entre duas operações assíncronas concorrentes.

`test_promocao_sem_autorizacao_e_rejeitada` verifica não só que a exceção é levantada, mas que o
`estado_global` permanece vazio depois da tentativa — provando que a rejeição é completa, sem
efeito colateral parcial que deixasse um vestígio da promoção negada.