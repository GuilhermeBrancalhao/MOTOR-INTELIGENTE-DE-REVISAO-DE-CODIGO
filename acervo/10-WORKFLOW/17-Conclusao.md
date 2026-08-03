---
volume: "10"
volume_nome: WORKFLOW
tipo: ENGINE
secao: 17-Conclusao
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Conclusão

Este volume define o motor de workflow como sequência declarada de passos determinísticos e de
IA, com checkpoint confirmado a cada passo — não como uma cadeia de chamadas de função que perde
progresso a cada falha de infraestrutura. O contrato central — validação obrigatória de saída de
IA, checkpoint atômico antes de avançar, retomada sem reexecução de trabalho já confirmado —
existe para que um processo de negócio de longa duração seja tão confiável quanto um processo
determinístico curto, mesmo intercalando passos cuja saída não é garantida por construção.

O que o leitor deve levar embora: a diferença entre `AguardandoSinal` e `Pausado` não é
cosmética — uma é espera esperada pelo processo de negócio, a outra é sinal de atenção
necessária, e confundir as duas na observabilidade esconde onde intervenção humana é de fato
urgente. E a fronteira com `09-ORCHESTRATOR` (sequência declarada versus decisão de agente sem
sequência fixa a priori) é o que evita modelar decisão verdadeiramente aberta como uma árvore de
condições que tenta prever o imprevisível.

Este volume permanece `RASCUNHO` no front-matter: presumivelmente passa no gate estrutural, não
tem exemplo de código citado (gate 2 não se aplica ainda), e não passou pela auditoria do
critério 3.
