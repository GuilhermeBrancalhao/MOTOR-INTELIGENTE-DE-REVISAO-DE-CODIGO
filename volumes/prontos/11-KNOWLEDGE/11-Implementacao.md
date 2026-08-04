---
volume: "11"
volume_nome: KNOWLEDGE
tipo: ENGINE
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-08-04
---

# Implementação

<!-- exemplo: exemplos/11-knowledge/curadoria.py -->

`curadoria.py`, citado acima, formaliza K1-K6: `Documento` recusa origem sem os três campos
obrigatórios (K1); `consultar_valido` nunca devolve documento em estado `Expirado` (K2);
`detectar_conflitos` agrupa por `fato_chave` e nunca resolve sozinho, só sinaliza (K3);
`revalidar` é a única transição de `Expirando` de volta a `Valido`, sempre explícita (K6).

## Como o motor real aplicaria isto

A implementação mínima separa claramente três responsabilidades que é tentador misturar num
único pipeline: validação de entrada (K1, K4), detecção de conflito (K3) e gestão de ciclo de
vida (K2, K6). Misturar as três num único passo de ingestão dificulta testar cada uma
isoladamente e tende a produzir o atalho descrito em `10-Anti-Patterns.md` — pular a checagem de
conflito "porque o pipeline já está fazendo muita coisa".

## Onde a integração com outros volumes acontece

`14-VECTOR` recebe só documento que passou pela validação deste volume — nunca consulta a fonte
bruta diretamente. `13-RAG` consulta o estado de ciclo de vida deste volume antes de incluir um
documento numa resposta, mesmo que o documento já esteja fisicamente indexado.

A ordem de implementação recomendada é: `Origem` e `Documento` primeiro, testados contra os
cenários de rejeição (K1). Ciclo de vida (`EstadoCiclo`, transições) depois, testado
isoladamente do resto. Detecção de conflito por último, porque depende dos dois anteriores já
estarem corretos — um conflito detectado sobre um documento com origem inválida não deveria
sequer chegar a essa etapa.
