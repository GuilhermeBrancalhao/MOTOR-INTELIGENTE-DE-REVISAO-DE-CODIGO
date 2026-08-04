---
volume: "18"
volume_nome: DEVSECOPS
tipo: PROCESSO
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-08-04
---

# Conclusão

A distinção que este volume defende é simples de enunciar e fácil de perder na prática: uma
política de segurança declarada não é o mesmo que uma política enforçada. `17-SECURITY` decide o
que precisa ser verdade; este volume garante que alguém — ou melhor, algo automatizado — de fato
verifica isso a cada mudança, e que a falha bloqueia por padrão, com exceção sempre nomeada e
sempre temporária.

O ponto mais fácil de negligenciar não é o bloqueio em si — é a expiração do waiver. Um sistema
de exceção sem prazo, ou com prazo que só é honrado se alguém lembrar de agir, converge com o
tempo para uma política que existe em documento mas não em enforcement — exatamente o problema
que este processo existe para evitar. A regra que sustenta tudo o resto é que o padrão é bloquear,
e toda exceção paga um preço explícito: um nome, um motivo, e uma data em que deixa de valer.
