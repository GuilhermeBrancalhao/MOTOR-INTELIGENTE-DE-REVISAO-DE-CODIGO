---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-08-04
---

# Testes

A mutação alvo de cada teste é nomeada no docstring.

`test_adr_incompleto_e_rejeitado` prova W1: a mutação alvo é aceitar `ADR` com campo vazio.

`test_adr_ja_registrado_nao_pode_ser_reescrito` e
`test_substituir_adr_marca_anterior_como_superado_sem_apagar` provam W2 — o primeiro confirma
rejeição de sobrescrita direta; o segundo confirma que substituição preserva o registro anterior.

`test_documento_nao_versionado_e_rejeitado` prova W3: a mutação alvo é aceitar
`versionado_junto_do_codigo=False`.

`test_verificacao_de_vigencia_detecta_documento_desatualizado` prova W4: confirma que uma
afirmação não mais verdadeira levanta exceção nomeada com a afirmação específica.

`test_edicao_manual_de_documento_gerado_e_rejeitada` prova W5: a mutação alvo é permitir edição
direta sobre documento gerado automaticamente.

`test_publico_alvo_invalido_e_rejeitado` prova W6: a mutação alvo é aceitar um terceiro valor de
público-alvo que tentaria misturar usuário e mantenedor no mesmo documento.


Nenhum teste depende de sistema de controle de versão real nem de repositório de código de fato
existente — todos operam sobre estruturas de dado Python puras, o que mantém a suíte rápida e
focada exclusivamente na lógica de governança que este volume formaliza.

Essa escolha de projeto mantém a suíte determinística e livre de qualquer dependência de infraestrutura externa ao processo de teste em si.

Isso reflete a mesma filosofia de teste já aplicada consistentemente em outros volumes de
governança e processo deste mesmo acervo, priorizando velocidade e determinismo acima de qualquer outra consideração possível aqui.