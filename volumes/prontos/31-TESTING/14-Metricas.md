---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-07-30
---

# Métricas

| Métrica | Unidade | Fonte | Instrumentada neste volume? |
|---|---|---|---|
| Tempo de execução da suíte | segundos | saída de `python -m pytest exemplos/31-testing -q` | Sim -- `48 passed` em aproximadamente 0,1 s no ambiente de referência, variando por execução (medições entre 0,11 s e 0,14 s); o número não é usado como limiar de aprovação, só como sinal de que a suíte continua na camada unitária |
| Razão de testes parametrizados sobre o total de funções | percentual | contagem manual das funções decoradas com `@pytest.mark.parametrize` | Sim -- 7 de 23 (30%); ver `13-Testes.md` para a tabela por arquivo |
| Asserções por função de teste | contagem | revisão de código na abertura do pull request | Não -- é critério qualitativo de revisão (uma causa de falha isolável por teste), não um número que o gate calcula |
| Taxa de teste instável (flaky) | percentual de execuções que falham sem mudança de código | histórico de execução do pipeline de CI | Não -- este volume não tem pipeline de CI próprio; a instrumentação é responsabilidade de quem integra a suíte a um pipeline real |
| Tempo entre falha relatada e correção do teste | horas | histórico de commit/pull request | Não -- depende de processo de time, fora do que este componente pode medir isoladamente |
| Cobertura de branch dos três módulos | percentual | `coverage.py` (ferramenta externa, não integrada aos gates desta plataforma) | Não -- `ferramentas/` desta plataforma usa só biblioteca padrão; medir cobertura exige ferramenta de fora, e o resultado não é gate aqui |

## Por que a razão de parametrização é a métrica mais confiável desta lista

As duas primeiras linhas têm fonte verificável dentro deste próprio volume; as quatro
últimas dependem de infraestrutura que este volume não possui (pipeline de CI,
histórico de commit, ferramenta de cobertura). A razão de parametrização é a mais
robusta das duas instrumentadas porque não depende de hardware: contar decorators é
determinístico entre máquinas, enquanto o tempo de execução da suíte varia com a
velocidade do processador e a carga do sistema no momento da medição -- por isso o
tempo de execução é citado como referência, nunca como limiar de aprovação de nenhum
gate.

A ausência de cobertura de branch como métrica instrumentada não é lacuna esquecida --
é a fronteira declarada em `03-Escopo.md`: o indicador agregado de cobertura, sua
tendência ao longo do tempo e o gate de release baseado nele pertencem a
`32-QUALITY`, não a este volume.
