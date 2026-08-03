---
volume: "01"
volume_nome: FUNDACAO
tipo: GOVERNANCA
secao: 14-Metricas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Métricas

**Contagem de volumes por status** (`RASCUNHO`, `REQUER_REVISAO`, `PRONTO`), lida por
`ferramentas/status.py` a partir dos `_VOLUME.yml` materializados. Fonte: varredura do disco, não
estimativa. Em 2026-08-03, a contagem real era 3 `PRONTO`, 39 `RASCUNHO`, 0 `REQUER_REVISAO` — o
alvo do ciclo atual é 10 `PRONTO` (os essenciais), não 42, e a métrica deve refletir esse alvo
revisado, não o antigo.

**Violações do gate estrutural por execução de `validar --tudo`**, como indicador de saúde
agregada do acervo. O número por si só não diz se o acervo está pior ou melhor — subiu de 39 para
657 quando o BOM foi corrigido, e essa subida foi uma melhora (visibilidade real), não uma
regressão. A métrica só é útil lida junto com o que mudou desde a última medição, nunca isolada.

**Tempo entre `RASCUNHO` e `PRONTO` por volume**, medido pela diferença entre a primeira e a
última data de `atualizado_em` nos arquivos de seção. Útil para calibrar quanto uma auditoria de
novo volume deveria custar em tempo, mas enviesado pelos volumes que passaram por reescrita
completa (como `03-DISCOVERY`) versus os que nunca chegaram a ser escritos de fato.

**Proporção de volumes com auditoria registrada em `auditorias/` sobre volumes `PRONTO`** — se
esse número for menor que 1, existe volume `PRONTO` sem o critério 3 documentado, o que é uma
violação da Definição de PRONTO que o gate mecânico não detecta sozinho (porque a leitura da
linha `media:` só acontece quando o arquivo de auditoria existe; a ausência do arquivo não é
verificada automaticamente hoje — item registrado em `16-Roadmap.md`).
