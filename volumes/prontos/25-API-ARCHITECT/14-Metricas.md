---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Número de mudanças de campo rejeitadas por `MudancaQuebraContrato` durante desenvolvimento.**
Um número alto indica que mudanças que quebrariam compatibilidade estão sendo tentadas com
frequência — vale investigar se versionamento de novo endpoint deveria ser considerado com mais
frequência em vez de tentar evoluir um contrato existente.

**Latência real observada por endpoint versus orçamento declarado (T6).** Um endpoint
consistentemente próximo ou acima do orçamento declarado é sinal de que o orçamento precisa ser
revisado ou que o endpoint precisa de otimização.

**Proporção de campos de resposta que passam por `traduzir_para_resposta` versus qualquer resposta
que bypassa essa camada.** Deveria ser 100% — qualquer resposta que não passa pela tradução é uma
violação potencial de T2.

**Tempo médio de vida de uma versão de contrato antes de ser descontinuada.** Contextualiza o
impacto de mudanças futuras — uma versão usada há muito tempo por muitos clientes exige mais
cautela ao ser descontinuada do que uma recém-lançada.


Estas quatro métricas, lidas em conjunto, ajudam a decidir quando uma nova versão de contrato é
necessária versus quando um ajuste pode ser feito dentro da versão atual — mudança rejeitada com
frequência é sinal de que uma nova versão provavelmente já deveria ter sido criada, em vez de
continuar tentando encaixar mudança incompatível na versão existente.