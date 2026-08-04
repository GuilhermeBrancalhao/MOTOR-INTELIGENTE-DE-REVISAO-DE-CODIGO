---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_caso_de_uso_sem_dono_e_rejeitado` prova G1: a mutação alvo é aceitar `CasoDeUso` sem
`dono_responsavel`.

`test_verificar_producao_para_caso_nao_classificado_e_rejeitado` prova G2: a mutação alvo é
permitir verificação de produção para um caso nunca registrado.

`test_decisao_de_alto_risco_sem_revisao_humana_e_rejeitada` e
`test_decisao_de_baixo_risco_nao_exige_revisao_humana` provam G3 nos dois sentidos — o rigor é
proporcional ao risco, não uniforme.

`test_toda_decisao_registrada_fica_na_trilha_de_auditoria` prova G4: confirma que uma decisão
aceita aparece no histórico com todos os campos de contexto preservados.

`test_producao_sem_aprovacao_explicita_e_rejeitada` e
`test_producao_com_aprovacao_e_permitida` provam G5 nos dois sentidos.

`test_revisao_periodica_acumula_historico` prova G6: confirma que duas revisões sucessivas
coexistem no histórico, sem que a segunda apague a primeira.


Nenhum teste depende de um modelo de IA real nem de dado sensível de pessoa real — `entrada` nos
testes de `DecisaoAutomatizada` usa valores ilustrativos simples, suficientes para provar a lógica
de governança sem qualquer necessidade de dado real ou de conformidade adicional para os próprios
testes.

Essa escolha deliberada de dado sintético e simples mantém o foco da suíte inteiramente sobre a
lógica de governança, sem introduzir preocupação adicional sobre proteção de dado real dentro do
próprio ambiente de teste, nem exigir qualquer tratamento especial de privacidade só para rodar
a suíte localmente, mantendo o custo de execução da suíte inteira na casa dos milissegundos.