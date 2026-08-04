---
volume: "28"
volume_nome: PROMPT-COMPILER
tipo: ENGINE
secao: 14-Metricas
status: PRONTO
atualizado_em: 2026-08-04
---

# Métricas

**Proporção de tentativas de compilação rejeitadas por prompt não promovido.** Um número acima de
zero em ambiente de produção indica tentativa de usar prompt que não deveria estar em uso real —
vale investigar a origem dessas tentativas.

**Diferença entre tokens estimados na compilação e tokens reais cobrados pelo provedor.** Mede a
precisão da estimativa usada para verificar orçamento — uma diferença sistemática indica que o
método de estimativa precisa de ajuste.

**Taxa de acerto de cache por ponto declarado.** Um ponto de cache raramente reaproveitado é
sinal de posicionamento ruim, mesmo que estruturalmente válido segundo Q5.

**Frequência de rejeição por variável ausente, por prompt.** Um prompt com rejeição recorrente
por essa causa pode indicar contrato mal comunicado a quem chama a compilação, não apenas
descuido pontual.


Estas quatro métricas, lidas em conjunto, ajudam a distinguir problema de contrato de prompt
(rejeição por variável ausente, recorrente) de problema de estimativa de token (diferença
sistemática contra o cobrado real) — dois problemas com causas e correções completamente
diferentes que uma métrica isolada poderia confundir.

Nenhuma delas substitui investigação direta de um caso específico — todas existem para direcionar onde investigar primeiro quando o volume de rejeições cresce de forma inesperada.

Uma mudança súbita em qualquer uma delas, sem explicação correspondente em mudança de prompt ou de provedor, merece investigação antes de ser assumida como ruído.