---
volume: "29"
volume_nome: PROMPT-OPTIMIZER
tipo: ENGINE
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — variante com melhoria significativa é proposta

Um candidato com taxa de acerto claramente acima do baseline, além do limiar mínimo, se torna a
proposta retornada pela busca.

## Caso 2 — melhoria marginal não é suficiente

Um candidato com taxa de acerto ligeiramente maior que o baseline, mas dentro da margem de ruído
declarada, não é considerado proposta — a busca continua tentando outros candidatos, ou termina
sem propor nada se nenhum superar o limiar.

## Caso 3 — busca respeita o orçamento de tentativas

Um gerador de candidatos com mais itens do que `max_tentativas` permite é interrompido no limite
configurado — os candidatos restantes nunca chegam a ser avaliados.

## Caso 4 — toda tentativa, aprovada ou não, aparece no histórico

Após uma busca com múltiplos candidatos, o histórico contém uma entrada para cada um avaliado,
independente de ter se tornado a proposta final ou não.

## Caso 5 — mesma amostra usada do início ao fim

Capturando os argumentos passados a `avaliar_variante` ao longo de uma busca completa, a mesma
tupla `casos_de_ouro` aparece em toda chamada — baseline e cada candidato, sem exceção.


Os cinco casos cobrem, juntos, o espectro completo de resultado possível de uma busca: proposta
encontrada, nenhuma proposta encontrada, orçamento esgotado antes de todos os candidatos, e a
garantia de que a amostra usada nunca varia — a mesma cobertura que os testes da seção seguinte
verificam individualmente.

Essa cobertura completa reduz a chance de uma regressão futura passar despercebida, porque qualquer mudança que quebre uma das seis regras provavelmente também muda o resultado de pelo menos um desses cinco casos.