---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 11-Implementacao
status: PRONTO
atualizado_em: 2026-07-30
---

# Implementação

Os três módulos existem como código executável com teste, e é esse código que esta
seção descreve. As citações abaixo são verificadas pelo gate estrutural: o validador
confere que o arquivo citado existe e que existe o teste correspondente em
`tests/test_<arquivo>.py`. Documentação que cita código inexistente reprova.

<!-- exemplo: exemplos/31-testing/validador_cpf.py -->
<!-- exemplo: exemplos/31-testing/limitador_de_taxa.py -->
<!-- exemplo: exemplos/31-testing/notificacao.py -->

## Módulo 1: função pura, teste de fronteira

`validador_cpf.py` não tem estado nem colaborador -- três funções (`somente_digitos`,
`_digito_verificador`, `valido`) e duas constantes de pesos por posição
(`_PESOS_PRIMEIRO_DIGITO`, `_PESOS_SEGUNDO_DIGITO`), mais `_TAMANHO_CPF`. A decisão de
implementação que a seção `07-Regras.md` trava é a
ordem das duas checagens em `valido`: comprimento primeiro, dígitos repetidos depois,
cálculo dos verificadores por último. Checar o comprimento primeiro existe por
segurança de índice -- as linhas seguintes indexam a tupla de dígitos posicionalmente, e
uma entrada mais curta que onze caracteres quebraria ali se a ordem fosse outra.
Checar dígitos repetidos antes de calcular os verificadores é economia, não correção:
o cálculo aconteceria de qualquer forma se a ordem fosse inversa, porque o resultado
não depende de ter ou não calculado o dígito ainda.

## Módulo 2: dependência de tempo, injeção de relógio

`limitador_de_taxa.py` é um `dataclass` com `slots=True` mas **sem** `frozen=True` --
diferente de um registro de domínio como o `Veredicto` de `12-memory`, um limitador de
taxa tem estado que muda a cada chamada (`_fichas`, `_ultima_verificacao`), e
`frozen=True` proibiria exatamente a mutação que o componente existe para fazer. Os
dois campos de estado usam `field(init=False, repr=False)`: `init=False` porque são
calculados em `__post_init__`, nunca recebidos de fora; `repr=False` porque expor o
saldo interno na representação textual convidaria código de chamador a inspecionar
estado em vez de chamar `fichas_disponiveis()`, que é o único caminho público para essa
informação.

`agora: Callable[[], float]` não tem valor padrão -- a ausência de padrão é a
implementação da prática 1 de `09-Boas-Praticas.md`. `_reabastecer` é privado e chamado
no início de `permitir` e de `fichas_disponiveis`, nunca pelo chamador diretamente: as
duas operações públicas precisam do saldo atualizado, e centralizar a atualização em um
único método evita que uma das duas seja alterada no futuro e esqueça de reabastecer
antes de ler o saldo.

## Módulo 3: colaborador substituível por `Protocol`

`notificacao.py` declara `Notificador` como `typing.Protocol`, não como classe
abstrata. A diferença importa para o teste: `Protocol` é tipagem estrutural -- qualquer
objeto com um método `enviar(destinatario, mensagem)` compatível satisfaz o tipo, sem
precisar herdar de nada. `NotificadorFalso` e `NotificadorQueFalha` não estendem
`Notificador`; eles só têm o método com a assinatura certa, e isso é suficiente para
`ServicoDeBoasVindas` aceitá-los. Uma classe abstrata (`abc.ABC`) exigiria herança
explícita dos dois duplos, acoplando o código de teste à hierarquia de tipos do código
de produção sem necessidade.

A checagem de destinatário vazio em `registrar` ocorre **antes** da chamada a
`self.notificador.enviar` -- é essa ordem que `test_destinatario_vazio_levanta_e_nao_envia`
verifica ao afirmar `fake.enviados == []` depois da exceção, não só que a exceção foi
levantada.

## O `conftest.py` do diretório de exemplos

Os três módulos usam apenas a biblioteca padrão -- `validador_cpf.py` não importa nada
além de `__future__`; `limitador_de_taxa.py` importa `dataclasses` e `typing`;
`notificacao.py` importa `dataclasses` e `typing`. Não há dependência externa, não há
estado em disco e não há configuração. O
[`conftest.py`](../exemplos/31-testing/conftest.py) de `exemplos/31-testing/` existe por
um motivo de coleta de teste, não de comportamento do componente: sem `__init__.py` em
`tests/`, cada arquivo de teste do acervo inteiro precisa de um nome de módulo único
(`test_validador_cpf`, e não `tests.test_validador_cpf`), e a pasta que contém os três
módulos de produção deixa de entrar automaticamente no caminho de import -- o
`conftest.py` insere essa pasta em `sys.path` explicitamente, mesma solução já adotada
em `exemplos/12-memory/`.
