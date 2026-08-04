---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 02-Objetivos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Objetivos

Definir contrato de extensão versionado entre host e plugin, rejeitando ativação de plugin cujo
contrato alvo seja incompatível com o contrato que o host de fato oferece, antes de qualquer hook
ser chamado em produção.

Isolar toda falha originada dentro de um plugin — uma exceção levantada por um hook de plugin
nunca propaga ao host; o host sempre contém, registra e segue funcionando, mesmo que aquele
plugin específico pare de funcionar corretamente.

Exigir declaração explícita de toda capacidade que um plugin pretende usar, negando acesso a
qualquer capacidade não declarada — nenhuma permissão é concedida por omissão ou por padrão amplo
demais.

Exigir registro explícito de ativação — nome, versão de contrato alvo e ponto de entrada
declarados —, nunca execução automática de código apenas por sua presença em um diretório ou
caminho de busca.

Garantir que desativar um plugin não deixe efeito residual no estado do host — a desativação é
simétrica à ativação, liberando todo recurso alocado durante a ativação daquele plugin específico.

Evoluir o contrato de extensão seguindo a mesma disciplina de versionamento semântico do `41-SDK`
— mudança que quebra um hook existente sempre exige versão maior nova do próprio contrato, nunca
lançada como versão menor.
