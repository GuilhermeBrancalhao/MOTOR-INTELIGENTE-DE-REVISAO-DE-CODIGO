---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 01-Introducao
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Introdução

Um sistema com componente de IA falha de formas que observabilidade tradicional (log de
requisição, métrica de latência, trace de chamada) não captura por completo: o modelo pode
responder com sucesso técnico (HTTP 200, sem excepção) e ainda produzir saída incorreta,
incoerente, ou fora do formato esperado pelo próximo consumidor — uma classe de falha que não
aparece em nenhuma métrica de infraestrutura convencional. Sem instrumentação desenhada
especificamente para essa classe, uma equipe opera o sistema "às escuras" na dimensão que mais
importa: não que ele está no ar, mas que está fazendo o que deveria fazer.

Este volume trata de três sinais que toda instrumentação de sistema com IA precisa capturar além
do básico de infraestrutura: taxa e motivo de encerramento não-ideal (um agente que termina por
orçamento excedido, um workflow que pausa por saída malformada — sinais definidos em
`08-AGENT-ENGINE` e `10-WORKFLOW`, mas cuja telemetria é assunto deste volume), taxa de
intervenção humana necessária (quanto do que o sistema decide autonomamente precisa de correção
ou aprovação — sinal de calibração, não de falha isolada), e latência e custo decompostos por
etapa de IA versus etapa determinística (porque otimizar a etapa errada desperdiça esforço).

A governança deste volume é irmã da de `17-SECURITY`, não sua substituta: aquele volume define o
que precisa ser *detectável* (um vetor de risco, uma tentativa de exfiltração); este volume
define como esse dado é *instrumentado e monitorado continuamente* em produção. Um controle de
segurança sem observabilidade correspondente é uma política que ninguém verifica estar
funcionando; observabilidade sem a taxonomia de risco de `17` mediria o sistema sem saber o que
de fato importa medir.
