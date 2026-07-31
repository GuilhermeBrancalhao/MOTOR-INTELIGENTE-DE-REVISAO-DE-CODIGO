---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 09-Boas-Praticas
status: PRONTO
atualizado_em: 2026-07-30
---

# Boas Práticas

Cada prática abaixo tem par direto em `10-Anti-Patterns.md` -- a prática descreve o
comportamento a seguir, o anti-padrão descreve o comportamento trocado e o custo
concreto de trocá-lo.

1. **Injete o relógio como parâmetro obrigatório, nunca como valor padrão.** Um
   parâmetro `agora` sem padrão transforma "esqueci de injetar o relógio falso" em erro
   de escrita, detectado na hora de programar; com `time.monotonic` como padrão, o
   mesmo esquecimento só aparece como instabilidade intermitente em CI, semanas depois.
2. **Escreva teste de fronteira explícito para toda regra que uma fórmula pode
   "confirmar" por acidente.** `validador_cpf` teria passado em qualquer teste que só
   verificasse números "normais"; só um teste dedicado ao caso de dígitos repetidos
   revela que a fórmula sozinha aceita entrada que o domínio rejeita.
3. **Escreva o dublê à mão quando a interface do colaborador é pequena.**
   `NotificadorFalso` e `NotificadorQueFalha` somam menos de dez linhas cada; configurar
   um framework de mock para um método só teria mais código de configuração do que a
   implementação real economizaria em execução.
4. **Verifique interação só quando a interação em si é o comportamento observável.** O
   valor de retorno de `registrar` já prova que a mensagem foi montada certo; a
   asserção sobre `fake.enviados` prova algo que o retorno não prova -- que o envio de
   fato ocorreu, com o destinatário certo.
5. **Nomeie o teste pela regra que ele trava, não pelo método chamado.**
   `test_todos_os_digitos_iguais_sao_rejeitados_apesar_do_digito_bater` diz o que quebra
   se alguém remover a checagem; `test_valido_caso_2` não diria nada a quem lê o nome
   sem abrir o corpo do teste.
6. **Use parametrização para classe de equivalência, não cópia e cola.**
   `test_ultimo_digito_errado_invalida` roda uma vez por CPF sintético porque o mesmo
   comportamento (dígito final trocado invalida) vale para todos -- quatro cópias do
   mesmo teste, cada uma com um número diferente, esconderiam que é a mesma regra sendo
   verificada quatro vezes.
7. **Teste o caminho de erro com a mesma disciplina do caminho feliz.**
   `test_custo_nao_positivo_levanta` cobre três valores inválidos, não um só -- o
   caminho de erro de um parâmetro numérico tem sua própria fronteira (`0` é um caso
   diferente de `-1`), e tratá-lo como "qualquer negativo serve de exemplo" deixaria
   `0` sem cobertura.
8. **Isole o motivo de falha por teste.** Cada teste deste volume verifica uma
   consequência: quando `test_reabastecimento_nao_passa_da_capacidade` falha, a causa
   possível é uma só (o teto do balde), nunca uma escolha entre três hipóteses
   diferentes espalhadas pelo mesmo corpo de teste.
