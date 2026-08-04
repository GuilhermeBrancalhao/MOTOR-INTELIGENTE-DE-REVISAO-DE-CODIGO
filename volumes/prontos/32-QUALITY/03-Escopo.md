---
volume: "32"
volume_nome: QUALITY
tipo: PROCESSO
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-04
---

# Escopo

Este volume cobre o indicador agregado de qualidade: taxa de prova por mutação, gate de release,
registro de dívida técnica, tendência ao longo do tempo, e detecção de regressão.

**Fronteira com `31-TESTING`.** Como se escreve, organiza e mantém teste — nome de teste, prova
por mutação individual, teste de fluxo completo — é daquele volume. Este volume trata do que se
faz com o resultado agregado de toda essa prática: um número (ou conjunto de números nomeados)
usado para decidir release e acompanhar tendência.

**Fronteira com `33-PERFORMANCE`.** Qualidade, aqui, trata de correção verificada por prova de
regra — não de característica de desempenho (latência, throughput). Um sistema pode ter alta taxa
de prova por mutação e ainda ser lento; as duas dimensões são independentes e cada uma tem seu
próprio volume.

**Fronteira com `18-DEVSECOPS`.** O gate de segurança daquele volume e o gate de qualidade deste
volume são etapas paralelas e independentes do mesmo pipeline (`19-DEVOPS`) — uma mudança pode
passar em segurança e falhar em qualidade, ou o contrário, e cada gate tem sua própria lógica de
bloqueio.

Não cobre ferramenta específica de medição de cobertura — os princípios deste volume (indicador
por prova, gate com piso declarado, dívida registrada, tendência acompanhada) valem
independentemente de qual ferramenta calcula os números.
