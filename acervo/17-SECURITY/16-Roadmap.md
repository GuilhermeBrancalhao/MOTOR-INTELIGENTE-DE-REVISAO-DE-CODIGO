---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 16-Roadmap
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Roadmap

## O que este volume ainda não cobre

Citação formal de código executável com teste correspondente no formato deste acervo
(`<!-- exemplo: -->`) — a implementação real existe no motor `ENGINE` e é referenciada em prosa
em `11-Implementacao.md` e `12-Exemplos.md`, mas citar formalmente exigiria extrair o
classificador de risco como módulo genérico (sem acoplamento ao restante do motor) e escrever
teste no formato `exemplos/17-security/tests/`, trabalho registrado como pendente, não feito
neste ciclo (2026-08-03).

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
