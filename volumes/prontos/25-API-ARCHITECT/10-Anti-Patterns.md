---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Serializar o objeto de persistência interno diretamente como resposta HTTP.** É exatamente o
atalho que T2 existe para evitar — qualquer mudança de schema interno vira, sem intenção,
mudança de contrato externo.

**Reaproveitar um campo de resposta existente para um significado novo, sob a justificativa de
"é essencialmente a mesma coisa".** Viola T5 mesmo quando o tipo do campo não muda — o cliente que
confiava no significado antigo recebe dado incorreto sem nenhum sinal de que algo mudou.

**Cada endpoint com seu próprio formato de erro, evoluído independentemente ao longo do tempo.**
Força o cliente a escrever tratamento de erro específico por endpoint, multiplicando esforço de
integração sem benefício correspondente.

**Cliente obrigado a fazer polling com intervalo adivinhado, porque o endpoint de status não
documenta frequência de consulta recomendada.** Viola o espírito de T4 mesmo quando o recurso de
status tecnicamente existe — "consultável" implica uma política de consulta razoável, não apenas
a existência de um endpoint.

**Endpoint síncrono sem orçamento de latência declarado, cuja duração real só é descoberta pelo
cliente em produção.** É exatamente o cenário que T6 existe para prevenir.


**Corrigir um "bug" de resposta simplesmente removendo um campo que estava incorreto, sem
considerar que clientes já dependem dele.** Mesmo um campo com valor errado pode ter clientes que
dependem de sua presença estrutural — removê-lo é uma mudança que quebra contrato tanto quanto
mudar seu tipo.