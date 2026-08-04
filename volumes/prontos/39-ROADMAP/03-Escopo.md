---
volume: "39"
volume_nome: ROADMAP
tipo: PROCESSO
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o processo de backlog de longo prazo: priorização por critério explícito, item
fora de escopo registrado, decisão sinalizada como exigindo autoridade externa, revisão periódica,
e distinção entre compromisso e direção.

**Fronteira com `38-PROJECT-PLANNER`.** Decompor um objetivo já priorizado em tarefas executáveis
dentro de um ciclo específico é daquele volume. Este volume decide qual objetivo entra no backlog
e em que ordem — a fronteira é a mesma que separa "o que vamos fazer, e quando" (aqui) de "como
vamos fazer isso especificamente" (38).

**Fronteira com `35-DOCUMENTATION`.** Registro de decisão arquitetural com consequência duradoura
(ADR) é daquele volume — uma decisão de roadmap sinalizada como exigindo autoridade externa (AA3)
pode, eventualmente, gerar um ADR quando de fato decidida, mas o roadmap em si não é onde a
decisão arquitetural fica registrada permanentemente.

**Fronteira com `30-AI-GOVERNANCE`.** Aprovação de caso de uso de IA antes de produção é daquele
volume. Priorização de roadmap pode incluir quando um caso de uso é proposto para desenvolvimento,
mas a aprovação de governança em si acontece separadamente, antes de produção.

Não cobre ferramenta específica de gestão de backlog — os princípios deste volume (critério
explícito, escopo registrado, autoridade sinalizada, revisão periódica, distinção de horizonte)
valem independentemente de qual ferramenta representa o roadmap visualmente.
