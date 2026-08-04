---
volume: "42"
volume_nome: PLUGINS
tipo: ENGINE
secao: 09-Boas-Praticas
status: RASCUNHO
atualizado_em: 2026-08-04
---

# Boas Práticas

Publicar o contrato de extensão com exemplo de hook mínimo funcionando, para que quem desenvolve
plugin novo tenha um ponto de partida real testável, em vez de precisar inferir a assinatura
esperada apenas lendo a documentação de referência.

Registrar toda ativação e desativação de plugin numa trilha auditável, incluindo qual versão de
contrato foi usada — o histórico completo facilita diagnosticar problema relatado por usuário que
tenha instalado combinação específica de plugins ativos.

Testar isolamento de falha deliberadamente, com um plugin de teste que lança exceção
propositalmente em cada hook conhecido, confirmando que o host de fato sobrevive e contém cada
um desses casos antes de considerar o mecanismo de isolamento confiável.

Revisar periodicamente quais capacidades cada plugin ativo de fato usa na prática, comparado ao
que foi declarado — uma capacidade declarada mas nunca usada pode indicar declaração excessiva
que vale a pena reduzir por princípio de menor privilégio.

Documentar explicitamente, para cada versão maior do contrato, quais hooks foram adicionados,
alterados ou removidos desde a versão maior anterior — um changelog de contrato de extensão
dedicado, separado do changelog geral do host, ajuda quem mantém plugin publicado a avaliar
rapidamente o esforço real de migração antes de atualizar.