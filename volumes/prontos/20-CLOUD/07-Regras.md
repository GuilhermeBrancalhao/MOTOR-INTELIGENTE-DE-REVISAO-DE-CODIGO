---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**N1 — Todo recurso de infraestrutura é declarado em configuração versionável antes de existir.**
*Consequência:* não há recurso "clicado em existência" sem registro — todo recurso reconhecido
pelo sistema passou por uma declaração auditável.

**N2 — Todo recurso que sustenta um alvo de disponibilidade que exige redundância é redundante,
sem exceção implícita.** *Consequência:* ausência de redundância onde é necessária aparece como
lacuna explícita na verificação, nunca como suposição silenciosa de que está tudo bem.

**N3 — Todo recurso tem um dono declarado, responsável por seu custo e seu risco.**
*Consequência:* custo e risco de infraestrutura são sempre justificáveis por alguém específico —
nunca existe recurso "de ninguém" cujo motivo de existir ninguém consegue explicar.

**N4 — Mudança de infraestrutura é isolada por ambiente; uma alteração destinada a um ambiente
nunca alcança outro de forma implícita.** *Consequência:* staging e produção nunca divergem por
um erro de contexto na aplicação de uma mudança — a validação de ambiente acontece antes da
aplicação, não depois.

**N5 — Segredo nunca é declarado como texto plano na configuração de infraestrutura.**
*Consequência:* mesmo um repositório privado não se torna um vazamento de credencial só por
conter a configuração declarada — segredo vem de um cofre, referenciado, nunca embutido.

**N6 — O estado real da infraestrutura é periodicamente comparado contra o estado declarado, e
toda divergência é reportada explicitamente.** *Consequência:* uma mudança feita fora do fluxo
declarado (manual, de emergência, ou por engano) não permanece invisível até causar um incidente
— ela aparece como divergência detectável antes disso.
