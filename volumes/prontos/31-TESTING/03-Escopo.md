---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 03-Escopo
status: PRONTO
atualizado_em: 2026-08-03
---

# Escopo

## Dentro deste volume

A prática de escrever, organizar e manter teste que funciona como especificação executável: como
nomear um teste para que ele documente a regra que protege, como aplicar prova por mutação para
verificar que um teste não é decorativo, e como organizar uma suíte de forma que a
correspondência entre regra declarada (em `07-Regras.md` de qualquer volume) e teste que a prova
seja rastreável.

## Fora deste volume, e para onde vai

**O indicador agregado de qualidade** (cobertura percentual, taxa de teste quebradiço, tendência
de dívida técnica ao longo do tempo, gate de release baseado nesses números) é `32-QUALITY` — este
volume trata de como um teste individual é bem escrito; `32` trata de como a saúde da suíte
inteira é medida e usada para decisão de release.

**Performance e latência de execução da suíte de testes** é `33-PERFORMANCE` quando relevante —
este volume não trata de quão rápido os testes rodam, só de quão bem eles provam o que afirmam
provar.

**O processo que executa testes automaticamente a cada mudança de código** é `18-DEVSECOPS`
quando o foco é segurança, ou infraestrutura de CI/CD em geral fora do escopo deste acervo — este
volume define o que um teste deveria ser, não quando ele roda no pipeline.

**Teste de sistema com componente de IA especificamente** (validação de saída de modelo,
simulação de agente com modelo fake) é tratado dentro de cada volume que define o motor
correspondente (`08-AGENT-ENGINE/13-Testes.md`, `10-WORKFLOW/13-Testes.md`) — este volume define
os princípios gerais de teste como especificação que esses volumes aplicam ao seu domínio
específico, não repete o conteúdo específico de cada um.

## Fronteira deliberada

Este volume não define ferramenta ou framework de teste específico — os princípios (prova por
mutação, nomeação por regra, rastreabilidade regra-teste) são independentes de linguagem ou
ferramenta, e amarrar o volume a uma stack específica reduziria seu valor como referência geral.
