---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 13-Testes
status: PRONTO
atualizado_em: 2026-07-30
---

# Testes

A suíte de `exemplos/31-testing/tests/` tem **23 funções de teste**, das quais **7 são
parametrizadas**, somando **48 casos executados** por `python -m pytest
exemplos/31-testing -q`. A distinção entre função e caso importa para este volume
especificamente: `09-Boas-Praticas.md` recomenda parametrização sobre cópia e cola, e a
métrica que prova que a recomendação foi seguida aqui é justamente esta -- 7 das 23
funções cobrem, juntas, 32 dos 48 casos; as 16 funções restantes cobrem um caso cada.

| Arquivo | Funções | Casos | Parametrizadas |
|---|---|---|---|
| `test_validador_cpf.py` | 9 | 32 | 6 (`cpf_sintetico_valido_passa`, `ultimo_digito_errado_invalida`, `penultimo_digito_errado_invalida`, `comprimento_errado_invalida`, `todos_os_digitos_iguais_sao_rejeitados_apesar_do_digito_bater`, `valido_com_caracteres_nao_numericos_nunca_levanta`) |
| `test_limitador_de_taxa.py` | 8 | 10 | 1 (`custo_nao_positivo_levanta`) |
| `test_notificacao.py` | 6 | 6 | 0 |

## Classificação por camada

Os três arquivos são, sem exceção, testes **unitários**: nenhum toca rede, disco ou
processo externo, e todos rodam na suíte inteira em menos de duas décimas de segundo.
Dentro da camada unitária, duas técnicas diferentes aparecem:

- **Teste de fronteira e classe de equivalência**, em `test_validador_cpf.py`. As
  classes de equivalência são "comprimento correto" contra "comprimento incorreto",
  "dígitos distintos" contra "onze dígitos iguais", e "dígito verificador correto"
  contra "alterado" -- cada classe tem pelo menos um caso representando-a, e a classe
  de repdígito tem os dez casos possíveis, não um só.
- **Teste de interação e de propagação de erro sobre um duplo**, em
  `test_notificacao.py`. Quatro dos seis testes daquele arquivo assertam sobre o que o
  colaborador substituído recebeu (`fake.enviados`), não só sobre o valor devolvido; um
  quinto (`test_notificador_que_falha_propaga_o_erro`) assere sobre o que o duplo
  repassa quando falha (`pytest.raises(RuntimeError, match=...)`). Os dois primeiros
  testes de `test_limitador_de_taxa.py` (`test_comeca_com_o_balde_cheio`,
  `test_permite_ate_a_capacidade_e_depois_bloqueia`) **não** são desta categoria --
  ambos assertam só sobre o valor devolvido por `fichas_disponiveis`/`permitir`, sem
  inspecionar nenhum colaborador.

## Os quatro testes que mais sustentam este volume

`test_todos_os_digitos_iguais_sao_rejeitados_apesar_do_digito_bater` é o que justifica
o módulo 1 existir -- sem ele, remover a checagem de repdígito não quebraria teste
nenhum. `test_recusa_nao_consome_fichas_parcialmente` e
`test_reabastecimento_nao_passa_da_capacidade` são os dois que travam os limites do
balde de fichas nas duas direções (não desconta ao recusar, não excede ao reabastecer).
`test_notificador_que_falha_propaga_o_erro` é o único teste da suíte que verifica
comportamento de erro de um colaborador externo, e é ele que prova que
`ServicoDeBoasVindas` não tem `try`/`except` escondendo a falha.

## O que esta suíte deliberadamente não cobre

Não há teste de performance sob volume (quantas chamadas por segundo o limitador
sustenta) -- isso é escopo de `33-PERFORMANCE`, conforme `03-Escopo.md`. Não há teste
de concorrência (duas threads chamando `permitir` ao mesmo tempo): os três módulos não
declaram ser thread-safe, e testar concorrência sobre um componente que não promete
segurança de thread produziria uma garantia que o código não sustenta.
