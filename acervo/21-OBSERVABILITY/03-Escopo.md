---
volume: "21"
volume_nome: OBSERVABILITY
tipo: GOVERNANCA
secao: 03-Escopo
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Escopo

## Dentro deste volume

A disciplina geral de instrumentação para sistema com IA: quais categorias de sinal são
específicas dessa classe de sistema (motivo de encerramento não-ideal, taxa de intervenção
humana, decomposição de custo/latência por tipo de etapa), como decidir granularidade de
instrumentação proporcional ao custo do passo, e o critério que decide quando um sinal cruza de
"observar" para "alertar".

## Fora deste volume, e para onde vai

**A lista específica de métricas de cada motor individual** (as tabelas em `08-Metricas.md`,
`09-Metricas.md`, `10-Metricas.md` etc.) é definida em cada volume próprio — este volume não
repete essas listas, define os princípios que orientam como qualquer uma delas deveria ser
coletada e monitorada.

**A taxonomia de risco que decide o que é um vetor de segurança a detectar** é `17-SECURITY` —
este volume assume que essa taxonomia já existe e trata de como o sinal correspondente é
instrumentado e monitorado continuamente, não de qual sinal é relevante do ponto de vista de
segurança.

**Infraestrutura de coleta e armazenamento de log/métrica/trace** (ferramenta específica, formato
de exportação, retenção) é preocupação de `19-DEVOPS`/`20-CLOUD` quando aplicável — este volume
define o contrato do que precisa ser instrumentado, não onde os dados residem fisicamente.

**O processo de resposta a incidente depois que um alerta dispara** não é assunto deste volume —
este volume termina no ponto em que um sinal é classificado como "exige atenção"; o que acontece
depois é operação, fora do escopo de um volume de conhecimento.

## Fronteira deliberada

Este volume não decide o que é "sucesso" ou "risco" para um domínio específico — essas decisões
pertencem a cada volume individual (o que é objetivo atingido para `08`, o que é vetor de risco
para `17`). Este volume decide como qualquer decisão desse tipo, já tomada em outro volume, se
torna sinal observável e monitorável de forma consistente.
