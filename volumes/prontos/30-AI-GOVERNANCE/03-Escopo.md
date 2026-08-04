---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre a governança organizacional do uso de IA: responsabilidade nomeada,
classificação de risco, revisão humana obrigatória por nível de risco, trilha de auditoria de
decisão, e aprovação antes de produção.

**Fronteira com `17-SECURITY`.** A defesa técnica contra ataque — isolamento de instrução e dado,
prevenção de exfiltração, sandboxing de execução — é daquele volume. Este volume trata de
governança de decisão, não de defesa contra adversário: um sistema pode estar tecnicamente seguro
segundo o 17 e ainda causar dano por decisão automatizada sem dono, sem classificação de risco, ou
sem revisão humana onde deveria haver.

**Fronteira com `18-DEVSECOPS`.** O processo que enforça controle técnico de segurança no
pipeline é daquele volume. Este volume trata de aprovação de caso de uso e classificação de risco
organizacional — um gate diferente, aplicado antes mesmo de código chegar ao pipeline técnico.

**Fronteira com `26-AI-MODELS`.** A seleção técnica de modelo (capacidade, avaliação, custo) é
daquele volume. Este volume trata de quem é responsável pelo caso de uso que usa esse modelo, não
de qual modelo é tecnicamente adequado.

Não cobre política legal específica de jurisdição — os princípios deste volume (responsabilidade
nomeada, classificação de risco, revisão humana, auditoria, aprovação) são a base sobre a qual uma
política de conformidade legal específica se apoiaria, sem substituí-la.
