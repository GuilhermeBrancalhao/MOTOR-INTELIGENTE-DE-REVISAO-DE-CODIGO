---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 02-Objetivos
status: PRONTO
atualizado_em: 2026-08-03
---

# Objetivos

Depois de ler este volume, o leitor consegue:

**Identificar sinais que só existem em sistema com IA** e não têm equivalente direto em
observabilidade de infraestrutura convencional — motivo de encerramento de agente, taxa de
validação de saída de IA reprovada, taxa de intervenção humana necessária — e explicar por que
"sucesso técnico da chamada" não é o mesmo que "resultado correto" nesse contexto.

**Decompor latência e custo por etapa de IA versus etapa determinística**, e explicar por que
essa decomposição orienta otimização de forma diferente: uma etapa de IA lenta pede revisão de
modelo/prompt (`27-LLM-ROUTER`, `07-PROMPT-ENGINE`); uma etapa determinística lenta pede revisão
de código ou infraestrutura convencional.

**Distinguir sinal que exige alerta imediato de sinal que só alimenta tendência agregada.** Nem
toda anomalia pontual justifica interromper alguém — a matriz de controles de `07-Regras.md`
formaliza o critério de quando um sinal cruza de "observar" para "agir".

**Aplicar granularidade de instrumentação proporcional ao custo de investigar sem ela.** Um passo
caro (chamada de IA longa) merece instrumentação mais fina do que um passo barato — não porque um
importa mais em abstrato, mas porque o custo de não saber onde o tempo/dinheiro foi gasto é maior
quando o passo em si já é caro.

**Traçar a fronteira com `17-SECURITY` e `14-Metricas.md` de cada volume individual**: este
volume trata da infraestrutura e disciplina geral de instrumentação; cada volume individual
(`08`, `09`, `10` etc.) já define quais métricas específicas do seu domínio existem — este volume
não repete essas listas, define como elas são coletadas e monitoradas de forma consistente.
