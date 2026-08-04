---
volume: "41"
volume_nome: SDK
tipo: ENGINE
secao: 07-Regras
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Regras

**AC1 — Mudança que quebra compatibilidade sempre exige versão maior nova.**
*Consequência:* quem confia na convenção de versionamento semântico nunca é enganado por uma
mudança que quebra lançada como versão menor ou de correção.

**AC2 — Superfície pública é mínima e deliberada; todo elemento público tem justificativa
explícita.** *Consequência:* nenhum elemento é público por omissão — a decisão de expor algo é
sempre consciente, nunca acidental.

**AC3 — Todo erro do SDK orienta correção, não apenas descreve o que falhou.**
*Consequência:* quem integra sempre tem um caminho de ação claro diante de um erro, não apenas
uma descrição do sintoma.

**AC4 — Compatibilidade retroativa é garantida dentro da mesma versão maior.**
*Consequência:* código escrito contra uma versão menor mais antiga continua funcionando sem
modificação contra versões menores mais recentes da mesma versão maior.

**AC5 — Elemento público é depreciado explicitamente, com motivo e caminho de migração, antes de
removido.** *Consequência:* nenhuma remoção quebra código de terceiros sem aviso prévio — sempre
existe um ciclo de depreciação anterior à remoção real.

**AC6 — Todo exemplo de uso é verificado contra o código real do SDK.**
*Consequência:* documentação nunca diverge silenciosamente do comportamento real que o SDK de
fato tem.

Essas seis regras se reforçam mutuamente: AC1 sem AC5 permitiria uma remoção correta em versão
maior, mas sem aviso prévio; AC5 sem AC1 permitiria depreciar e depois remover na mesma versão
menor, quebrando quem ainda não teve tempo de migrar. As duas juntas, aplicadas por
`SuperficieDoSDK.remover_membro`, são o que de fato protege o desenvolvedor externo do risco de
uma mudança inesperada.