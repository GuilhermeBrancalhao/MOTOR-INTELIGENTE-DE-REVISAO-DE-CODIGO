---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`declarar_operacao_pronta` recusa aceitar uma operação sem `SLO` e sem `PoliticaDeSobrecarga`
declarados — ambos são condições de prontidão, verificadas juntas antes de a operação ser
considerada pronta para produção.

`MedicaoDeCarga` carrega `concorrencia` junto das amostras de latência — `verificar_slo` recusa
uma medição com concorrência abaixo de um mínimo realista antes mesmo de calcular percentil,
porque uma medição sob carga insuficiente não representa comportamento de produção.

`SLO.__post_init__` recusa um SLO marcado como `envolve_chamada_de_ia=True` cujo `p99_ms` não seja
estritamente maior que `p95_ms` — a variabilidade da chamada de IA precisa estar refletida na
própria margem entre os dois percentis, não apenas mencionada em texto.

`validar_otimizacao` compara medição antes e depois de forma explícita — uma otimização sem
melhoria mensurável no percentil relevante é rejeitada, independente de quão razoável a mudança
pareça em teoria.


Nenhum desses quatro componentes assume que uma mudança é boa por argumento teórico — cada
verificação exige um número concreto, medido, antes de aceitar qualquer afirmação sobre
desempenho como verdadeira. Essa disciplina de exigir prova numérica atravessa toda a arquitetura
deste volume, do SLO declarado até a otimização validada.

Essa exigência estrutural de prova numérica é o que distingue este processo de um julgamento subjetivo sobre se algo está rápido o suficiente ou não.