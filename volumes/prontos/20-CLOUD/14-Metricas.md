---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de recursos com dono atribuído.** Deveria ser 100% por construção (N3 impede a
existência de recurso sem dono), então uma queda aqui indica falha no próprio processo de
declaração, não apenas descuido pontual.

**Número de recursos sem redundância para um alvo que a exige, ao longo do tempo.** Mede se N2
está sendo corrigido conforme identificado, ou apenas acumulando como lacuna conhecida e
ignorada.

**Frequência e magnitude de divergência (drift) detectada por ciclo de verificação.** Um número
crescente indica que mudanças estão acontecendo fora do fluxo declarado com frequência maior do
que o processo consegue absorver.

**Custo de infraestrutura sem atribuição clara de workload.** Complementa a proporção de recursos
com dono — um recurso pode ter dono nominal e ainda assim ter seu custo mal compreendido em
relação ao que efetivamente sustenta.


Estas quatro métricas, lidas em conjunto, revelam maturidade do processo de infraestrutura ao
longo do tempo — nenhuma delas isoladamente prova que a infraestrutura está bem administrada, mas
a combinação de dono sempre presente, redundância sem lacuna crescente e drift raro é o padrão
que indica disciplina sustentada, não apenas um bom momento pontual.

Nenhuma delas deveria ser lida isoladamente como aprovação ou reprovação de um período específico
— o valor está na tendência ao longo de vários ciclos de verificação, não no valor pontual de uma
única medição, que pode variar por razões incidentais sem refletir mudança real na disciplina de
infraestrutura.