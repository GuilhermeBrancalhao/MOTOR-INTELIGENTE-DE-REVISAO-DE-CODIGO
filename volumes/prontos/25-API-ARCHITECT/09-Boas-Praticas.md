---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Documentar, junto de cada endpoint, exemplos de resposta de sucesso e de erro lado a lado — a
consistência de formato de erro (T3) só tem valor prático se for visível e fácil de conferir na
documentação, não apenas verdadeira no código.

Preferir adicionar campo novo a reaproveitar um campo existente quando o significado muda, mesmo
que pareça mais trabalho no curto prazo — a violação de T5 é normalmente mais barata de evitar na
hora de escrever do que de corrigir depois que clientes já dependem do significado antigo.

Revisar o orçamento de latência declarado periodicamente contra a latência real observada, não
apenas declarar uma vez e esquecer — um orçamento que nunca é revisitado tende a divergir da
realidade conforme o sistema evolui.

Versionar mesmo mudanças que parecem pequenas o suficiente para "não contar" — a decisão sobre o
que conta como mudança que quebra compatibilidade deveria ser conservadora, não uma aposta sobre
o que os clientes provavelmente não vão notar.


Manter um changelog de contrato separado do changelog de código interno, focado exclusivamente em
mudanças visíveis ao cliente — um changelog que mistura os dois obscurece o que de fato importa
para quem integra contra a API.