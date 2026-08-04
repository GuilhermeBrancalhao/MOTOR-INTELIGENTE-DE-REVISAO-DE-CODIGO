---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a arquitetura de interface dentro do mesmo produto, com foco específico em como
ela lida com chamada de IA: estado de carregamento distinto, renderização incremental, estado de
falha visível, escopo de estado (componente vs. global), e cancelamento de requisição abandonada.

**Fronteira com `16-INTEGRATION`.** A robustez da chamada em si — contrato versionado,
idempotência, tolerância a falha do provedor — é daquele volume. Este volume trata do que a
interface faz com o resultado (ou a falha) dessa chamada depois que ela retorna ou falha, não da
chamada em si.

**Fronteira com `23-BACKEND-ARCHITECT` e `24-DATABASE-ARCHITECT`.** Onde e como o dado persiste
no lado do servidor é daqueles volumes; este volume trata apenas do que acontece no cliente.

**Fronteira com `25-API-ARCHITECT`.** O contrato entre frontend e backend — formato de request e
response, versionamento de endpoint — é daquele volume; este volume assume que esse contrato
existe e trata de como a interface reage à variabilidade específica de uma resposta de IA dentro
dele (chegada incremental, latência variável, formato que pode divergir do esperado).

Não cobre escolha de framework de interface nem biblioteca de gerenciamento de estado específica
— os princípios deste volume (estado de carregamento distinto, renderização incremental, escopo
de estado, cancelamento) valem independentemente da tecnologia escolhida para implementá-los.
