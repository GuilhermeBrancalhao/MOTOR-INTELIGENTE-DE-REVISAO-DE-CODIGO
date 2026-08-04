---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

**Registrar autoridade no momento da ingestão, nunca retroativamente.** Reconstruir origem de um
documento que já está na base há meses é, na maioria das vezes, impossível com precisão — a
autoridade só é confiável quando registrada no momento em que o documento entra.

**Definir `fato_chave` de forma granular o suficiente para detectar conflito real, sem ser tão
granular que todo documento pareça único.** Um `fato_chave` bom agrupa documentos que de fato
competem entre si sobre a mesma afirmação; um `fato_chave` ruim ou não agrupa nada (todo
documento é "único") ou agrupa demais (documentos não relacionados aparecem como conflito).

**Tratar expiração como parte do desenho inicial, não como funcionalidade adicionada depois.**
Um pipeline que nasce sem noção de ciclo de vida tende a acumular documento desatualizado
indefinidamente, porque adicionar expiração depois exige reclassificar tudo que já existe.

**Revisar documento em `Expirando` antes que vire `Expirado`**, não depois. A janela de
"expirando" existe justamente para dar tempo de revalidação antes da perda de validade, e
ignorá-la até o documento expirar desperdiça essa janela.

**Preferir coexistência marcada a escolha forçada quando dois documentos representam visões
legítimas diferentes**, não necessariamente conflito real — nem toda divergência precisa de um
vencedor único.

**Registrar o motivo da resolução de conflito, não só o resultado.** Saber que "d1 prevaleceu
sobre d2" é menos útil do que saber por quê — autoridade mais alta, informação mais recente, ou
decisão de negócio específica. O motivo é o que permite a alguém revisitar a decisão meses depois
sem precisar reconstruir o raciocínio original.
