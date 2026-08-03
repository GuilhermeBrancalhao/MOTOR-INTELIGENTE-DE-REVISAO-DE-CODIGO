---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-03
---

# Boas Práticas

**Escrever o nome do teste antes de escrever o corpo dele.** Se o nome não consegue descrever a
violação específica que o teste previne, é sinal de que o teste ainda não tem foco claro — o
exercício de nomear primeiro força a pergunta "que regra exatamente isto protege?" antes de
qualquer código de teste existir.

**Guardar a mutação usada para provar um teste, mesmo que não permaneça no código de produção.**
Um comentário breve ("provado por mutação: trocar `and` por `or` na linha X quebra este teste")
custa pouco e preserva a evidência de que a prova foi feita, útil quando alguém revisita o teste
meses depois e precisa confiar nele sem repetir o trabalho.

**Escrever teste de fluxo completo depois que os testes de componente isolado já passam**, não
antes — testar composição antes de garantir que cada peça funciona isoladamente mistura duas
classes de bug (do componente, da composição) numa única falha difícil de diagnosticar.

**Revisar testes de caminho feliz periodicamente para promover os mais críticos a teste de
regressão de regra provado.** Um teste que começou como documentação de comportamento pode, com
o tempo, se revelar protegendo algo importante o suficiente para merecer a prova por mutação
formal.

**Tratar falha de teste depois de mudança de código como primeira hipótese "o código mudou de
forma que quebra a regra", não "o teste está desatualizado".** Ajustar o teste para o código
passar, sem investigar se a mudança de fato violou a regra original, é o caminho mais rápido para
uma suíte que documenta comportamento atual em vez de proteger invariante pretendida.
