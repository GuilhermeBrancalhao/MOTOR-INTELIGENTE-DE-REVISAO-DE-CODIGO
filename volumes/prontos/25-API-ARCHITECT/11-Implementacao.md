---
volume: "25"
volume_nome: API-ARCHITECT
tipo: ARQUITETURA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/25-api-architect/contrato_api.py -->

`contrato_api.py`, citado acima, formaliza T1-T6: `ContratoDeEndpoint.declarar_campo` rejeita
mudança de tipo de campo sob a mesma versão (T1/T5); `traduzir_para_resposta` só inclui campos
explicitamente permitidos, nunca o registro interno inteiro (T2); `ErroDeAPI` é o único tipo de
erro usado em todo o exemplo, garantindo consistência estrutural (T3); `status_do_trabalho`
produz um recurso consultável com `url_consulta` para qualquer estado de trabalho (T4);
`declarar_endpoint_sincrono` rejeita endpoint sem `limite_ms` declarado (T6).

`ErroDeAPI` e `RecursoDeStatusDeTrabalho` são ambos `frozen=True` — nenhum dos dois deveria ser
alterado depois de construído, porque cada um representa um fato específico (este erro aconteceu,
este trabalho está neste estado) que não faz sentido mutar depois de formado; qualquer mudança de
fato deveria produzir uma nova instância, não uma modificação da anterior.

`declarar_endpoint_sincrono` usa `limite_ms: int | None` como assinatura explícita, tornando a
ausência de orçamento um valor representável no próprio tipo (`None`), em vez de omitir o
parâmetro inteiro — isso permite que a validação aconteça de forma centralizada dentro da função,
sem depender de verificação externa antes da chamada.

Essa escolha espelha `resolver_exibicao` do `22-FRONTEND-ARCHITECT` e `artefato_atual` do
`19-DEVOPS`: ausência de valor esperado é sempre um estado explícito na assinatura da função,
nunca uma condição inferida por convenção externa ao tipo.