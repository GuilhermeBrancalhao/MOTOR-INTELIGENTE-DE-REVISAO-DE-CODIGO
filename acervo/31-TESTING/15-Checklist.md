---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 15-Checklist
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Checklist

Antes de considerar uma suíte de teste madura para um componente ou volume. Nenhum item vem
marcado: quem verifica marca cada um com evidência à mão — o nome do teste, a mutação que o
derrubou — e item que não pode ser marcado é o que falta, não detalhe a contornar.

- [ ] Toda invariante declarada em `07-Regras.md` do domínio tem pelo menos um teste
      identificável pelo nome.
- [ ] Nomes de teste de regressão de regra descrevem a violação prevenida, não só a função
      testada.
- [ ] Pelo menos um teste crítico por invariante foi provado por mutação, com a prova registrada.
- [ ] Existe teste de fluxo completo para todo sistema com mais de um componente interagente em
      ordem específica.
- [ ] Nenhum teste foi ajustado para "passar" numa mudança de código sem antes investigar se a
      mudança violou a regra original protegida.
- [ ] A suíte distingue explicitamente (por convenção de nome ou organização) teste de caminho
      feliz de teste de regressão de regra.
- [ ] Ferramenta de mutação automatizada integrada ao pipeline — hoje o processo descrito é
      manual (mutar de propósito, observar, revisar); automação é extensão registrada em
      `16-Roadmap.md`, não parte do contrato mínimo deste volume.

O último item é lacuna conhecida e registrada, não esquecida.
