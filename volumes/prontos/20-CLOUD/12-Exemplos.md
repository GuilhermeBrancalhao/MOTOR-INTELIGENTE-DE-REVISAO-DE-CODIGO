---
volume: "20"
volume_nome: CLOUD
tipo: ARQUITETURA
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-08-04
---

# Exemplos

## Caso 1 — recurso declarado corretamente

Um banco de dados de produção é declarado com dono atribuído, ambiente "producao" e
`redundante=True`. A declaração é aceita sem ressalva.

## Caso 2 — redundância ausente para alvo crítico

O mesmo tipo de recurso, mas `redundante=False`, avaliado contra um alvo de disponibilidade que
exige redundância. A verificação retorna esse recurso na lista de lacunas — a ausência de
redundância é visível antes de virar incidente, não descoberta durante um.

## Caso 3 — segredo inline rejeitado antes da declaração

Uma configuração bruta contém a chave `"senha": "abc123"` diretamente. `validar_config_sem_segredo`
rejeita essa configuração antes que qualquer `Recurso` seja construído a partir dela — o segredo
nunca chega a fazer parte do estado declarado versionado.

## Caso 4 — mudança isolada por ambiente

Uma mudança preparada para um recurso de staging é aplicada, por engano, tentando alvo
"producao". `PlanoDeInfraestrutura.aplicar_mudanca` rejeita a operação porque o ambiente da
mudança não corresponde ao do recurso — nenhuma alteração indevida chega a produção.

## Caso 5 — drift detectado quando o real diverge do declarado

O estado declarado diz que um recurso é redundante; o estado real observado mostra que não é —
talvez alterado manualmente fora do fluxo declarado. `detectar_drift` reporta essa divergência
especificamente, nomeando o recurso e o campo que diverge.


Os cinco casos cobrem, juntos, as quatro regras verificáveis por operação isolada (N2 a N5) mais
duas variações de N6 — a mesma cobertura que a suíte de testes da seção seguinte confirma caso a
caso, incluindo o caso negativo em que a comparação não deveria reportar problema nenhum.