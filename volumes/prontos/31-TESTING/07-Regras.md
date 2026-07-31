---
volume: "31"
volume_nome: TESTING
tipo: PROCESSO
secao: 07-Regras
status: PRONTO
atualizado_em: 2026-07-30
---

# Regras

As nove regras abaixo são invariantes que o código de `exemplos/31-testing/` sustenta.
Sete das nove são travadas por pelo menos um teste nomeado; as duas primeiras são
verificadas de outra forma, cada uma pela sua própria evidência -- R1 pela ausência de
um padrão (nenhum arquivo importa `time` ou `datetime`), R2 pela assinatura de
`LimitadorDeTaxa` (`agora` sem valor padrão, o que faz o próprio Python levantar
`TypeError` se alguém instanciar sem informá-lo). Nenhuma das duas depende de teste
único que a exercite, e essa distinção está declarada aqui em vez de fingida como
"regra 3 nomeia teste, regra 1 também". Regra sem nenhuma forma de verificação, nomeada
ou estrutural, não é regra, é intenção -- o mesmo princípio que `CONTRIBUTING.md` exige
da própria máquina da plataforma se aplica ao conteúdo deste volume.

1. **Nenhum teste deste volume depende do relógio real.** `limitador_de_taxa.py` recebe
   `agora` como parâmetro; nenhum dos três arquivos de teste importa `time` ou
   `datetime`. É essa ausência que torna a suíte inteira determinística -- confirmada
   por busca textual, não por um teste que a assere.
2. **`agora` não tem valor padrão.** Se `time.monotonic` fosse o padrão, um teste
   poderia esquecer de injetar o relógio falso e ainda assim rodar -- de forma lenta e
   instável. Tornar o parâmetro obrigatório move o erro de "às vezes falha em CI" para
   "sempre falha ao escrever o código", que é onde um erro custa menos -- e é o próprio
   Python, via `TypeError` por argumento obrigatório ausente, quem impõe isso, não um
   teste deste volume.
3. **`permitir` nunca deixa `_fichas` negativa.** A subtração só ocorre depois da
   checagem `fichas >= custo`; uma recusa não desconta nada.
   `test_recusa_nao_consome_fichas_parcialmente` trava exatamente isso.
4. **Custo não positivo sempre levanta, antes de qualquer leitura do relógio.**
   `test_custo_nao_positivo_levanta` cobre três valores (`0`, `-1`, `-0.5`); a ordem das
   duas checagens dentro de `permitir` garante que o erro de parâmetro nunca dependa do
   estado do balde.
5. **`_reabastecer` nunca faz o saldo de fichas exceder a capacidade.** O `min(...)` na
   soma do reabastecimento é o que impede isso; `test_reabastecimento_nao_passa_da_capacidade`
   avança cem segundos simulados contra uma capacidade de cinco fichas e confirma o teto.
6. **`valido` nunca levanta exceção, para nenhuma entrada.** Comprimento errado,
   caractere não numérico e string vazia devolvem `False`; não há caminho de código que
   levante a partir de `valido`. `test_valido_com_caracteres_nao_numericos_nunca_levanta`
   é o teste que exercita especificamente entrada sem nenhum dígito numérico -- os
   demais casos deste arquivo partem de uma sequência de dígitos, certa ou errada.
7. **Uma sequência de onze dígitos iguais é sempre inválida, para qualquer um dos dez
   dígitos.** `test_todos_os_digitos_iguais_sao_rejeitados_apesar_do_digito_bater` é
   parametrizado sobre os dez valores (`"00000000000"` a `"99999999999"`) porque a regra
   vale para todos, não só para o caso mais citado (`"11111111111"`).
8. **`ServicoDeBoasVindas.registrar` nunca chama `notificador.enviar` quando o
   destinatário é vazio ou só espaço.** A checagem ocorre antes da chamada ao
   colaborador; `test_destinatario_vazio_levanta_e_nao_envia` confirma tanto a exceção
   quanto a lista `enviados` vazia depois dela.
9. **Erro levantado pelo notificador nunca é capturado em silêncio pelo serviço.**
   `registrar` não tem `try`/`except`; `test_notificador_que_falha_propaga_o_erro`
   confirma que a exceção do stub chega ao chamador com a mensagem original.
