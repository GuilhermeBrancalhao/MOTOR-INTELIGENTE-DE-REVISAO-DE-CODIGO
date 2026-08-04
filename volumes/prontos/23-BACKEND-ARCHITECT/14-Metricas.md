---
volume: "23"
volume_nome: BACKEND-ARCHITECT
tipo: ARQUITETURA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Tempo médio entre enfileiramento e retirada por um worker.** Mede se a capacidade de
processamento está acompanhando a demanda, sinal direto de quando backpressure (S3) precisa ser
ajustada.

**Proporção de trabalhos que se recuperam via retry versus os que terminam em
FALHOU_PERMANENTEMENTE.** Um número crescente de falha permanente pode indicar problema
sistemático, não apenas falhas isoladas absorvidas normalmente pela política de retry.

**Número de rejeições por backpressure (`CapacidadeInsuficiente`) ao longo do tempo.** Rejeição
zero constante pode indicar capacidade superdimensionada; rejeição frequente pode indicar
capacidade insuficiente para a demanda real — os dois extremos merecem investigação.

**Distribuição de tentativas consumidas por trabalho concluído com sucesso.** Um trabalho que
sistematicamente só é bem-sucedido na última tentativa permitida é diferente, para fins de
diagnóstico, de um que quase sempre é bem-sucedido na primeira.


Lidas em conjunto, essas quatro métricas revelam se o sistema está dimensionado corretamente para
a demanda real: tempo de espera crescente junto de rejeição por backpressure indica capacidade
insuficiente; falha permanente crescente sem rejeição por backpressure indica problema na lógica
de processamento em si, não na capacidade disponível.

Nenhuma dessas métricas deveria disparar uma ação automática sozinha — elas existem para orientar
decisão humana sobre ajuste de capacidade, política de retry ou investigação de causa raiz, não
para acionar reconfiguração automática sem revisão, que poderia amplificar um problema mal
diagnosticado em vez de corrigi-lo.