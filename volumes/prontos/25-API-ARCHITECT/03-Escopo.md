---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o contrato exposto ao cliente dentro do mesmo produto: versionamento,
tradução entre formato interno e externo, formato de erro consistente, exposição de status de
trabalho, e orçamento de latência declarado.

**Fronteira com `24-DATABASE-ARCHITECT`.** O formato de persistência interna — schema, campos de
controle de concorrência, proveniência — é daquele volume. Este volume garante que esse formato
nunca atravessa diretamente para o cliente; a tradução entre os dois é responsabilidade explícita
desta camada.

**Fronteira com `23-BACKEND-ARCHITECT`.** O modelo de trabalho assíncrono com estado
(ENFILEIRADO, EXECUTANDO, CONCLUIDO, FALHOU_PERMANENTEMENTE) é daquele volume. Este volume define
como esse estado é exposto como recurso HTTP consultável, não a lógica de transição em si.

**Fronteira com `16-INTEGRATION`.** Versionamento de contrato que este produto consome de um
fornecedor externo é daquele volume (I1/I6); este volume trata do contrato que este produto
expõe para seus próprios clientes, internos ou externos.

Não cobre escolha de protocolo específico (REST, GraphQL, gRPC) — os princípios deste volume
(versionamento, tradução, erro consistente, status consultável, orçamento de latência) valem
independentemente do protocolo escolhido para implementá-los.


A escolha de não cobrir protocolo específico é deliberada pela mesma razão que aparece em outros
volumes deste grupo: um produto real pode expor REST para um conjunto de clientes e GraphQL ou
gRPC para outro, e as seis regras deste volume deveriam continuar valendo independente de qual
protocolo carrega o contrato — a disciplina é sobre o que é prometido, não sobre como é
transportado.