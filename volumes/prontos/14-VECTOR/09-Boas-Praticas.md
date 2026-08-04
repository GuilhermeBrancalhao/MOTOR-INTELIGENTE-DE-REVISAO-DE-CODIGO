---
volume: "14"
volume_nome: VECTOR
tipo: ENGINE
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-08-04
---

# Boas Práticas

**Tratar mudança de modelo de embedding como evento de reindexação completa, nunca como migração
incremental que mistura versões.** A tentação de reindexar só os documentos alterados desde a
última mudança de modelo produz um índice com duas versões coexistindo, que é exatamente o que
V1 proíbe.

**Declarar métrica no momento da criação do índice, não deixar como configuração ajustável em
tempo de consulta.** Métrica é propriedade do espaço vetorial, não da consulta individual —
permitir que cada consulta escolha métrica livremente sugere que qualquer métrica funciona com
qualquer índice, o que não é verdade.

**Nomear partição por domínio de conteúdo, não por conveniência técnica de infraestrutura.** Uma
partição chamada "índice-2" não comunica nada sobre o que ela isola; uma partição chamada
"documentos-rh" torna o cruzamento acidental mais fácil de perceber quando acontece.

**Medir o tempo de reindexação completa antes de precisar dele em produção.** Uma mudança de
modelo de embedding em sistema grande pode levar horas para reindexar — descobrir isso pela
primeira vez durante um incidente é pior do que medir com antecedência.

**Reter o índice antigo por um período após a troca atômica**, não descartar imediatamente. Se o
índice novo tiver um problema não detectado na validação, reter o antigo permite reverter sem
reconstruir do zero.
