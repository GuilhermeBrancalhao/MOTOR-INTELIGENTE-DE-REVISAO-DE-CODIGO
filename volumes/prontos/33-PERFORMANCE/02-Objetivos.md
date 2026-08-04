---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-04
---

# Objetivos

Declarar um alvo de latência (SLO) explícito para toda operação exposta a cliente, antes de ela
ser considerada pronta para produção — nunca inferido depois, a partir do que o sistema já faz.

Medir desempenho sob carga realista — concorrência e volume de dado que se aproximam da
produção — nunca apenas em ambiente isolado que não revela contenção de recurso real.

Investigar toda regressão de desempenho com o mesmo rigor que se investigaria uma regressão de
qualidade — nunca descartada como "provavelmente só ruído" sem verificação.

Degradar graciosamente sob sobrecarga — rejeitar, aplicar backpressure, ou retornar resultado
parcial — em vez de falhar catastroficamente para toda requisição quando a capacidade é excedida.

Validar toda otimização por medição antes e depois, nunca assumida como tendo funcionado só
porque a mudança "parece" mais rápida.

Os cinco objetivos formam uma cadeia de confiança: declarar SLO (primeiro) só tem valor se medido
sob carga real (segundo); medir sob carga real só tem valor se regressão for de fato investigada
(terceiro); e nenhuma dessas três coisas substitui degradação graciosa (quarto), que protege o
sistema mesmo quando o SLO já foi violado por sobrecarga inesperada. Validação por medição
(quinto) fecha o ciclo, garantindo que qualquer correção proposta seja provada, não presumida.