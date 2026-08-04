---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Fidelidade média das respostas geradas, por período.** Fonte: medição pós-geração. Uma
tendência de queda ao longo do tempo, mesmo com fonte e índice estáveis, sinaliza que o passo de
geração está extrapolando mais — pode ser mudança de modelo, mudança de prompt, ou aumento de
complexidade das perguntas recebidas.

**Taxa de recusa explícita por falta de fonte suficiente**, sobre o total de perguntas. Fonte:
log do pipeline. Uma taxa muito baixa é tão suspeita quanto muito alta — pode significar que R4
não está sendo aplicado com rigor (o sistema "sempre acha algo" para responder) em vez de
refletir cobertura real da base de conhecimento.

**Proporção de candidatos descartados na etapa de confirmação de validade** (R6), sobre o total
de candidatos que sobreviveram à reordenação. Fonte: log de `confirmar_validade`. Uma proporção
alta sustentada sugere que a base de conhecimento tem muito documento expirando sem revalidação
correspondente — achado que aponta de volta para `11-KNOWLEDGE`, não para este volume.

**Diferença entre ranking de proximidade e ranking de relevância** para os mesmos candidatos, ao
longo de amostras de consulta. Fonte: comparação dos dois scores por candidato. Uma correlação
muito alta entre os dois rankings sugere que a etapa de reordenação pode não estar agregando
valor real sobre a ordem que o índice já devolveria sozinho.
