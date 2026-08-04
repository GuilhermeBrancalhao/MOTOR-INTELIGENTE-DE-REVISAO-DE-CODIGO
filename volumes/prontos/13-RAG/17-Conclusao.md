---
volume: "13"
volume_nome: RAG
tipo: ENGINE
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-08-04
---

# Conclusão

Este volume trata o pipeline de recuperação aumentada como o lugar onde três garantias
independentes (fonte curada, índice correto, geração fiel) precisam se juntar sem que nenhuma
seja assumida das outras. A tese central — fidelidade é medida depois da geração, nunca inferida
da presença de citação — existe porque citação presente e conteúdo fiel são propriedades
diferentes, e confundi-las é o modo de falha mais silencioso de sistemas de RAG.

O que o leitor deve levar embora: recusa explícita por falta de fonte é resultado de sucesso do
pipeline, não uma falha a evitar a qualquer custo — a alternativa, resposta plausível sem
fundamento, é sempre pior. E a fronteira com `11-KNOWLEDGE` e `14-VECTOR` é o que permite
diagnosticar exatamente onde um problema mora quando uma resposta sai errada: fonte, índice, ou
este pipeline.

Este volume permanece `RASCUNHO` no front-matter: presumivelmente passa no gate estrutural, tem
exemplo de código citado, e não passou pela auditoria do critério 3.
