---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 03-Escopo
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a disciplina de ecossistema de plugin: contrato de extensão versionado,
isolamento de falha, permissão declarada, registro explícito, desativação sem resíduo, e evolução
do contrato seguindo disciplina de versionamento semântico.

**Fronteira com `41-SDK`.** Um SDK é consumido por código de terceiros que roda no processo
*do próprio desenvolvedor externo*; um plugin roda *dentro do processo do host*, o que torna
isolamento de falha (AD2) e permissão declarada (AD3) preocupações centrais aqui que não existem
da mesma forma para SDK. AD6 reaproveita diretamente o princípio de AC1/AC5 de `41-SDK` — o
contrato de extensão é, ele mesmo, uma superfície pública sujeita à mesma disciplina de
versionamento e depreciação.

**Fronteira com `20-CLOUD` e `18-DEVSECOPS`.** Isolamento de falha de plugin (AD2) e permissão
declarada (AD3) ecoam princípios de isolamento de processo e menor privilégio já tratados nesses
volumes para infraestrutura em geral — este volume aplica o mesmo princípio especificamente à
relação entre host e código de extensão de terceiros.

Não cobre implementação de sandbox de sistema operacional nem de máquina virtual isolada — os
princípios aqui (contrato versionado, isolamento de falha, permissão declarada, registro
explícito, desativação limpa, evolução disciplinada do contrato) valem com qualquer mecanismo de
isolamento técnico escolhido, do mais simples (captura de excecão em Python) ao mais complexo
(processo separado, sandbox de sistema).
