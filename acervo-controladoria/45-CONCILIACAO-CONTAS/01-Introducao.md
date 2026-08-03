---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 01-Introducao
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Introdução

Este volume descreve um motor de reconciliação entre o extrato de uma conta bancária e o
lançamento correspondente num sistema contábil. O problema que ele resolve não é "importar
extrato" nem "gerar relatório de saldo" — é decidir, movimento a movimento, se o que apareceu no
banco já tem contrapartida no sistema, se pode ser escrito sozinho ou se precisa de revisão
humana, e como garantir que a mesma escrita nunca aconteça duas vezes. Existem cinco decisões que
se repetem em qualquer motor de conciliação bancária, independentemente do banco ou do ERP por
trás: onde ancorar o saldo, como casar um movimento com um título em aberto, quando confiar o
suficiente para escrever sozinho, como impedir duplicata sem impedir movimento legítimo, e onde
fica a fonte da verdade sobre o que já foi processado. Este volume trata dessas cinco decisões
como módulos separados e testáveis, não como um único script monolítico.

A razão para este volume existir separado de `43-CONTABILIDADE-BASICA` é que conciliação e
lançamento contábil resolvem problemas diferentes: o 43 decide **como registrar** um fato
financeiro (débito, crédito, categoria, centro de custo); este volume decide **se um fato já
foi registrado** e, se não, **com que confiança escrevê-lo**. Um sistema pode ter contabilidade
impecável e conciliação inexistente — e nesse caso ninguém sabe se o saldo contábil reflete a
realidade do banco. A separação também importa porque conciliação tem uma característica que
lançamento contábil não tem: ela lida com dado que chega fora de ordem, atrasado, ou de fontes
que mudam de estado depois da leitura (um índice remoto que apaga um campo após a escrita, por
exemplo) — o que exige desenho específico, coberto em `07-Regras.md` e `10-Anti-Patterns.md`.

O código citado por este volume vive em
[`../exemplos/45-conciliacao-contas/`](../exemplos/45-conciliacao-contas/) e é genérico por
construção: não referencia nenhum banco, ERP, cliente ou credencial específicos. O padrão que ele
implementa foi extraído de operação real de conciliação bancária, generalizado para qualquer par
banco/sistema contábil.
