---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 02-Objetivos
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Objetivos

Seguir versionamento semântico real — mudança que quebra compatibilidade sempre exige versão
maior nova, nunca lançada como versão menor ou de correção que engana quem confia na convenção.

Manter superfície pública mínima e deliberada — todo elemento exposto tem justificativa explícita
para ser público, nunca público por omissão de alguém esquecer de marcar como interno.

Garantir que todo erro levantado pelo SDK oriente correção, não apenas descreva o que falhou —
"o quê" sem "como corrigir" deixa quem integra sem caminho claro de ação.

Garantir compatibilidade retroativa dentro da mesma versão maior — código escrito contra uma
versão menor mais antiga continua funcionando sem modificação contra versões menores mais
recentes da mesma versão maior.

Depreciar elemento público explicitamente, com motivo e caminho de migração, antes de removê-lo
na próxima versão maior — nunca removido sem ciclo de depreciação anterior.

Manter todo exemplo de uso do SDK verificado contra o código real, nunca documentação que diverge
silenciosamente do comportamento de fato.

Nenhum desses objetivos depende de uma linguagem de implementação específica ou de um formato
particular de empacotamento — o princípio central é sempre o mesmo, independentemente de o SDK
ser publicado como pacote Python, biblioteca JavaScript, ou qualquer outro formato de
distribuição de código para desenvolvedor externo consumir diretamente no próprio projeto.