---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-03
---

# Exemplos

Os três casos abaixo usam um domínio inventado e neutro — uma loja que registra pedidos — para
que o padrão apareça sem depender de conhecer nenhum sistema específico.

## Caso 1 — teste nomeado pela violação, não pela função

O nome `test_dois_pedidos_de_mesmo_valor_em_dias_diferentes_nao_sao_duplicata` diz exatamente o
cenário que seria um bug se o teste falhasse: dois pedidos de valor igual, feitos em dias
diferentes, sendo tratados incorretamente como o mesmo pedido. Comparado a um nome genérico como
`test_guarda_caso_2`, o primeiro permite a qualquer leitor entender o que está sendo protegido
sem abrir o corpo do teste — e permite, na revisão de uma suíte inteira, avaliar cobertura de
regra por simples leitura dos nomes, que é o que `05-Diagramas.md` chama de rastreabilidade
regra-teste.

## Caso 2 — prova por mutação revelando teste decorativo

Um teste `test_bloqueia_pedido_duplicado` que só verifica "registrar a mesma chave duas vezes
devolve verdadeiro na segunda" pode passar mesmo se a implementação comparar apenas o valor,
ignorando data e cliente — porque o teste nunca exercitou o caso que distinguiria as duas
implementações (dois valores iguais, contextos diferentes). Mutar a implementação para comparar
só valor e rodar a suíte revelaria que esse teste específico não captura a regressão, mesmo
"parecendo" testar duplicata. É exatamente esse tipo de descoberta que a prova por mutação existe
para produzir antes que a regressão chegue a produção — e o Caso 1 mostra por que o nome importa:
o teste do Caso 1 não passaria pela mesma mutação, porque o cenário está no nome.

## Caso 3 — teste de fluxo completo capturando quebra de composição

Um teste que exercita cinco módulos na ordem real de uso — identificar o pedido, casar com o
registro existente, decidir a confiança do casamento, checar a guarda de duplicata e gravar na
trilha — captura uma classe de bug que nenhum teste unitário pega: a inversão acidental da ordem
entre a guarda e a trilha. Cada módulo, isolado, continua correto sob seus próprios testes; só a
composição exercitada na ordem certa revela se a integração entre eles preserva a garantia de não
gravar duas vezes. É a diferença entre "cada peça funciona" e "o conjunto faz o que promete".
