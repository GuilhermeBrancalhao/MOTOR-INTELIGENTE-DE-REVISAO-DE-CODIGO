---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 06-Fluxogramas
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Fluxogramas

O fluxo de decisão de risco já está em `04-Arquitetura.md` (o `flowchart` que satisfaz a
exigência de diagrama do tipo `GOVERNANCA`). Esta seção detalha o caminho de decisão para cada
uma das três categorias separadamente, com foco no que dispara cada ramo.

## Prompt injection — o que dispara isolamento

Qualquer dado que o sistema processa sem ter sido escrito diretamente pelo operador na sessão
atual é candidato: conteúdo de arquivo lido, resultado de busca web, corpo de e-mail, saída de
uma ferramenta anterior que por sua vez consultou fonte externa. O gatilho não é "este texto
parece suspeito" (detecção de padrão é frágil e contornável) — é "este texto tem origem que não é
o operador", condição estrutural e verificável sem depender de heurística de conteúdo.

## Exfiltração — o que dispara auditoria de destino

Toda chamada de ferramenta que envia dado para fora do sistema (rede, arquivo compartilhado,
serviço externo) é candidata a auditoria de destino — a pergunta não é "o dado é sensível?"
(classificação de sensibilidade é outro problema, mais difícil e mais frágil), é "o destino desta
chamada específica é um dos destinos autorizados para este tipo de operação?". Uma chamada para
destino não listado é travada ou rastreada, nunca liberada por assumir que o conteúdo enviado é
inócuo.

## Execução insegura — o que dispara sandboxing

Toda execução de código ou comando cuja origem é geração do modelo (não código escrito e
revisado por humano antes da execução) é candidata a isolamento proporcional ao dano potencial —
comando de shell, por padrão, nunca é liberado sem verificação (a regra central do motor
`ENGINE`, documentada em `README.md`), porque cada comando de shell é uma linguagem própria com
aspas, substituição e variantes por plataforma, e enumerar o que é perigoso dentro dessa
linguagem não termina.
