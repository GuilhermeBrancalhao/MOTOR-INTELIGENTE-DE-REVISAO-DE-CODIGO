---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-03
---

# Boas Práticas

**Declarar o formato de saída esperado de todo passo de IA de forma explícita e verificável**,
nunca como "texto livre que o próximo passo vai interpretar como conseguir" — um schema
explícito é o que permite ao motor validar automaticamente, sem depender de o passo seguinte
tratar dado malformado por conta própria.

**Preferir passo determinístico sempre que a tarefa não exigir interpretação de texto livre ou
decisão ambígua.** Um passo de IA custa mais (latência, tokens, variabilidade) do que uma
transformação de dados direta — reservar IA para onde ela é de fato necessária mantém o workflow
mais previsível e mais barato de operar.

**Gravar checkpoint granular o suficiente para retomar sem reprocessar trabalho caro.** Se um
passo é caro (por exemplo, uma chamada de IA longa), o checkpoint deveria capturar seu resultado
imediatamente após conclusão, não esperar o fim de um grupo de passos — quanto mais fino o
checkpoint, menos trabalho é perdido numa falha.

**Tratar `AguardandoSinal` e `Pausado` como estados operacionalmente diferentes na
observabilidade**, mesmo que ambos "parem" a execução — o primeiro é esperado; o segundo é sinal
de atenção necessária, e tratar os dois com o mesmo alerta esconde qual dos dois realmente
precisa de ação humana imediata.

**Limitar o número de tentativas de correção automática para saída de IA malformada, com queda
para pausa depois do limite.** Deixar o ciclo de correção automática irrestrito pode consumir
tempo e tokens indefinidamente sem garantia de convergência — um limite explícito, seguido de
pausa para intervenção, é o comportamento seguro por padrão.
