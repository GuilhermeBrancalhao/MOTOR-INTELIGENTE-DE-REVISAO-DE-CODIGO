---
volume: "26"
volume_nome: AI-MODELS
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/26-ai-models/selecao_de_modelo.py -->

`selecao_de_modelo.py`, citado acima, formaliza M1-M6: filtro por requisito de capacidade
precede avaliação (M1); `CandidatoDeModelo.aprovado` levanta `ModeloNaoAvaliado` se chamado antes
de uma avaliação existir (M2); `validar_plano` rejeita `PlanoDeTarefa` sem `modelo_fallback`
(M3); `comparar_custo_por_tarefa` calcula custo total, não preço unitário (M4); nenhum preço ou
nome de modelo é hardcoded no módulo — todo valor numérico é parâmetro fornecido por quem chama
(M5); `registrar_troca` é o único caminho para adicionar uma entrada ao histórico de substituição
(M6).

Nenhuma constante de módulo em `selecao_de_modelo.py` representa preço, limite de contexto ou
nome de modelo — todo valor desse tipo entra como argumento de função ou campo de dataclass
fornecido no momento do uso, nunca como padrão hardcoded que envelheceria junto com o código.
Essa é a aplicação literal de M5: o método é fixo, os números não são.

Isso é o oposto de um exemplo que, por conveniência, fixasse um preço de ilustração direto no
corpo do código — mesmo como exemplo, esse hábito treina o leitor a aceitar número fixo como
normal, exatamente o que a regra de volume perecível pede para evitar.

Nenhuma exceção a essa disciplina existe em nenhuma parte deste módulo — nem mesmo nos testes,
que também recebem seus valores numéricos como argumento explícito em vez de constante global.