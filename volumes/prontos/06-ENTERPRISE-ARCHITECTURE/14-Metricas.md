---
volume: "06"
volume_nome: ENTERPRISE-ARCHITECTURE
tipo: ARQUITETURA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de sistemas registrados no inventário sobre o total de sistemas com componente de IA
conhecidos.** Fonte: comparação entre inventário e outra fonte independente (por exemplo,
faturamento de fornecedor de IA). Uma proporção baixa é o sintoma mais direto de invisibilidade
de portfólio — sistemas existem e não aparecem no único lugar que deveria enxergá-los.

**Número de fornecedores distintos por categoria de capacidade equivalente.** Fonte: agrupamento
do inventário por categoria. Um número alto sugere fragmentação sem coordenação; um número
baixo demais pode sugerir concentração de risco não decidida — a métrica não tem direção "boa"
única, precisa ser lida junto com a decisão de portfólio que a acompanha.

**Tempo entre registro de dependência com sinalização e decisão de portfólio correspondente.**
Fonte: timestamps do inventário. Um tempo muito longo significa que sinalização vira ruído
ignorado — a mesma lógica de fadiga de alerta que `21-OBSERVABILITY` trata para sinal técnico
se aplica aqui a sinal de portfólio.

**Custo total de propriedade agregado por fornecedor, ao longo do tempo.** Fonte:
`custo_total_agregado`. A leitura útil não é o valor absoluto num ponto, é a tendência — um
fornecedor cujo custo agregado cresce mais rápido que o número de projetos que o usam sinaliza
mudança de termos que merece revisão, mesmo sem nenhum projeto novo entrando.
