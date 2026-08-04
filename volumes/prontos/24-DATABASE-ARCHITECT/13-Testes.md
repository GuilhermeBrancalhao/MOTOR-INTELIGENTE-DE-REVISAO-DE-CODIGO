---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_migracao_incompativel_e_rejeitada` e `test_migracao_compativel_e_aceita` provam A1 nos dois
sentidos — a mutação alvo do primeiro é registrar uma migração incompatível sem rejeição.

`test_registro_sem_procedencia_e_rejeitado` prova A2: a mutação alvo é aceitar
`RegistroDeConteudo` construído sem `Procedencia`.

`test_salvar_com_versao_desatualizada_gera_conflito` e
`test_salvar_com_versao_correta_funciona_e_incrementa` provam A3 nos dois sentidos.

`test_declarar_tabela_sem_retencao_e_rejeitada` prova A4: a mutação alvo é aceitar declaração de
tabela sem política de retenção.

`test_leitura_tolera_campo_desconhecido` prova A5: confirma que um campo não reconhecido não
quebra a leitura e permanece acessível em `campos_desconhecidos`.

`test_remover_registro_referenciado_e_rejeitado` e
`test_remover_registro_sem_referencia_funciona` provam A6 nos dois sentidos — a mutação alvo do
primeiro é permitir exclusão que deixaria referência quebrada.


Nenhum teste depende de um banco de dados real — `Repositorio` opera inteiramente sobre
estruturas em memória, permitindo verificar exaustivamente as seis regras sem custo nem
instabilidade de infraestrutura externa. `test_salvar_com_versao_correta_funciona_e_incrementa`
verifica não apenas que a escrita foi aceita, mas que o conteúdo e a versão refletem exatamente a
segunda escrita, não uma mistura entre as duas.

`test_migracao_incompativel_e_rejeitada` verifica não apenas que a exceção é levantada, mas que o
`historico` permanece vazio depois da tentativa — confirmando que a rejeição é completa, sem
registro parcial de uma migração que nunca deveria ter sido aceita em primeiro lugar.