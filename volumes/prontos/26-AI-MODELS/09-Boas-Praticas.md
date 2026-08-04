---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Reavaliar candidatos ativos periodicamente contra os mesmos casos de ouro, não apenas na
seleção inicial — um modelo pode ter seu comportamento alterado pelo fornecedor sem aviso, e a
única forma de perceber é reavaliar.

Manter o requisito de capacidade da tarefa separado da lista de candidatos atuais — o requisito
muda raramente; a lista de candidatos que o atendem muda com frequência bem maior.

Tratar todo número de preço ou limite citado em documentação interna como teria data de validade
implícita — revisar antes de confiar, nunca assumir que um valor visto há meses ainda é real.

Testar o caminho de fallback ativamente, não apenas declará-lo — um fallback nunca exercitado
pode falhar silenciosamente no momento em que é de fato necessário.


Manter a lista de candidatos aprovados separada da configuração de qual candidato é "principal"
hoje — a primeira muda por avaliação; a segunda pode mudar por decisão operacional (custo,
disponibilidade) sem que uma nova avaliação seja necessária.

Documentar o motivo de cada avaliação reprovada, não apenas o resultado numérico — "reprovado"
sem contexto não ajuda a decidir se vale a pena reavaliar o mesmo candidato depois de um ajuste
de prompt ou configuração.

Esse contexto economiza tempo de investigação da próxima pessoa que revisitar a decisão.