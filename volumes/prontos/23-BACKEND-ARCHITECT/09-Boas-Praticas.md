---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Escolher a chave de idempotência a partir de algo que o cliente já possui de forma estável (um id
de requisição, um identificador de negócio), nunca gerada internamente sem relação com a
intenção original do cliente — senão a proteção contra duplicação não cobre o cenário mais comum
de duplicação real, que é o cliente reenviando a mesma solicitação.

Registrar o motivo de cada falha junto da tentativa, mesmo antes de decidir se ela vai esgotar o
limite de retry — o histórico de falhas de tentativas anteriores costuma ser mais informativo
para diagnóstico do que apenas o estado terminal final.

Testar backpressure sob carga simulada antes de depender dela em produção — um limite de
concorrência mal calibrado tanto pode rejeitar capacidade real disponível quanto pode falhar em
proteger o sistema, e os dois erros só aparecem sob volume real de requisições.

Tratar o limite de tentativas como configurável por tipo de trabalho, não um valor único global —
um trabalho barato de repetir tolera mais tentativas que um trabalho caro, e tratar os dois
igualmente desperdiça capacidade em um caso ou arrisca demais no outro.


Expor a contagem de tentativas consumidas junto do estado do trabalho, não apenas o estado final
— um trabalho concluído na primeira tentativa e um concluído na terceira tiveram experiências
muito diferentes, mesmo terminando no mesmo estado `CONCLUIDO`.