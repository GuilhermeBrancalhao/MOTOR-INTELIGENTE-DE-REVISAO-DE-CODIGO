---
volume: "34"
volume_nome: COST-OPTIMIZATION
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/34-cost-optimization/otimizacao_de_custo.py -->

`otimizacao_de_custo.py`, citado acima, formaliza U1-U6: `CustoDeTarefa.__post_init__` recusa
registro sem `tarefa` (U1) ou sem `escopo` (U2); `verificar_orcamento` retorna três estados
distintos com base no limiar de alerta configurável (U3); `detectar_tendencia_de_custo` exige
dois períodos no histórico antes de produzir resultado (U4); `validar_otimizacao_de_custo` rejeita
mudança sem redução real de gasto medido (U5); nenhuma constante de preço aparece em nenhum lugar
do módulo — todo valor numérico é parâmetro fornecido por quem chama (U6).

`RegistroDeCusto.total_por_escopo` filtra por igualdade exata de string de escopo, sem
normalização ou correspondência parcial — uma escolha deliberadamente simples que exige que quem
registra custo use o identificador de escopo de forma consistente, em vez de o sistema tentar
adivinhar correspondência aproximada entre nomes ligeiramente diferentes.

Essa simplicidade é uma escolha deliberada para o modelo mínimo deste exemplo, documentada aqui para que uma implementação real saiba exatamente onde adicionar normalização, se necessário.

Um sistema real que precisasse de correspondência aproximada teria que implementar essa lógica
explicitamente numa camada externa, nunca implicitamente dentro deste modelo mínimo, preservando
a simplicidade e a previsibilidade do comportamento de filtragem por escopo em todo o restante
do módulo, sem introduzir qualquer ambiguidade sobre qual registro pertence a qual escopo específico de negócio.