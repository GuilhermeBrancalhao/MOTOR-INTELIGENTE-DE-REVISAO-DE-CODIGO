---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 08-Modelos
status: PRONTO
atualizado_em: 2026-08-04
---

# Modelos

`NivelDeRisco` é um enum ordenado (BAIXO, MEDIO, ALTO, CRITICO) — a ordem de declaração no código
corresponde à ordem de rigor exigido, e é essa ordenação que `registrar_decisao` consulta para
decidir se revisão humana é obrigatória.

`CasoDeUso` é imutável, e `RegistroDeCasosDeUso.aprovar_para_producao` produz uma nova instância
via `dataclasses.replace` em vez de mutar o campo `aprovado_para_producao` diretamente — cada
mudança de estado do caso de uso é uma substituição explícita, não uma mutação silenciosa de um
campo específico.

`DecisaoAutomatizada` carrega `modelo_usado` e `entrada` junto da `decisao` em si — a trilha de
auditoria (G4) não é útil se só registra o resultado; o contexto que produziu esse resultado é
igualmente parte do que precisa ser reconstruível depois.


`RegistroDeCasosDeUso` mantém três coleções distintas — `casos`, `trilha_de_auditoria` e
`historico_de_revisoes` — em vez de uma estrutura única que misturaria os três tipos de registro;
essa separação reflete que cada um tem ciclo de vida e frequência de escrita completamente
diferentes.

Misturar os três numa única lista exigiria filtrar por tipo toda vez que alguém precisasse
consultar apenas um deles, um custo evitável desde o desenho inicial do tipo — separar por
coleção específica também torna cada uma delas mais simples de exportar isoladamente, se
necessário apresentar apenas a trilha de auditoria a um auditor externo, por exemplo.