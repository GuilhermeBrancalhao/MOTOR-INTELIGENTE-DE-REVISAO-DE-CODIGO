---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 03-Escopo
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a disciplina de SDK exposto a desenvolvedor externo: versionamento semântico
real, superfície pública deliberada, erro acionável, compatibilidade retroativa, depreciação
explícita, e exemplo verificado.

**Fronteira com `25-API-ARCHITECT`.** O contrato de rede exposto ao cliente — endpoint,
formato de resposta, orçamento de latência — é daquele volume. Este volume trata especificamente
do SDK empacotado: biblioteca instalada diretamente no código de terceiros, onde a superfície
pública é o próprio código-fonte exposto, com disciplina de versionamento de pacote de software,
não apenas de contrato de rede.

**Fronteira com `40-TEMPLATES`.** Depreciação explícita de template reutilizável (AB5) segue o
mesmo princípio geral aplicado aqui a elemento de SDK — a diferença é que remoção de elemento
público de SDK, sem ciclo de depreciação, quebra código de terceiros compilado ou já publicado,
um risco mais imediato que depreciação de template interno.

**Fronteira com `37-CODE-GENERATION`.** A disciplina de validar código gerado antes de aceitar
(Y1) é reaproveitada aqui para exemplo de uso do SDK — um exemplo na documentação é, ele mesmo,
código que precisa ser verificado contra a realidade, nunca apenas escrito e presumido correto.

Não cobre linguagem específica de implementação do SDK — os princípios deste volume (versão
semântica, superfície mínima, erro acionável, compatibilidade retroativa, depreciação, exemplo
verificado) valem independentemente de qual linguagem o SDK é publicado.
