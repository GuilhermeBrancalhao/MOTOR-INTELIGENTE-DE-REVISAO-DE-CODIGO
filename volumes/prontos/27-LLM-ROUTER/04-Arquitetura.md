---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 04-Arquitetura
status: PRONTO
atualizado_em: 2026-08-04
---

# Arquitetura

`JanelaDeSaude.esta_degradado` recebe um `SinalDeSaude` agregado (total de chamadas, falhas,
latência média) e só julga degradação quando o volume de chamadas na amostra atinge um mínimo —
abaixo disso, retorna sempre "não degradado", tornando uma falha isolada estruturalmente incapaz
de disparar fallback sozinha.

`Roteador.rotear` mantém `estado_atual` por tarefa — qual candidato está ativo agora — e
`chamadas_consecutivas_saudaveis_apos_fallback`, o contador que implementa a janela de
estabilidade: uma vez em fallback, o roteador só volta ao principal depois de uma sequência de
sinais saudáveis consecutivos, nunca no primeiro sinal positivo isolado.

Toda chamada a `rotear` recusa candidato fora do conjunto `candidatos_aprovados`, recebido de
fora (representando a saída do 26) — o roteador nunca decide, por conta própria, que um modelo
não aprovado é aceitável só porque está disponível.

Cada decisão retornada por `rotear` também é acrescentada ao `historico` do roteador, com a
tarefa, o candidato escolhido e o motivo — nenhuma decisão é tomada sem deixar rastro.


Nenhum desses componentes mantém referência direta a um provedor de IA específico — toda a lógica
opera sobre nomes de candidato como string opaca e sinal de saúde agregado, o que mantém o
roteador testável e neutro a fornecedor, alinhado à regra de volume perecível.

Essa separação de responsabilidade — histórico como lista simples, estado atual como mapa consultável — evita que a mesma estrutura de dado precise servir dois propósitos diferentes ao mesmo tempo.