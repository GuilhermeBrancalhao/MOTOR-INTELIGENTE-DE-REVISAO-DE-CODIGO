---
volume: "30"
volume_nome: AI-GOVERNANCE
tipo: GOVERNANCA
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/30-ai-governance/governanca_ia.py -->

`governanca_ia.py`, citado acima, formaliza G1-G6: `RegistroDeCasosDeUso.registrar_caso` recusa
`CasoDeUso` sem `dono_responsavel` (G1); `verificar_pronto_para_producao` recusa caso não
classificado (G2); `registrar_decisao` recusa decisão de risco ALTO ou CRITICO sem
`revisada_por_humano=True` (G3); toda decisão aceita entra em histórico nunca editado (G4);
`verificar_pronto_para_producao` também recusa caso sem `aprovado_para_producao=True` (G5);
`RevisaoPeriodica` acumula histórico de revisão, nunca substituindo a anterior (G6).

`aprovar_para_producao` usa `dataclasses.replace` em vez de um campo mutável em `CasoDeUso` —
essa escolha mantém `CasoDeUso` congelado (`frozen=True`), o que impede qualquer código externo de
alterar `dono_responsavel` ou `nivel_de_risco` de um caso já registrado sem passar pelas operações
nomeadas do `RegistroDeCasosDeUso`, preservando a mesma garantia estrutural já vista em outros
volumes deste acervo para dado que representa um fato histórico.

Essa mesma disciplina aparece em `Repositorio` do 24-DATABASE-ARCHITECT e em `RegistroDeDeploy`
do 19-DEVOPS, reforçando que fato histórico imutável é um padrão recorrente neste acervo, não
uma escolha isolada deste volume específico, mas uma convenção que atravessa vários domínios
diferentes tratados por volumes distintos. A recorrência dessa escolha em contextos tão
diferentes — deploy, persistência de dado, e agora governança de decisão — sugere fortemente que ela resolve
um problema bem genérico o suficiente para valer a pena reconhecer como padrão do próprio acervo.