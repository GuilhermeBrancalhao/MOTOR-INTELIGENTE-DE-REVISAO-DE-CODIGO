---
volume: "22"
volume_nome: FRONTEND-ARCHITECT
tipo: ARQUITETURA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-04
---

# Roadmap

## O que este volume ainda não cobre

Retry automático de fragmento perdido dentro de um stream em andamento (hoje uma falha de rede no
meio de um stream é tratada como falha da requisição inteira, não como perda pontual
recuperável).

Política de expiração para o cache usado em fallback (F3) — hoje o exemplo assume que o cache
anterior está disponível, sem modelar quando ele deveria deixar de ser considerado válido para
uso como fallback.

Coordenação entre múltiplas requisições de IA concorrentes no mesmo componente (por exemplo,
usuário dispara uma nova ação antes da anterior terminar) — hoje cada `RequisicaoDeIA` é
independente, sem modelar a política de "cancelar a anterior automaticamente" versus "permitir
ambas em paralelo".

## Ordem de cobertura pretendida

Primeiro, o modelo de referência mínimo (ciclo de vida da requisição, resolução de exibição,
escopo de estado, adaptação de provedor), testado por mutação nas seis regras. Depois,
integração real com o contrato do `25-API-ARCHITECT` como fonte concreta da resposta.

## O que este volume assume que pode mudar

O modelo de cinco estados (`EstadoCarregamento`) é o mínimo suficiente hoje — um esquema mais
granular (por exemplo, distinguir "conectando" de "recebendo primeiro fragmento") pode ser
necessário conforme a interface fica mais sofisticada, sem alterar o princípio central de estado
explícito e transição auditável.
