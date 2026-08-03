---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 02-Objetivos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Escrever um teste que corresponde a uma regra específica**, não a um caminho de execução
genérico — e nomear o teste de forma que o nome sozinho diga qual regra está sendo protegida
(o padrão usado em todo este acervo: `test_valores_redondos_repetidos_em_dias_diferentes_nao_sao_duplicata`
diz o que a violação seria, não só "test_guarda_2").

**Aplicar prova por mutação a um teste existente**: alterar o código de propósito para violar a
regra alvo, confirmar que o teste falha, e reverter a alteração — como verificação de que o teste
não é decorativo, é ancorado na regra que afirma proteger.

**Diferenciar teste de caminho feliz de teste de regressão de regra.** Ambos têm valor, mas
servem propósitos diferentes: o primeiro documenta comportamento esperado; o segundo travamento
específico impede que uma violação conhecida reapareça sem ser notada.

**Organizar testes por regra, não só por função testada.** Quando uma seção `07-Regras.md` lista
N invariantes, a suíte correspondente deveria ter rastreabilidade clara de qual teste prova qual
invariante — não uma coleção de testes onde essa correspondência precisa ser reconstruída por
inspeção.

**Traçar a fronteira com `32-QUALITY`**: este volume é a prática (como testar); `32` é o indicador
agregado (cobertura, tendência, gate de release) que mede se a prática está de fato acontecendo
em escala, ao longo do tempo, não em cada teste individual.
