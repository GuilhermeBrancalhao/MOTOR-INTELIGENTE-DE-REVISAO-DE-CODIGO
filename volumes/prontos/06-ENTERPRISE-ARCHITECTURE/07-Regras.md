---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-04
---

# Regras

**E1 — Todo sistema com componente de IA se registra no inventário de portfólio**, com
fornecedor, modelo e fonte de dado explícitos. *Consequência:* sistema não registrado é invisível
ao portfólio, e invisibilidade é a condição que produz dependência não decidida de propósito.

**E2 — Decisão de portfólio só se aplica quando há consequência nomeável que cruza projeto**
(concentração de fornecedor, fronteira de governança de dado). *Consequência:* decisão de
portfólio sem essa justificativa explícita é overreach, não decisão legítima.

**E3 — Custo total de propriedade é medido em agregado, nunca só por projeto isolado.**
*Consequência:* uma análise de custo que olha só o projeto individual pode aprovar dez decisões
que juntas custam mais do que qualquer uma delas revelaria sozinha.

**E4 — Portfólio não decide arquitetura técnica interna de um sistema.** Isso é sempre do
projeto. *Consequência:* uma revisão de portfólio que opina sobre padrão de código ou desenho
interno excedeu o próprio escopo, mesmo com boa intenção.

**E5 — Capacidade duplicada entre projetos é achado de portfólio, não culpa de projeto.**
*Consequência:* dois times construindo a mesma coisa de forma independente é sintoma de falta de
visibilidade compartilhada, não de erro de julgamento de qualquer um dos dois times.

**E6 — O inventário registra fato, não avalia mérito.** Um sistema registrado com dependência
concentrada não é automaticamente "errado" — é visível, e a decisão sobre se isso é aceitável
continua sendo humana, tomada por quem tem autoridade sobre portfólio.
