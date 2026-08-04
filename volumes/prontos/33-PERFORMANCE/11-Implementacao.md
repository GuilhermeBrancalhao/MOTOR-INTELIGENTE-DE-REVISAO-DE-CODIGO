---
volume: "33"
volume_nome: PERFORMANCE
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/33-performance/orcamento_de_desempenho.py -->

`orcamento_de_desempenho.py`, citado acima, formaliza J1-J6: `declarar_operacao_pronta` recusa
operação sem `SLO` (J1) ou sem `PoliticaDeSobrecarga` (J4); `verificar_slo` recusa medição com
concorrência abaixo do mínimo realista antes de calcular percentil (J2);
`detectar_regressao_de_performance` compara p95 entre duas medições, produzindo objeto explícito
quando piora (J3); `validar_otimizacao` rejeita mudança sem melhoria mensurável no percentil
comparado sob a mesma carga (J5); `SLO.__post_init__` rejeita `envolve_chamada_de_ia=True` sem
margem entre `p95_ms` e `p99_ms` (J6).

`MedicaoDeCarga.percentil` ordena as amostras e usa índice truncado, não interpolado — uma
simplificação deliberada para o modelo mínimo deste exemplo, suficiente para provar as seis
regras sem a complexidade adicional de interpolação estatística entre pontos vizinhos da amostra
ordenada.

Um sistema real, com volume de amostra muito maior, provavelmente se beneficiaria de um cálculo de percentil mais preciso, mas o princípio de comparação entre duas medições sob a mesma carga permanece idêntico independente dessa escolha de implementação.

A troca futura para um cálculo mais sofisticado, se necessária, afetaria apenas `percentil`, sem
exigir mudança em nenhuma das seis regras nem nos testes que as verificam, porque todas elas
dependem apenas do contrato público da função, nunca de sua implementação interna específica de
cálculo estatístico de percentil, que continua livre para evoluir de forma isolada e independente.