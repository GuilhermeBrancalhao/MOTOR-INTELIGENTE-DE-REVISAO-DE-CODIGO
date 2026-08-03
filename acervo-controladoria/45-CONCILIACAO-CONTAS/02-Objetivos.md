---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 02-Objetivos
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Objetivos

Depois de ler este volume e usar o código citado, o leitor consegue:

**Achar o ponto em que dois saldos fecham.** Dado um saldo inicial conhecido, uma lista de
movimentos e uma série de saldos de banco por dia, calcular o dia mais recente em que o saldo
projetado do sistema bate com o saldo do banco no centavo — e explicar por que caminhar para
frente a partir de um saldo passado é mais robusto que caminhar para trás a partir do saldo de
hoje, ver `04-Arquitetura.md` e `07-Regras.md`.

**Casar um movimento bancário contra um título em aberto** sem criar lançamento avulso quando já
existe previsão, respeitando tolerância de valor para consumo variável e descontando vocabulário
genérico (boilerplate bancário) antes de medir similaridade de nome — ver `11-Implementacao.md`.

**Classificar a confiança de um casamento em três níveis** (alta, média, baixa), sabendo qual
combinação de evidência move um movimento para escrita automática e qual sempre precisa de
revisão humana, e demonstrar que a ausência de uma fonte de evidência só pode reduzir a
confiança, nunca aumentá-la — ver `exemplos/45-conciliacao-contas/confianca.py` e o teste
`test_ausencia_de_fonte_de_evidencia_so_pode_rebaixar_nunca_subir`.

**Impedir escrita duplicada por chave composta**, não por valor isolado, e explicar por que dois
movimentos legítimos de mesmo valor absoluto não podem colidir na guarda.

**Registrar uma trilha local e apontar por que ela é a fonte de verdade sobre idempotência**, e
não um índice de sistema externo que pode mudar de estado depois da escrita.

Cada um desses cinco objetivos corresponde a um módulo com testes próprios em
`exemplos/45-conciliacao-contas/tests/`, mais um teste de integração
(`test_fluxo_completo.py`) que percorre os cinco em sequência, na ordem em que a operação real
acontece.
