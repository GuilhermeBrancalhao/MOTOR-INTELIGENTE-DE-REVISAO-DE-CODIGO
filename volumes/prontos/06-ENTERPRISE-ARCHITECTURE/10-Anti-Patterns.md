---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Exigir aprovação de portfólio para toda decisão técnica de projeto.** Isso trata `03-Escopo.md`
como se dissesse o oposto do que diz — a maioria das decisões nunca deveria chegar ao portfólio,
e um processo que trata todas como candidatas produz a lentidão que a fronteira deste volume
existe para evitar.

**Manter inventário que ninguém consulta.** Um registro de dependência que existe só para
satisfazer uma exigência de auditoria, sem ninguém de fato usando para achar concentração ou
duplicação, tem o custo de manutenção sem nenhum dos benefícios.

**Confundir sistema registrado com sistema aprovado.** O inventário registra fato (E6); tratar
registro como aprovação automática de mérito remove a etapa humana de julgamento que decisões de
portfólio de fato exigem.

**Medir custo total de propriedade só na aprovação inicial do projeto, nunca de novo.** Um
fornecedor que muda de preço um ano depois da aprovação original não aparece em nenhuma análise
se o cálculo nunca é refeito — o TCO agregado precisa de revisão periódica, não só de aprovação
única.

**Deixar a detecção de duplicação depender de alguém lembrar qual projeto faz o quê.** Sem
inventário estruturado, a detecção de capacidade duplicada vira dependente de memória informal de
quem já está há tempo suficiente na empresa para ter visto os dois projetos — e essa pessoa nem
sempre existe ou está disponível.
