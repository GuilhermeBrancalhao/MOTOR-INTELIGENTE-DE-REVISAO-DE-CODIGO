---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 16-Roadmap
status: PRONTO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Paridade entre o exemplo e o classificador real do motor. `exemplos/17-security/classificador.py`
é a forma mínima da política — inversão de default, destinos autorizados, proteção do painel,
teto de tamanho — mas o classificador que roda em `ferramentas/risco.py` tem doze famílias
nomeadas e superfície muito maior. Os dois não divergem hoje no que ambos cobrem, e nada verifica
isso automaticamente: um teste de paridade, que rodasse os mesmos vetores contra os dois e
comparasse o nível devolvido, fecharia essa lacuna.

Catálogo de vetores de prompt injection e exfiltração observados em produção real fora do
contexto do motor `ENGINE` — o catálogo atual (`12-Exemplos.md`) é inteiramente sobre execução
insegura de comando (as famílias R1-R12), porque é o histórico real disponível; casos reais de
prompt injection e exfiltração ainda não foram documentados com o mesmo nível de detalhe
concreto.

## Ordem de cobertura pretendida

Primeiro, extrair o classificador de risco do motor `ENGINE` como módulo citável, com os testes
que já existem no motor adaptados ao formato de `exemplos/`. Depois, documentar casos reais de
prompt injection e exfiltração, se e quando observados, com o mesmo padrão de "vetor concreto +
correção + generalização em família" usado para as famílias R1-R12.

## O que este volume assume que pode mudar

O conjunto de três categorias de risco (prompt injection, exfiltração, execução insegura) reflete
o que é conhecido hoje como específico de sistemas com IA — uma quarta categoria pode emergir
conforme sistemas de IA assumem novos tipos de capacidade (por exemplo, manipulação de outro
agente de IA como vetor), e este volume precisaria ser estendido, não substituído, seguindo o
mesmo padrão de matriz de controles.
