---
volume: "35"
volume_nome: DOCUMENTATION
tipo: GOVERNANCA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre governança de documentação: registro de decisão arquitetural (ADR),
imutabilidade de decisão aceita, versionamento junto do código, verificação de vigência, e
distinção entre conteúdo gerado e conteúdo mantido manualmente.

**Fronteira com `39-ROADMAP`.** Planejamento de trabalho futuro e priorização são daquele
volume. Este volume trata de registro de decisão já tomada — o ADR documenta o que foi decidido e
por quê, não o que ainda está por decidir.

**Fronteira com `30-AI-GOVERNANCE`.** Aquele volume trata de governança de decisão automatizada
que afeta pessoa — responsabilidade, revisão humana, trilha de auditoria de decisão de negócio.
Este volume trata de governança de decisão arquitetural e de documentação em si, um domínio
diferente de governança.

**Fronteira com `36-DIAGRAMS` e `40-TEMPLATES`.** Catálogo de diagrama e de template reutilizável
são daqueles volumes (tipo BIBLIOTECA). Este volume trata do processo de decidir o que documentar
e como manter essa documentação vigente, não do catálogo de artefato específico em si.

Não cobre ferramenta específica de geração de documentação — os princípios deste volume (ADR
imutável, versionamento junto do código, vigência verificada, distinção gerado/manual) valem
independentemente de qual ferramenta produz ou publica a documentação.


Essas três fronteiras (39, 30, 36/40) isolam este volume da tentação de virar um "volume de
documentação geral" — ele trata especificamente do processo de registrar decisão e manter
documentação vigente, não de planejamento futuro, governança de decisão de negócio, nem catálogo
de artefato reutilizável, que já têm seus próprios volumes dedicados.