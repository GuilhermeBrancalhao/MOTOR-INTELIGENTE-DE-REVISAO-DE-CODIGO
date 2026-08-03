---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 10-Anti-Patterns
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Anti-Patterns

**Tratar "a chamada ao modelo teve sucesso" como sinal suficiente de qualidade.** Esse é o erro
mais específico de sistemas com IA na observabilidade: uma chamada sem erro técnico pode ainda
produzir conteúdo incorreto, incoerente, ou fora do formato esperado — instrumentação que só olha
sucesso de chamada nunca detecta essa classe de falha.

**Fixar limiar de alerta por número redondo escolhido sem observação real** ("mais de 10 erros
por hora" sem nunca ter medido a taxa real de erro esperada). Isso produz alertas desalinhados
com a criticidade real — tanto alertas em excesso para variação normal quanto silêncio para
anomalia real, dependendo de qual lado do número redondo o comportamento real do sistema cai.

**Agregar custo e latência de etapa de IA e determinística num único número sem decomposição.**
Um painel que mostra só "tempo total do workflow" sem separar quanto veio de decisão de modelo
versus execução de código orienta investigação para o lugar errado quando o tempo sobe.

**Assumir que o canal de alerta nunca falha.** Um sistema que confia inteiramente no canal de
notificação sem verificação periódica de que ele está de fato entregando mensagens corre o risco
real de operar "cego" por período indeterminado sem que ninguém saiba — a falha do canal é
silenciosa por natureza, o que a torna mais perigosa que a falha do sinal em si.

**Recalibrar limiar para "parar de alertar" sem investigar se o alerta estava certo.** Um alerta
frequente pode ser sintoma de comportamento real do sistema que precisa de correção, não de
limiar mal calibrado — ajustar o número sem essa investigação prévia troca visibilidade de um
problema real por silêncio confortável.
