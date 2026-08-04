---
volume: "39"
volume_nome: ROADMAP
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/39-roadmap/roadmap.py -->

`roadmap.py`, citado acima, formaliza AA1-AA6: `CriterioDePriorizacao.__post_init__` recusa
critério incompleto (AA1); `Roadmap.registrar_fora_de_escopo` recusa item sem motivo (AA2);
`Roadmap.sinalizar_decisao_de_autoridade` recusa decisão sem autoridade declarada (AA3);
`registrar_revisao_de_roadmap` recusa revisão com item atrasado sem motivo (AA4);
`ItemDeRoadmap.__post_init__` recusa item direcional com data comprometida (AA5);
`DependenciaEntreCiclos.__post_init__` exige os três campos completos, nunca inferidos (AA6).

`Roadmap` mantém três dicionários separados — `itens`, `fora_de_escopo` e
`decisoes_pendentes_de_autoridade` — em vez de uma única lista com um campo de tipo, porque cada
categoria tem operação de registro própria com sua própria validação específica, e misturar as
três exigiria despachar por tipo toda vez que alguém precisasse consultar apenas uma delas.

Essa separação também torna trivial expor apenas uma das três categorias, se necessário, sem vazar informação das outras duas categorias para quem não precisa dela.

Um sistema real com volume muito maior de itens provavelmente se beneficiaria de um armazenamento
mais sofisticado, como um banco de dado dedicado, mas o princípio de separação por categoria
permaneceria idêntico ao que este exemplo mínimo já demonstra com clareza suficiente aqui, sem
qualquer necessidade de otimização prematura que só complicaria a leitura deste código simples,
mantendo o exemplo focado exclusivamente em demonstrar as seis regras com a máxima clareza possível.