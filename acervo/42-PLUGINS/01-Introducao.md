---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 01-Introducao
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Introdução

Um plugin é código de terceiros que passa a rodar dentro do próprio host, não apenas ao lado
dele — essa proximidade é exatamente o que torna a disciplina de plugin diferente da disciplina
de SDK tratada em `41-SDK`. Um SDK quebrado no código do desenvolvedor externo falha no processo
dele; um plugin mal isolado, ao quebrar, pode derrubar o processo do host inteiro, afetando todo
usuário do produto, não apenas quem instalou aquele plugin específico.

Este volume trata da disciplina de ecossistema de plugin: contrato de extensão versionado entre
host e plugin, isolamento de falha (uma exceção de plugin nunca propaga ao host), permissão
declarada explicitamente (nenhuma capacidade concedida por omissão), registro explícito de
ativação (nunca execução implícita de código encontrado por acaso em um caminho de busca),
desativação sem efeito residual, e evolução do próprio contrato de extensão seguindo a mesma
disciplina de versionamento semântico já formalizada para superfície pública de SDK.

A metáfora central é a de uma casa com tomadas padronizadas: qualquer aparelho compatível com o
padrão de tomada funciona, sem que o dono da casa precise confiar cegamente no fabricante do
aparelho — o padrão de tomada (o contrato de extensão) é o que protege a casa de um aparelho
malfeito, não a boa vontade de quem o fabricou.
