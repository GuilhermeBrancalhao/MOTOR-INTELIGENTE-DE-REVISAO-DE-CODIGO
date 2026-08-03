---
volume: "17"
volume_nome: SECURITY
tipo: GOVERNANCA
secao: 03-Escopo
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Escopo

## Dentro deste volume

As três categorias de risco específicas de sistemas com componentes de IA: prompt injection,
exfiltração de dados via ferramenta/saída do modelo, e sandboxing de execução de código/comando
gerado por IA. A política e os controles que mitigam cada categoria — o que precisa ser verdade
sobre o sistema para que o risco seja aceitável.

## Fora deste volume, e para onde vai

**O processo que faz esses controles rodarem no pipeline, a cada mudança de código** é
`18-DEVSECOPS` — este volume define a política (o que precisa ser verdade); `18` define o
processo (como isso é verificado continuamente, em que ponto do CI/CD).

**Segurança de infraestrutura tradicional** (rede, autenticação de usuário final, criptografia em
repouso/trânsito) tem literatura de segurança de software genérica que não é reescrita aqui — este
volume foca no que é específico de sistemas com IA, não em segurança de aplicação em geral.

**Observabilidade e telemetria de produção**, incluindo alertas de segurança acionados em tempo
real, é `21-OBSERVABILITY` — este volume define o que precisa ser detectável; `21` define como a
detecção é instrumentada e monitorada continuamente.

**A governança do próprio processo de documentação deste acervo** (quem audita o quê, matriz de
controles sobre o texto) é `01-FUNDACAO` — não confundir as duas matrizes de controle: uma audita
comportamento de sistema de IA em produção, a outra audita qualidade de conteúdo escrito.

## Fronteira deliberada

Este volume não cobre gestão de vulnerabilidade de dependência de terceiro (bibliotecas com CVE
conhecido) nem resposta a incidente pós-violação — o foco é prevenção estrutural específica da
classe de risco introduzida por um modelo de linguagem processando texto de origem não
totalmente confiável.
