---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/24-database-architect/repositorio.py -->

`repositorio.py`, citado acima, formaliza A1-A6: `aplicar_migracao` rejeita migração marcada
como incompatível antes de registrá-la (A1); `RegistroDeConteudo` recusa criação sem
`Procedencia` (A2); `Repositorio.salvar` levanta `ConflitoDeConcorrencia` quando a versão
esperada não corresponde à versão real (A3); `declarar_tabela` recusa política de retenção
ausente (A4); `ler_tolerante` preserva campo desconhecido em vez de descartá-lo ou falhar (A5);
`Repositorio.remover` verifica referência ativa antes de excluir (A6).

`Repositorio.registros`, `politicas_de_retencao` e `referencias` usam `default_factory=dict`, não
um valor padrão mutável compartilhado — um erro comum em Python que faria múltiplas instâncias de
`Repositorio` compartilharem acidentalmente o mesmo dicionário, algo que um teste que cria duas
instâncias e verifica isolamento entre elas confirmaria não estar acontecendo aqui.

O parâmetro `versao_esperada` de `salvar` é obrigatório, sem valor padrão — forçando quem grava a
declarar explicitamente contra qual versão está escrevendo, em vez de um padrão implícito que
poderia mascarar a ausência de verificação de concorrência.

`ler_tolerante` reconstrói `Procedencia` a partir de um dicionário aninhado (`bruto["procedencia"]`)
usando desempacotamento de argumentos nomeados — se o dicionário bruto não contiver exatamente os
campos `modelo` e `versao` esperados por `Procedencia`, a própria construção do objeto falha de
forma explícita, em vez de silenciosamente aceitar uma proveniência incompleta ou malformada,
propagando esse erro de forma tardia e mais difícil de rastrear até sua causa original.