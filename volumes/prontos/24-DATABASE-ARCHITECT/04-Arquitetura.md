---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`Migracao` representa uma mudança de schema com uma flag explícita de compatibilidade com a
versão anterior — `aplicar_migracao` recusa registrar uma migração marcada como incompatível,
tornando a disciplina de expandir-antes-de-contrair (adicionar o novo formato, migrar os
consumidores, só depois remover o antigo) uma verificação, não apenas uma convenção de processo.

`RegistroDeConteudo` recusa sua própria criação sem `Procedencia` — um par de modelo e versão que
identifica o que produziu o conteúdo. Essa recusa acontece no momento da construção do objeto, não
como validação posterior, tornando proveniência ausente estruturalmente impossível de passar
despercebida.

`Repositorio.salvar` implementa controle de concorrência otimista: toda escrita declara a versão
que espera encontrar, e uma divergência entre essa expectativa e o estado real gera
`ConflitoDeConcorrencia` explícito — nunca uma sobrescrita silenciosa. `Repositorio.ler_tolerante`
separa campos reconhecidos de campos desconhecidos ao interpretar um registro bruto, preservando
os desconhecidos em vez de descartá-los ou falhar ao encontrá-los.

`Repositorio.remover` verifica referência ativa antes de excluir um registro — uma exclusão que
deixaria outro registro apontando para algo inexistente é rejeitada explicitamente, nunca
executada silenciosamente.


Nenhum desses quatro componentes (`Migracao`, `RegistroDeConteudo`, `Repositorio`, `Procedencia`)
conhece detalhes de infraestrutura de armazenamento — a arquitetura representa apenas a lógica de
decisão (compatibilidade, proveniência, concorrência, retenção, tolerância de leitura), deixando
a tradução para uma tecnologia de banco específica como responsabilidade de uma camada de
adaptação que não faz parte deste modelo mínimo.