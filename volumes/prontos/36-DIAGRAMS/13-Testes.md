---
volume: "36"
volume_nome: DIAGRAMS
tipo: BIBLIOTECA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_tipo_de_diagrama_incompleto_e_rejeitado` prova X1: a mutação alvo é aceitar
`TipoDeDiagrama` sem `proposito` ou `quando_usar`.

`test_tipo_nao_catalogado_e_rejeitado` prova X3: a mutação alvo é aceitar um nome de tipo fora do
conjunto reconhecido.

`test_entrada_sem_prosa_explicativa_e_rejeitada` e
`test_entrada_sem_escopo_declarado_e_rejeitada` provam X2 e X6.

`test_escolher_tipo_por_necessidade_mapeia_corretamente` e
`test_necessidade_nao_catalogada_e_rejeitada` provam X5 nos dois sentidos.

`test_vigencia_detecta_diagrama_desatualizado` prova X4: confirma que um diagrama marcado como
não refletindo mais o sistema levanta exceção nomeada.


Nenhum teste depende de renderização real de Mermaid nem de validação de sintaxe visual — todos
operam sobre metadado estrutural (tipo, prosa, escopo, necessidade), o que é suficiente para
provar as seis regras de governança sem exigir um motor de renderização de diagrama disponível
durante a execução da suíte de teste.

Essa escolha de projeto mantém a suíte rápida e determinística, consistente com a filosofia de teste já adotada pelos demais volumes de biblioteca e processo deste acervo.

Nenhuma parte da suíte depende de biblioteca externa de renderização instalada, o que simplifica
a execução em qualquer ambiente sem configuração adicional, seja localmente ou em qualquer
pipeline de integração contínua que rode este acervo, sem passo de instalação extra necessário, mantendo o tempo total de execução na casa dos
milissegundos mesmo cobrindo as seis regras de ponta a ponta.