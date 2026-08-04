---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

Registrar a carga exata (concorrência, volume de dado) usada em toda medição, junto do resultado
— um percentil sem o contexto de carga que o produziu não é comparável com uma medição futura
feita sob condição diferente.

Revisar SLO de operação que envolve chamada de IA sempre que o modelo ou provedor por trás dela
mudar — a variabilidade de latência de um modelo novo pode ser bem diferente da que motivou a
margem original declarada em J6.

Tratar toda estratégia de sobrecarga declarada (J4) como testada sob condição real de sobrecarga
simulada, não apenas declarada em teoria — descobrir que a estratégia não funciona durante uma
sobrecarga real é o pior momento possível para essa descoberta.

Investigar regressão de desempenho antes de otimizar qualquer outra coisa — uma regressão não
investigada pode continuar piorando enquanto atenção vai para melhorias em outra área.


Manter um catálogo de cargas de referência padronizadas (baixa, média, pico) usadas
consistentemente em todas as medições de um mesmo sistema — comparar medições feitas sob cargas
arbitrariamente diferentes reduz a utilidade de qualquer comparação histórica ao longo do tempo.

Um catálogo pequeno de três ou quatro perfis de carga padronizados já cobre a maioria das comparações relevantes sem exigir infraestrutura de teste elaborada demais para manter.