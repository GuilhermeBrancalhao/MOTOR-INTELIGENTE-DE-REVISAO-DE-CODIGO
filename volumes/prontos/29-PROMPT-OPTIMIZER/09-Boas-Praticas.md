---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Revisar o histórico completo de uma busca, não apenas a proposta vencedora, antes de decidir
submetê-la ao 07 — o padrão de quais variantes falharam pode revelar algo sobre a direção da
busca, não apenas sobre o resultado final.

Calibrar o limiar de melhoria mínima (O2) contra o tamanho real da amostra de casos de ouro — uma
amostra pequena tem variação estatística maior, exigindo um limiar mais conservador para não
confundir ruído com sinal.

Registrar, junto da proposta submetida ao 07, a referência à busca completa que a gerou — a
rastreabilidade entre "esta versão foi proposta por busca automática" e o histórico que a
justificou é informação valiosa para quem revisa a promoção depois.

Testar o gerador de candidatos separadamente da lógica de avaliação — os dois têm motivos de
falhar completamente diferentes, e misturar os dois numa mesma investigação de bug custa mais
tempo do que precisa.


Documentar a estratégia de geração de candidato usada em cada busca junto do histórico
resultante — mesmo que a estratégia em si seja externa a este volume, saber como os candidatos
foram gerados ajuda a interpretar por que a busca encontrou (ou não encontrou) melhoria.

Essa documentação não precisa ser extensa — o nome da estratégia e uma referência ao código que a implementa já ajudam consideravelmente.