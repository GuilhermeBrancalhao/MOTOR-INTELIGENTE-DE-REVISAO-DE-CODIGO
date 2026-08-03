---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-08-03
---

# Regras

## Invariantes

**Todo teste que afirma proteger uma regra específica precisa ter sido provado por mutação pelo
menos uma vez.** Sem essa prova, a afirmação de que o teste protege a regra é não verificada —
exatamente a classe de problema que este acervo, como um todo, existe para evitar em qualquer
outra afirmação.

**O nome de um teste de regressão de regra identifica a violação que ele previne**, não apenas a
função ou módulo testado. Um nome genérico (`test_guarda_2`) não sobrevive a uma leitura rápida de
seis meses depois; um nome que descreve a violação
(`test_valores_redondos_repetidos_em_dias_diferentes_nao_sao_duplicata`) documenta a regra mesmo
sem abrir o código.

**Um teste que continua passando depois de uma mutação que deveria violar sua regra é reescrito,
nunca mantido como está.** Manter um teste decorativo na suíte, mesmo sem removê-lo, cria falsa
confiança de cobertura — é preferível não ter o teste do que tê-lo e acreditar que ele protege
algo que não protege.

**Teste de fluxo completo (composição de componentes na ordem real de uso) é obrigatório sempre
que houver mais de um componente com ordem de chamada específica entre si.** Testes unitários por
componente isolado não capturam quebra de composição — inverter a ordem de duas chamadas, por
exemplo, pode passar despercebido se nenhum teste exercita os componentes juntos.

**Regra sem teste correspondente é lacuna registrada, nunca lacuna silenciosa.** Se uma invariante
declarada em `07-Regras.md` de qualquer volume não tem teste ainda, isso aparece explicitamente
em `16-Roadmap.md` daquele volume — nunca é simplesmente omitido como se a regra não existisse.
