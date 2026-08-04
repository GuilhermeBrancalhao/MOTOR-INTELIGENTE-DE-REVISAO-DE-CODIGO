---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 01-Introducao
status: PRONTO
atualizado_em: 2026-08-04
---

# Introdução

`17-SECURITY` declara o que precisa ser verdade sobre o sistema — os controles, o vetor de risco
que cada um mitiga, como cada um é verificado. Mas uma política declarada e nunca automatizada
não protege nada: ela existe em documento, alguém a lê uma vez, e o sistema evolui sem que
ninguém volte a checar se a condição que a política exige ainda se sustenta. Este volume trata do
processo que fecha essa distância — como o controle declarado no 17 vira um gate que roda de
verdade, a cada mudança, sem depender de alguém lembrar de rodá-lo manualmente.

A diferença entre segurança como política e segurança como processo contínuo é a diferença entre
auditoria periódica e prevenção no momento em que o risco é introduzido. Uma auditoria trimestral
encontra o problema meses depois de ele ter entrado em produção; um gate que roda em toda
mudança encontra o problema antes do merge, quando corrigir ainda custa uma linha de código e uma
conversa, não um incidente.

Este volume não define quais controles existem — isso é `17-SECURITY`. Define como um controle
declarado passa a ser enforçado: o pipeline que executa a verificação, o que acontece quando ela
falha, e a diferença entre uma exceção documentada com prazo e um bypass silencioso que nunca
mais é revisado.
