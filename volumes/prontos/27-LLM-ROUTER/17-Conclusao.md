---
volume: "27"
volume_nome: LLM-ROUTER
tipo: ENGINE
secao: 17-Conclusao
status: PRONTO
atualizado_em: 2026-08-04
---

# Conclusão

Rotear entre modelos parece, à primeira vista, uma decisão simples de "se o principal falhar, usa
o outro". A parte não óbvia — e onde a maioria das implementações ingênuas falha — é a diferença
entre reagir a ruído e reagir a sinal real, e a assimetria deliberada entre cair rápido para o
fallback e subir devagar de volta ao principal. As seis regras deste volume existem para essa
diferença, não para a lógica trivial do caso feliz.

A regra mais fácil de subestimar é L5 — janela de estabilidade na recuperação. Sem ela, um
sistema sob degradação intermitente pode alternar entre principal e fallback repetidamente,
produzindo uma experiência pior do que ficar simplesmente no fallback até a situação se
estabilizar de verdade.

Um roteador que reage bem à degradação mas mal à recuperação ainda causa dano — apenas um dano
diferente, mais sutil e mais difícil de diagnosticar, porque parece que o sistema está
"funcionando", só que instável. As seis regras deste volume tratam as duas metades do problema
com o mesmo rigor.