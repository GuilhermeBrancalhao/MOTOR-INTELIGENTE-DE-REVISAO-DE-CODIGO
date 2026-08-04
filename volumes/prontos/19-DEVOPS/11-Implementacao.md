---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/19-devops/pipeline.py -->

`pipeline.py`, citado acima, formaliza P1-P6: `Pipeline.executar_estagio` recusa estágio fora de
ordem e bloqueia estágios seguintes após uma falha (P1/P5); `Pipeline` é um dataclass congelado
construído em torno de um único `Artefato`, tornando reatribuição de artefato um erro em tempo de
execução (P6); `implantar_em_producao` rejeita percentual 100 sem `forcar_completo=True` (P3);
`GerenciadorDeploy.artefato_atual` responde "o que está em produção" a partir do último registro
do histórico, nunca por suposição (P4); `GerenciadorDeploy.reverter` promove o artefato do
registro anterior, falhando explicitamente quando não há um (P2).


`ORDEM`, a lista que define a sequência de estágios, existe como constante única consultada tanto
por `executar_estagio` quanto por `pronto_para_producao` — evitando que as duas checagens
divirjam silenciosamente se a sequência mudar no futuro. `RegistroDeploy` também é congelado,
pela mesma razão que `Artefato`: um registro histórico não deveria ser alterável depois de
criado, ou a garantia de rastreabilidade (P4) perderia sentido.


O tipo de retorno `Artefato | None` de `artefato_atual` torna explícito, no próprio contrato da
função, que um ambiente sem deploy nenhum é um estado válido e distinto de erro — quem consome
essa função precisa lidar com a ausência explicitamente, em vez de receber uma exceção ou um
valor sentinela ambíguo para um caso que não é excepcional, apenas ainda não aconteceu.