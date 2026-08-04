---
volume: "19"
volume_nome: DEVOPS
tipo: ARQUITETURA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`Artefato` é o modelo central: `hash` (identidade imutável do build) e `commit` (origem
rastreável). É `frozen=True` — não existe operação que altere um artefato depois de criado, só
criação de um novo. Essa imutabilidade não é estilo de código, é a implementação direta de P6:
se o artefato não pode mudar depois de construído, ele não pode divergir entre o que foi validado
em staging e o que roda em produção.

`Estagio` é um enum ordenado (BUILD, TESTE, SEGURANCA, STAGING, PRODUCAO) — a ordem de declaração
no código é a mesma ordem exigida em execução, para que a sequência não dependa de uma lista de
configuração separada que poderia divergir do enum.

`Pipeline` é também `frozen=True`, carregando um único `Artefato` e a lista mutável
`estagios_concluidos`. O congelamento do dataclass impede reatribuir `pipeline.artefato` depois de
criado; a lista em si continua mutável porque o pipeline precisa registrar progresso — congelar o
dataclass previne troca de identidade do artefato, não impede avanço de estado.

`RegistroDeploy` carrega o `Artefato` implantado, o percentual de tráfego e uma flag indicando se
foi originado por rollback — essa distinção é o que permite ao histórico responder não só "o que
está rodando" mas "como chegou a estar rodando".
