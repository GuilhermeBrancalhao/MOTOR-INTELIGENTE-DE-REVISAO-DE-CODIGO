---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-03
---

# Anti-Patterns

**Medir qualidade de suíte só por cobertura percentual, sem verificar se os testes de fato
travam regressão.** Cobertura alta com testes que nunca foram provados por mutação mede quanto
código foi executado durante o teste, não quanto comportamento está protegido — as duas coisas
parecem relacionadas e não são.

**Nomear teste pela função testada em vez da regra protegida** (`test_processar`,
`test_validar_2`). Esse padrão de nome não sobrevive a releitura futura — quem lê não sabe, sem
abrir o corpo do teste, qual violação específica ele deveria capturar.

**Ajustar o teste para acomodar uma mudança de código sem verificar se a mudança violou a regra
original.** Esse é o anti-padrão mais silenciosamente perigoso: a suíte continua "verde", mas
pode estar verde porque parou de proteger algo que deveria proteger, não porque o código está
correto.

**Testar só componente isolado, nunca a composição na ordem real de uso.** Um sistema com vários
componentes que interagem em ordem específica pode ter cada componente perfeito isoladamente e
ainda quebrar na composição — a ausência de teste de fluxo completo é lacuna que só aparece
quando já é tarde, em produção.

**Escrever teste depois de já saber que o código passa, sem nunca ter visto o teste falhar.** Um
teste que nunca foi observado falhando (nem contra código incorreto, nem por mutação deliberada)
carrega risco real de estar testando algo trivial ou de ter um bug que sempre retorna sucesso,
mascarado pela ausência de qualquer caso que o exercitasse de verdade.
