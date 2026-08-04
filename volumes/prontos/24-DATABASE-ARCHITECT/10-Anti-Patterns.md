---
volume: "24"
volume_nome: DATABASE-ARCHITECT
tipo: ARQUITETURA
secao: 10-Anti-Patterns
status: PRONTO
atualizado_em: 2026-08-04
---

# Anti-Patterns

**Migração de schema aplicada no mesmo deploy do código que já assume o formato novo.** Remove a
janela de compatibilidade que A1 exige, criando uma corrida entre a migração terminar e o código
novo começar a ler — se a ordem inverter mesmo que por um instante, algo lê no formato errado.

**Conteúdo gerado por IA gravado sem nenhuma referência a qual modelo o produziu.** Torna
impossível, mais tarde, diagnosticar por que dois resultados aparentemente da mesma operação
divergem — a explicação mais provável (mudança de modelo) fica invisível.

**Última escrita sempre vence, sem verificação de versão esperada.** É exatamente o comportamento
que A3 existe para evitar — uma mudança concorrente legítima desaparece sem que ninguém saiba.

**Coleção de log ou histórico crescendo indefinidamente "porque um dia pode ser útil".** Sem
política de retenção declarada, esse "um dia" nunca chega, e o custo de armazenamento cresce sem
limite por um valor que ninguém decidiu ativamente preservar.

**Exclusão em cascata automática sem revisão, disparada só para "resolver" uma referência
quebrada.** Excluir automaticamente tudo que referencia um registro removido pode apagar dado que
deveria ter sido preservado — a rejeição explícita (A6) é mais segura que cascata automática sem
revisão humana.


**Testar migração apenas contra banco vazio, nunca contra dado real no formato antigo.** Um teste
que só valida o schema novo isoladamente não prova compatibilidade — prova apenas que o schema
novo é internamente consistente, o que é uma verificação bem mais fraca do que A1 exige.