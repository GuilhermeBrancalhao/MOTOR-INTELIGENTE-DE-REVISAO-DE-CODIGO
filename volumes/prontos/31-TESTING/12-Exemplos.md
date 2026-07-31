---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 12-Exemplos
status: PRONTO
atualizado_em: 2026-07-30
---

# Exemplos

Os três casos abaixo foram reproduzidos por execução direta contra os módulos reais,
não copiados de memória -- cada número citado é o que a chamada de fato devolve.

<!-- exemplo: exemplos/31-testing/validador_cpf.py -->
<!-- exemplo: exemplos/31-testing/limitador_de_taxa.py -->
<!-- exemplo: exemplos/31-testing/notificacao.py -->

## Caso 1: validação em lote, quatro sintéticos e três armadilhas

Chamando `valido` sobre sete entradas -- os quatro CPFs sintéticos de
`test_validador_cpf.py` e três variações inválidas construídas a partir do primeiro:

| Entrada | `valido(...)` | Por quê |
|---|---|---|
| `"123.456.789-09"` | `True` | dígitos verificadores conferem; a máscara é removida antes de calcular |
| `"98765432100"` | `True` | base descendente, dígitos verificadores `0` e `0` |
| `"11223344517"` | `True` | dígitos verificadores `1` e `7` |
| `"33333333414"` | `True` | base quase-repdígito com um dígito final diferente da base |
| `"12345678900"` | `False` | mesma base do primeiro caso, segundo dígito verificador alterado de `9` para `0` |
| `"1234567890"` | `False` | dez caracteres, não onze |
| `"11111111111"` | `False` | onze dígitos iguais -- a fórmula devolveria `1` e `1`, e a checagem explícita rejeita antes de chegar lá |

## Caso 2: um limitador de dez fichas observado por dois segundos simulados

`LimitadorDeTaxa(capacidade=10, taxa_por_segundo=5, agora=relogio)`, com `relogio`
começando em `0.0` e avançando só quando `avancar` é chamado:

```
inicio:                 fichas_disponiveis() == 10
permitir(10) -> True    fichas_disponiveis() == 0
avancar(1)              fichas_disponiveis() == 5.0   (0 + 1s * 5/s)
permitir(3)  -> True    fichas_disponiveis() == 2.0
avancar(1)              fichas_disponiveis() == 7.0   (2 + 1s * 5/s)
permitir(5)  -> True    fichas_disponiveis() == 2.0
permitir(5)  -> False   fichas_disponiveis() == 2.0   (recusa nao consome)
```

Nenhum passo desta sequência esperou um segundo real -- os dois segundos simulados
custaram o tempo de duas chamadas a `avancar`, não dois segundos de relógio de parede.
É essa propriedade que torna a suíte inteira de `test_limitador_de_taxa.py` executável
em milissegundos, confirmado em `13-Testes.md`.

## Caso 3: dois registros no mesmo fake, e um provedor fora do ar

Com um único `NotificadorFalso`, duas chamadas a `registrar`:

```
servico.registrar("Ana", "ana@exemplo.test")
  -> devolve "Bem-vindo(a), Ana!"
servico.registrar("Bea", "bea@exemplo.test")
  -> devolve "Bem-vindo(a), Bea!"

fake.enviados == [
    ("ana@exemplo.test", "Bem-vindo(a), Ana!"),
    ("bea@exemplo.test", "Bem-vindo(a), Bea!"),
]
```

Trocando o fake por `NotificadorQueFalha`, a mesma chamada
(`servico.registrar("Pedro", "pedro@exemplo.test")`) levanta `RuntimeError` com a
mensagem `"provedor de envio indisponivel"` -- o serviço não a captura, e quem chamou
`registrar` recebe a falha original, não uma versão resumida ou traduzida dela.
