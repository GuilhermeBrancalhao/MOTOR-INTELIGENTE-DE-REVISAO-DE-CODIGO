---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`RequisitoDeCapacidade` declara o que uma tarefa exige de um modelo — janela de contexto mínima,
modalidade, tolerância de latência — antes de qualquer candidato ser considerado. `CandidatoDeModelo`
só é aprovado se atender esse requisito e tiver `ResultadoDeAvaliacao` contra casos de ouro acima
do limiar configurado — `aprovado()` levanta exceção explícita se a avaliação nunca aconteceu,
tornando "nunca avaliado" estruturalmente distinto de "avaliado e aprovado".

`PlanoDeTarefa` liga uma tarefa a um modelo principal e um modelo de fallback — `validar_plano`
recusa um plano sem fallback declarado. `comparar_custo_por_tarefa` calcula o custo total da
tarefa (tokens de entrada e saída multiplicados por tentativas) em vez de comparar preço unitário
isoladamente, o que é a diferença central entre este modelo e uma comparação ingênua de tabela de
preço.

`registrar_troca` é o único caminho para substituir o modelo de uma tarefa — nenhuma substituição
acontece fora dessa operação nomeada, o que torna toda troca rastreável a uma entrada de
histórico com data, motivo e avaliação que a justificou.


Nenhum desses tipos centrais (`RequisitoDeCapacidade`, `CandidatoDeModelo`, `PlanoDeTarefa`,
`CustoPorTarefa`) contém um valor de preço ou nome de modelo fixo no próprio código — todos são
parâmetros fornecidos por quem chama, o que é a implementação direta de M5 dentro da própria
arquitetura, não apenas uma promessa em prosa.