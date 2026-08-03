---
volume: "45"
volume_nome: CONCILIACAO-CONTAS
tipo: ENGINE
secao: 11-Implementacao
status: RASCUNHO
atualizado_em: 2026-08-03
---

# Implementação

O motor são cinco arquivos de biblioteca padrão, sem dependência externa, com vinte e três
testes ao lado. A ordem de leitura é a ordem de dependência conceitual — âncora, casamento,
confiança, guarda, trilha — mesmo que nenhum módulo importe o anterior diretamente.

<!-- exemplo: exemplos/45-conciliacao-contas/ancora.py -->
<!-- exemplo: exemplos/45-conciliacao-contas/casamento.py -->
<!-- exemplo: exemplos/45-conciliacao-contas/confianca.py -->
<!-- exemplo: exemplos/45-conciliacao-contas/guarda.py -->
<!-- exemplo: exemplos/45-conciliacao-contas/trilha.py -->

## `ancora.py` — o saldo

Uma função pública, `achar_ancora`, e uma auxiliar, `saldo_projetado`. A decisão que mais paga é
caminhar para frente a partir de um saldo passado conhecido em vez de para trás a partir do
saldo de hoje — `07-Regras.md` explica o porquê, e `test_lancamento_com_data_retroativa_fecha_o_dia_correto_quando_chega`
prova o comportamento com um lançamento que só aparece dois dias depois da sua própria data.
`CENTAVO = 0.005` é a tolerância de fechamento — abaixo dela, resíduo de arredondamento de ponto
flutuante não é confundido com divergência real.

## `casamento.py` — o nome por trás do boilerplate

`_tokens()` remove pontuação, força maiúsculas e descarta palavras curtas (menos de quatro
caracteres) e o conjunto `BOILERPLATE` — vocabulário genérico que aparece em quase todo memo
bancário e por isso não identifica ninguém. `similaridade()` compara os tokens que sobram, não o
texto bruto: duas descrições de cartão do tipo "COMPRA NACIONAL DEBIT `<fornecedor>`" têm alta
similaridade textual bruta mesmo com fornecedores diferentes, porque o prefixo compartilhado
domina a métrica — descontar o boilerplate antes de comparar é o que evita esse falso positivo,
provado em `test_boilerplate_nao_derruba_a_identificacao_de_fornecedores_diferentes`. `casar()`
filtra candidatos por tolerância de valor primeiro, depois desempata por similaridade de nome, e
descarta o resultado se a melhor similaridade ainda ficar abaixo do limiar — ambíguo demais para
decidir sozinho é tratado como "sem casamento", não como "casamento arriscado".

## `confianca.py` — o gate de escrita

Duas condições alternativas levam a `ALTA`: match exato de valor com nome forte, ou histórico
forte (ocorrências e dominância acima dos limiares `LIMIAR_HISTORICO_OCORRENCIAS` e
`LIMIAR_HISTORICO_DOMINANCIA`). Qualquer combinação mais fraca cai em `MEDIA` (pendência
qualificada) ou `BAIXA` (pendência sem indício útil). A ordem das checagens no código importa:
histórico forte é avaliado mesmo quando o valor não bate exato, porque cobre o caso de despesa
recorrente com valor variável — o teste que fixa esse comportamento é
`test_historico_forte_promove_a_alta_mesmo_sem_valor_exato`.

## `guarda.py` e `trilha.py` — as duas camadas de proteção contra duplicata

São camadas independentes de propósito: a guarda decide antes de escrever ("essa chave já foi
vista?"), a trilha registra depois de escrever e recusa uma segunda escrita da mesma chave
levantando exceção em vez de ignorar. Ter as duas não é redundância — a guarda pode ser
reconstruída do zero a cada execução (memória volátil), enquanto a trilha é o registro
persistente que sobrevive entre execuções. Um motor real usa a guarda para decisão em memória
dentro de um lote, e a trilha como o registro que a próxima execução consulta para saber o que
já foi feito antes.
