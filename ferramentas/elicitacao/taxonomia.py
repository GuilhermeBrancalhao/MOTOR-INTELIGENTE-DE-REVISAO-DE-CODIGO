"""O terceiro eixo: **o que a pessoa quer fazer**, e as lacunas que só ele traz.

Plataforma e contexto respondem *onde roda* e *que risco o domínio carrega*. Nenhum
dos dois responde a pergunta anterior a essas duas: **que tipo de trabalho é este?**
Otimizar um sistema que já roda e materializar uma ideia que ainda não existe têm a
mesma plataforma, o mesmo contexto e quase nenhuma pergunta em comum — e o catálogo
de `catalogo.py`, escrito para o caso de criar do zero, faz as mesmas trinta e sete
perguntas para os dois.

**O buraco que este módulo fecha.** O repositório já provava, em três lugares
diferentes, que existiam classes de pedido sem lugar nenhum:

- `ferramentas/estado.py` tem a fase `EVOLUCAO` e `agents/cartografo.md` existe, mas
  nenhum dos cinco motores cobre evoluir sistema existente: `materializar-ideia` se
  exclui por escrito ("não use para alterar aplicação existente") e `revisar-codigo`
  é diagnóstico, não mudança.
- `catalogo.py` tem `Plataforma.AUTOMACAO` com quatro lacunas próprias e
  `Contexto.INTEGRACAO_EXTERNA` com duas — sinal de que automação e integração são
  trabalho, não apenas cenário.
- O acervo tem volume dedicado a testes, segurança, documentação, infraestrutura,
  dados e sistemas de IA (`31`, `17`, `35`, `19`–`21`, `24`, `07`–`08`), e nenhuma
  dessas classes tinha uma pergunta atrelada.

Quatorze intenções, então: as cinco que já tinham motor e as nove que só existiam
como fase, papel de agente ou volume solto.

**Por que módulo novo e não emenda no catálogo.** `catalogo.py` é cópia auditável de
`acervo/exemplos/03-discovery`, e a auditoria dessa cópia é um `diff`. Acrescentar
lacuna lá dentro apagaria essa propriedade para sempre. Aqui o eixo novo mora
separado, o cruzamento é uma função explícita (`lacunas_do_pedido`) e a origem
continua se auditando por comparação de texto.

**O gatilho da lacuna de intenção é a chave do mapa, não o campo.** Uma `Lacuna`
deste módulo tem `plataformas` e `contextos` vazios de propósito: ela é destravada
por estar sob uma intenção em `LACUNAS_POR_INTENCAO`. Por isso ela **não passa** em
`validar_catalogo` — que reprovaria, com razão, "não é universal e não tem gatilho"
— e tem a sua própria validação aqui. Os dois validadores olham para a mesma
`Lacuna` com regras diferentes porque os dois eixos são diferentes; unificá-los
exigiria dar ao catálogo um campo que só este módulo usa.

**Sem intenção não há palpite.** `classificar` levanta quando o texto não traz sinal
ou traz sinal empatado. Adotar uma classe padrão seria o `PADRAO_ASSUMIDO` de
`deteccao.py` circulando como decisão — com o agravante de que aqui a classe escolhe
*quais perguntas existem*, e a errada não produz uma pergunta ruim: produz uma
entrevista inteira sobre outro assunto.

Nota de forma: o texto deste módulo leva acento, ao contrário de `catalogo.py` e
`deteccao.py`. Aqueles dois são cópia de um exemplo escrito em ASCII e a cópia se
mantém literal; este é código local, e a convenção local — `__init__.py`, `CLAUDE.md`
— é português escrito por inteiro.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from enum import StrEnum

from .catalogo import (
    CATALOGO,
    PESO_MAXIMO_VALIDO,
    PESO_MINIMO_VALIDO,
    Contexto,
    Lacuna,
    Plataforma,
    lacunas_ativas,
)
from .deteccao import (
    CONFIANCA_ALTA,
    CONFIANCA_BAIXA,
    CONFIANCA_MEDIA,
    Origem,
    Palpite,
    _dobrar,
    _fronteira,
    _trecho_em,
)


class Intencao(StrEnum):
    """Que tipo de trabalho o pedido pede. Decide quais perguntas existem.

    As cinco primeiras têm motor escrito em `motores/`. As nove seguintes são as que
    a descoberta encontrou sem dono: cada uma tem evidência no repositório (fase,
    papel de agente, cartão de stack ou volume do acervo) e nenhuma tinha pergunta.

    Uma intenção por pedido, e é aqui que este eixo difere dos outros dois. Um
    software roda em WEB **e** MOBILE, e carrega saúde **e** pagamento ao mesmo
    tempo; um pedido, no momento em que chega, é uma coisa só. "Revisa e otimiza"
    não é uma intenção mista: são dois trabalhos em sequência, com medição no meio,
    e tratá-los como um só produz uma entrevista que não serve a nenhum dos dois.
    Por isso `classificar` levanta no empate em vez de somar.
    """

    # --- Com motor em `motores/`
    MATERIALIZAR = "MATERIALIZAR"
    ARQUITETAR = "ARQUITETAR"
    REVISAR = "REVISAR"
    OTIMIZAR = "OTIMIZAR"
    DIAGRAMAR = "DIAGRAMAR"
    # --- Sem motor: descobertas por evidência no próprio repositório
    EVOLUIR = "EVOLUIR"
    AUTOMATIZAR = "AUTOMATIZAR"
    INTEGRAR = "INTEGRAR"
    TRATAR_DADOS = "TRATAR_DADOS"
    TESTAR = "TESTAR"
    PROTEGER = "PROTEGER"
    DOCUMENTAR = "DOCUMENTAR"
    OPERAR = "OPERAR"
    CONSTRUIR_IA = "CONSTRUIR_IA"


#: Qual motor atende cada intenção — e `None` onde não existe motor nenhum.
#:
#: O `None` é o achado do ciclo posto em dado, e não em comentário: nove das
#: quatorze classes não têm para onde ser encaminhadas. Um despachante que leia este
#: mapa consegue dizer "não há motor para isto, e é isto que falta", que é diferente
#: de escolher o motor menos errado em silêncio.
MOTOR_POR_INTENCAO: Mapping[Intencao, str | None] = {
    Intencao.MATERIALIZAR: "materializar-ideia",
    Intencao.ARQUITETAR: "arquitetar-sistema",
    Intencao.REVISAR: "revisar-codigo",
    Intencao.OTIMIZAR: "otimizar-performance",
    Intencao.DIAGRAMAR: "diagramar",
    Intencao.EVOLUIR: None,
    Intencao.AUTOMATIZAR: None,
    Intencao.INTEGRAR: None,
    Intencao.TRATAR_DADOS: None,
    Intencao.TESTAR: None,
    Intencao.PROTEGER: None,
    Intencao.DOCUMENTAR: None,
    Intencao.OPERAR: None,
    Intencao.CONSTRUIR_IA: None,
}


class TaxonomiaInvalida(ValueError):
    """Intenção sem lacuna, sem termo, com id repetido ou com peso fora da faixa.

    Levanta pelo mesmo motivo que `CatalogoInvalido`: é erro de programa, e todos os
    quatro somem em silêncio. Intenção sem lacuna é classe que classifica e não
    pergunta nada — o eixo existe e não muda a entrevista. Intenção sem termo é
    classe que nunca será alcançada por `classificar`, o que é pior: ela consta da
    enumeração, aparece na documentação e nenhum pedido chega nela.

    Id repetido é o defeito mais caro dos quatro, porque atravessa os dois eixos: o
    cruzamento junta lacuna de catálogo com lacuna de intenção em um conjunto único
    indexado por id, e um id repetido faz uma das duas desaparecer sem aviso.
    """


class IntencaoDesconhecida(KeyError):
    """Valor que não corresponde a nenhuma intenção declarada.

    Herda de `KeyError` porque é exatamente isso — chave ausente — e é o mesmo
    contrato de `LacunaDesconhecida` em `entrevista.py`. Devolver conjunto vazio de
    lacunas para uma classe desconhecida seria a pior saída possível: a entrevista
    seguiria adiante sem nenhuma pergunta de intenção e a especificação sairia
    parecendo completa.
    """


class IntencaoIndeterminada(ValueError):
    """O texto não trouxe sinal de intenção, ou trouxe sinal empatado.

    Não é falha do classificador: é resultado dele. Sem evidência é pendência, não
    palpite — e a pendência aqui tem conserto barato, que é perguntar. Escolher a
    primeira da lista custaria uma entrevista inteira sobre o trabalho errado.

    `candidatas` carrega as classes que empataram, na ordem do placar, para que quem
    chamou consiga formular a pergunta de desempate em vez de apenas relatar o erro.
    Vazio significa ausência de sinal, e aí a pergunta é outra.
    """

    def __init__(self, mensagem: str, candidatas: Iterable[Intencao] = ()) -> None:
        super().__init__(mensagem)
        self.candidatas: tuple[Intencao, ...] = tuple(candidatas)


LACUNAS_POR_INTENCAO: Mapping[Intencao, tuple[Lacuna, ...]] = {
    # --- MATERIALIZAR: o catálogo inteiro já foi escrito para este caso. O que ele
    #     não pergunta é o que cerca a construção do zero: o que já está decidido
    #     por fora, o que o sistema herda no primeiro dia e quem fica com ele.
    Intencao.MATERIALIZAR: (
        Lacuna(
            id="mat_stack_imposta",
            pergunta="Já existe linguagem, banco ou nuvem decidida por quem paga, ou a escolha é livre?",
            porque=(
                "Escolher a stack é a primeira decisão cara deste trabalho, e ela se "
                "toma uma vez. Descobrir na entrega que a casa só opera uma "
                "plataforma não custa uma migração: custa tudo o que foi construído "
                "em cima da escolha errada."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="mat_dado_inicial",
            pergunta="Nasce vazio, ou já precisa começar com o que hoje está em planilha ou em outro sistema?",
            porque=(
                "Carga inicial é o trabalho que ninguém orça e que decide o modelo de "
                "dados, porque o modelo tem de aceitar o que existe, e não o que "
                "seria bonito. Um sistema que nasce vazio e um que nasce com dez anos "
                "de histórico são dois projetos com a mesma descrição."
            ),
            peso=7,
            universal=False,
        ),
        Lacuna(
            id="mat_quem_mantem",
            pergunta="Depois de entregue, quem mexe no código quando precisar mudar?",
            porque=(
                "Quem mantém restringe o que se pode escolher. Stack que ninguém na "
                "casa lê entrega software que congela no dia da entrega, e o congelamento "
                "não aparece como defeito — aparece como pedido que nunca é atendido."
            ),
            peso=7,
            universal=False,
        ),
    ),
    # --- ARQUITETAR: decidir estrutura. As perguntas são sobre reversibilidade e
    #     sobre o que já está dado — nunca sobre a solução, que é a saída.
    Intencao.ARQUITETAR: (
        Lacuna(
            id="arq_decisao_cara",
            pergunta="Qual destas decisões é a cara de reverter daqui a um ano, e por quê?",
            porque=(
                "Arquitetura é o conjunto das decisões caras de reverter, e só isso. "
                "Sem nomear qual é a cara, o esforço se distribui por igual entre o "
                "que trava o projeto por dois anos e o que se troca numa tarde."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="arq_alternativa_descartada",
            pergunta="Que alternativa já foi considerada e descartada, e qual foi o motivo?",
            porque=(
                "Em dois anos ninguém lembra da alternativa descartada, e alguém a "
                "propõe de novo com energia. O registro do descarte é o que impede a "
                "mesma discussão de recomeçar do zero — e o que permite reabri-la de "
                "propósito, quando o motivo do descarte deixar de valer."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="arq_restricao_dada",
            pergunta="O que já está dado e não se negocia: nuvem, banco, licença, tamanho da equipe?",
            porque=(
                "Desenho que ignora restrição existente é exercício: ele volta para a "
                "mesa na primeira revisão, e o tempo gasto nele não vira nada. "
                "Restrição declarada antes reduz o espaço de escolha, que é "
                "exatamente o que se quer de uma decisão arquitetural."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="arq_escala_esperada",
            pergunta="Quantos usuários e quanto dado no primeiro ano, e no terceiro?",
            porque=(
                "Estrutura dimensionada para número que ninguém disse erra dos dois "
                "lados: cara demais hoje, ou remendo em dezoito meses. O número não "
                "precisa ser certo, precisa ser dito por alguém que responda por ele."
            ),
            peso=6,
            universal=False,
        ),
    ),
    # --- REVISAR: diagnóstico de código que existe. O recorte é a pergunta principal,
    #     porque revisão sem fronteira é leitura infinita e relatório raso.
    Intencao.REVISAR: (
        Lacuna(
            id="rev_alvo",
            pergunta="O que entra na revisão: um diff, um arquivo, um módulo, ou o sistema inteiro?",
            porque=(
                "Revisão sem fronteira declarada vira leitura sem fim, e o relatório "
                "sai raso em tudo. O recorte não é limitação: é o que permite ser "
                "fundo em alguma coisa, que é a única entrega que uma revisão faz."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="rev_severidade_minima",
            pergunta="O que precisa sair no relatório: só o que quebra, ou também design e estilo?",
            porque=(
                "Achado de estilo misturado com defeito de correção ensina quem lê a "
                "ignorar a lista inteira. Quando o relatório volta com trinta itens e "
                "quatro importam, os quatro morrem junto com os outros vinte e seis."
            ),
            peso=6,
            universal=False,
        ),
        Lacuna(
            id="rev_quem_corrige",
            pergunta="Quem aplica a correção depois, e ela pode entrar hoje mesmo?",
            porque=(
                "Revisão é diagnóstico, e o diagnóstico se escreve para quem vai "
                "agir. Sem saber quem corrige, o relatório erra o nível: explica "
                "demais para quem escreveu o código, ou de menos para quem o herdou "
                "ontem."
            ),
            peso=5,
            universal=False,
        ),
    ),
    # --- OTIMIZAR: o motor força Número-Primeira, e a primeira lacuna é o número.
    Intencao.OTIMIZAR: (
        Lacuna(
            id="perf_medicao_atual",
            pergunta="Qual é o número de hoje — medido como, em qual máquina e com qual volume?",
            porque=(
                "Otimização sem medição é adivinhação com custo de manutenção "
                "permanente. Sem linha de base não há como provar ganho, e o que é "
                "pior, não há como perceber piora: o código fica mais complicado e "
                "ninguém consegue dizer se ficou mais rápido."
            ),
            peso=10,
            universal=False,
        ),
        Lacuna(
            id="perf_meta",
            pergunta="Qual número seria aceitável, e quem definiu esse número?",
            porque=(
                "Sem alvo declarado a otimização termina quando alguém cansa, e o "
                "último ganho costuma custar mais do que vale. A meta é também a "
                "permissão para parar, que é a parte que ninguém escreve."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="perf_carga_real",
            pergunta="Qual é o volume real: quantos registros, quantas chamadas por minuto, em que horário?",
            porque=(
                "Gargalo medido em dado de brinquedo é outro gargalo. O que aparece "
                "com cem linhas não move nada com dez milhões, e o inverso também é "
                "verdade — o custo que só existe em escala não se reproduz na máquina "
                "de quem otimiza."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="perf_troca_aceitavel",
            pergunta="A saída pode mudar em troca de velocidade: arredondar, aproximar, atrasar, mostrar dado de minutos atrás?",
            porque=(
                "Boa parte do ganho barato exige afrouxar exatidão ou atualidade, e "
                "isso é decisão de negócio, não de implementação. Tomada em silêncio "
                "dentro do código, ela vira defeito relatado meses depois por quem "
                "conferia o número na mão."
            ),
            peso=6,
            universal=False,
        ),
    ),
    # --- DIAGRAMAR: comunicar estrutura. Tudo aqui é sobre o leitor.
    Intencao.DIAGRAMAR: (
        Lacuna(
            id="dia_pergunta_do_leitor",
            pergunta="Que pergunta a pessoa precisa conseguir responder depois de olhar o desenho?",
            porque=(
                "Diagrama é ferramenta de comunicação, não de documentação por "
                "cumprimento. Sem a pergunta declarada ele sai completo e ilegível, "
                "que é a forma mais comum de diagrama inútil: tudo está lá e ninguém "
                "acha nada."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="dia_publico",
            pergunta="Quem lê: quem escreve o código, quem paga a conta, ou quem opera de madrugada?",
            porque=(
                "O nível de detalhe é escolhido pelo leitor, e nunca pelo tamanho do "
                "sistema. O mesmo desenho serve bem a um dos três e desperdiça os "
                "outros dois, e a escolha de servir aos três produz o que não serve a "
                "nenhum."
            ),
            peso=7,
            universal=False,
        ),
        Lacuna(
            id="dia_onde_vive",
            pergunta="Onde o desenho vai morar, e quem o atualiza quando o sistema mudar?",
            porque=(
                "Diagrama sem dono envelhece em silêncio e passa a descrever um "
                "sistema que não existe mais. Isso é pior que ausência de diagrama, "
                "porque quem lê acredita, e a decisão errada tem a aparência de estar "
                "fundamentada."
            ),
            peso=5,
            universal=False,
        ),
    ),
    # --- EVOLUIR: a classe que a fase `EVOLUCAO` e o `cartografo` já supunham, e que
    #     nenhum motor cobre. Tudo aqui gira em torno do que já funciona.
    Intencao.EVOLUIR: (
        Lacuna(
            id="evo_comportamento_preservado",
            pergunta="O que precisa continuar funcionando exatamente como hoje, mesmo que seja feio?",
            porque=(
                "Em sistema que já roda, quase todo o valor está no que já funciona. "
                "Mudança que não declara o intocável quebra o intocável, e a quebra "
                "não aparece no teste de quem mudou: aparece no telefonema de quem "
                "usa, dias depois."
            ),
            peso=10,
            universal=False,
        ),
        Lacuna(
            id="evo_quem_depende",
            pergunta="Quem consome isto hoje: outro sistema, relatório, planilha, integração, alguém copiando na mão?",
            porque=(
                "Consumidor não mapeado quebra na primeira mudança de formato, e ele "
                "descobre antes de quem mudou. O consumo informal — a planilha que "
                "alguém alimenta copiando da tela — é o que nunca está no diagrama e "
                "é o primeiro a parar."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="evo_reversao",
            pergunta="Se a mudança der errado com o sistema no ar, como se volta ao estado anterior, e em quanto tempo?",
            porque=(
                "Em sistema em uso a pergunta não é se algo vai falhar, e sim quanto "
                "tempo se leva para desfazer. Caminho de volta não se improvisa às "
                "três da manhã, e a resposta muda o desenho da mudança — nem toda "
                "alteração de dado se desfaz."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="evo_janela",
            pergunta="Existe janela em que a mudança pode entrar, ou horário em que ela não pode?",
            porque=(
                "Sistema em uso tem hora do dia que não aceita risco, e isso raramente "
                "está escrito em algum lugar. Descobrir a janela depois de publicar "
                "transforma uma melhoria em incidente, com o mesmo código."
            ),
            peso=6,
            universal=False,
        ),
    ),
    # --- AUTOMATIZAR: `Plataforma.AUTOMACAO` já pergunta gatilho, falha no meio,
    #     frequência e formato de saída. Estas quatro são sobre o trabalho humano que
    #     está sendo substituído e sobre o que a plataforma não alcança.
    Intencao.AUTOMATIZAR: (
        Lacuna(
            id="auto_processo_manual_hoje",
            pergunta="Como esse trabalho é feito hoje na mão, passo a passo, e por quem?",
            porque=(
                "Automatizar processo que ninguém descreveu automatiza a versão "
                "imaginada dele. Os passos que não estão no papel são justamente os "
                "que existem por causa de exceção, e a exceção é o que a automação "
                "encontra na segunda semana."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="auto_reexecucao",
            pergunta="Rodar duas vezes no mesmo dia produz o mesmo resultado, ou duplica?",
            porque=(
                "Toda rotina é reexecutada em algum momento — por falha, por "
                "recuperação de atraso ou por engano de quem opera. Se a segunda "
                "execução duplica, a correção de um problema pequeno cria um maior, e "
                "a duplicata é descoberta na conferência, não na hora."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="auto_quem_vigia",
            pergunta="Quando a rotina falhar, quem recebe o aviso, por qual canal, e em quanto tempo?",
            porque=(
                "Automação sem destinatário de falha é automação que para em "
                "silêncio. A descoberta vem pelo efeito — o relatório que não chegou, "
                "o saldo que não bate — semanas depois, quando refazer o período "
                "custa mais que o trabalho manual que ela substituiu."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="auto_credencial",
            pergunta="Com qual credencial ela roda, e o que acontece quando essa senha vencer ou a pessoa sair?",
            porque=(
                "Rotina que roda sozinha roda com a permissão de alguém. Senha que "
                "vence derruba a rotina em silêncio, e credencial de pessoa que "
                "deixou a empresa derruba junto com o acesso dela — sempre no dia em "
                "que ninguém está olhando."
            ),
            peso=7,
            universal=False,
        ),
    ),
    # --- INTEGRAR: `Contexto.INTEGRACAO_EXTERNA` já pergunta qual sistema e o que
    #     fazer quando ele cair. Estas quatro são sobre o contrato e sobre o custo de
    #     descobri-lo errado.
    Intencao.INTEGRAR: (
        Lacuna(
            id="int_contrato",
            pergunta="Existe documentação do que esse sistema aceita e devolve, e ela está atualizada?",
            porque=(
                "Contrato descoberto por tentativa custa caro e custa rápido: chamada "
                "repetida em laço bloqueia a credencial, e depois do bloqueio toda "
                "leitura devolve a mensagem de bloqueio — que é lida como resposta do "
                "sistema. Uma consulta à documentação resolve o que a força bruta não "
                "resolve em trinta minutos."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="int_dono_do_dado",
            pergunta="Quando os dois lados discordarem do mesmo dado, qual deles está certo?",
            porque=(
                "Integração sem dono declarado do dado produz sincronização que "
                "oscila: cada lado sobrescreve o outro na sua vez, e o histórico não "
                "diz quem começou. A pergunta é de negócio e não tem resposta técnica."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="int_limite_de_uso",
            pergunta="Quantas chamadas por minuto ele aceita, e o que ele faz quando esse limite estoura?",
            porque=(
                "Limite de uso não é detalhe de desempenho: estourá-lo costuma "
                "bloquear a credencial inteira, e o bloqueio atinge todo mundo que "
                "usa aquela credencial — inclusive quem não tem nada a ver com o laço "
                "que estourou."
            ),
            peso=7,
            universal=False,
        ),
        Lacuna(
            id="int_ambiente_de_prova",
            pergunta="Existe ambiente de teste desse sistema, ou a primeira tentativa já é para valer?",
            porque=(
                "Sem ambiente de prova, cada tentativa produz efeito real do outro "
                "lado — pedido criado, mensagem enviada, lançamento gravado. Isso muda "
                "a forma de trabalhar inteira, e é decisão a tomar antes da primeira "
                "linha, não depois do primeiro estrago."
            ),
            peso=6,
            universal=False,
        ),
    ),
    # --- TRATAR_DADOS: cartões `power-query`, `excel-vba` e `office-scripts` existem
    #     há tempo, e nenhuma pergunta os acompanhava.
    Intencao.TRATAR_DADOS: (
        Lacuna(
            id="dado_fonte_da_verdade",
            pergunta="De onde o dado sai, e quem responde por ele quando estiver errado?",
            porque=(
                "Transformação herda a qualidade da fonte e, na hora do erro, herda a "
                "culpa por ela. Sem dono da fonte declarado, todo número estranho vira "
                "investigação do transporte — que é onde não está o problema."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="dado_regra_de_fechamento",
            pergunta="Como se confere que o resultado bate: qual total tem de fechar com qual?",
            porque=(
                "Transformação sem número de fechamento entrega resultado plausível e "
                "errado, que é o pior tipo de saída porque ninguém desconfia. A única "
                "defesa barata é um total conhecido de antemão que precisa reaparecer "
                "no fim."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="dado_volume_e_formato",
            pergunta="Quantas linhas, em qual formato, e o arquivo chega sempre com as mesmas colunas?",
            porque=(
                "Volume decide a ferramenta e estabilidade de formato decide o custo "
                "de manutenção. Planilha que muda de coluna quando alguém acha bom "
                "quebra a rotina toda vez, e quebra sem avisar quem a mudou."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="dado_historico",
            pergunta="Quando a regra mudar, o que já foi processado é reprocessado ou fica como está?",
            porque=(
                "Mudança de regra sem decisão sobre o passado produz base com duas "
                "verdades e nenhuma marca de onde uma termina. Meses depois, comparar "
                "dois períodos deixa de ser possível e ninguém sabe por quê."
            ),
            peso=6,
            universal=False,
        ),
    ),
    # --- TESTAR: fase `TESTE`, papel `testador` e cartão `pytest` existiam sem uma
    #     pergunta sequer sobre o que se está protegendo.
    Intencao.TESTAR: (
        Lacuna(
            id="teste_o_que_nao_pode_quebrar",
            pergunta="Que comportamento, se quebrar, ninguém percebe até virar prejuízo?",
            porque=(
                "Cobertura distribuída por igual gasta esforço onde a falha é visível "
                "e barata. Teste vale pelo que protege, e o que ele protege precisa "
                "ser nomeado por alguém que conheça o custo — não escolhido pelo que "
                "é fácil de testar."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="teste_estado_atual",
            pergunta="Existe suíte hoje? Ela passa inteira, e quanto tempo leva?",
            porque=(
                "Suíte já vermelha, ou lenta demais para ser rodada, não é ponto de "
                "partida: é o primeiro problema. Construir em cima dela esconde a "
                "regressão nova no meio da falha velha, e a partir daí ninguém mais "
                "olha o resultado."
            ),
            peso=7,
            universal=False,
        ),
        Lacuna(
            id="teste_dado_de_prova",
            pergunta="De onde vem o dado usado no teste: inventado, gerado, ou copiado de produção?",
            porque=(
                "Dado copiado de produção carrega dado pessoal para dentro do "
                "repositório, onde ele fica no histórico mesmo depois de apagado. "
                "Dado inventado demais não reproduz o caso que quebra, e a suíte fica "
                "verde sobre o que nunca acontece."
            ),
            peso=7,
            universal=False,
        ),
        Lacuna(
            id="teste_quem_roda",
            pergunta="Quem roda a suíte e quando: a pessoa antes de publicar, ou a máquina depois?",
            porque=(
                "Teste que só roda quando alguém lembra é teste que não roda. O "
                "momento da execução é o que decide se ele é portão — impede a "
                "entrada — ou relatório, que é o mesmo que enfeite."
            ),
            peso=6,
            universal=False,
        ),
    ),
    # --- PROTEGER: o papel `sentinela` existe e não tinha pergunta de elicitação.
    Intencao.PROTEGER: (
        Lacuna(
            id="seg_o_que_protege",
            pergunta="O que exatamente não pode vazar nem ser alterado, e o que acontece se acontecer?",
            porque=(
                "Segurança sem ativo nomeado vira lista de boas práticas aplicada por "
                "igual em tudo, que é a forma mais cara de proteger pouco. A "
                "consequência declarada é o que decide onde vale gastar."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="seg_de_quem_se_defende",
            pergunta="De quem se está defendendo: erro de quem usa, curioso de dentro, ou ataque dirigido?",
            porque=(
                "Os três exigem defesas diferentes e mutuamente inúteis. Defender-se "
                "do adversário errado entrega a sensação de proteção sem a proteção, "
                "e a sensação é o que impede a próxima pergunta."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="seg_segredo_onde_mora",
            pergunta="Onde as senhas e chaves ficam hoje, e quem consegue lê-las?",
            porque=(
                "Segredo dentro do código é o vazamento mais comum e o mais barato de "
                "evitar antes de existir. Depois de gravado no histórico ele "
                "permanece lá mesmo apagado do arquivo, e a correção deixa de ser "
                "editar uma linha."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="seg_registro_de_acesso",
            pergunta="É preciso poder provar depois quem fez o quê, e por quanto tempo esse registro fica?",
            porque=(
                "Registro de acesso acrescentado depois não cobre o período anterior, "
                "e o período auditado é sempre o anterior. A decisão é de antes, "
                "porque ela não tem versão retroativa."
            ),
            peso=7,
            universal=False,
        ),
    ),
    # --- DOCUMENTAR: fase `DOC` e papel `documentador` existiam sem pergunta.
    Intencao.DOCUMENTAR: (
        Lacuna(
            id="doc_quem_le_e_quando",
            pergunta="Quem lê isto, e em que momento: ao chegar no projeto, ou no meio de um incidente?",
            porque=(
                "Documento de chegada e documento de emergência têm formatos opostos "
                "— um explica o contexto, o outro entrega o comando na primeira linha. "
                "Escrever um só servindo aos dois produz um texto longo que ninguém "
                "abre com pressa."
            ),
            peso=8,
            universal=False,
        ),
        Lacuna(
            id="doc_o_que_ja_existe",
            pergunta="O que já está escrito hoje sobre isto, e onde mora?",
            porque=(
                "Documentação nova ao lado da antiga produz duas versões e nenhuma "
                "autoridade. Quem lê escolhe uma das duas sem saber que escolheu, e a "
                "errada tem exatamente a mesma aparência de correta."
            ),
            peso=7,
            universal=False,
        ),
        Lacuna(
            id="doc_o_que_envelhece",
            pergunta="Que parte disto muda toda semana, e como o texto acompanha essa mudança?",
            porque=(
                "Documento que descreve o que muda vira mentira em silêncio, e mentira "
                "documentada é consultada com confiança. A parte volátil ou é gerada "
                "a partir do código, ou fica deliberadamente de fora com o motivo "
                "escrito."
            ),
            peso=7,
            universal=False,
        ),
    ),
    # --- OPERAR: infraestrutura, publicação e observabilidade. Três volumes do
    #     acervo (`19`, `20`, `21`) e nenhuma pergunta.
    Intencao.OPERAR: (
        Lacuna(
            id="ops_como_publica_hoje",
            pergunta="Como uma mudança chega hoje em produção, passo a passo, e quem faz isso?",
            porque=(
                "O caminho de publicação existente é a restrição real de qualquer "
                "melhoria. Desenhar em cima de um caminho imaginado entrega automação "
                "que ninguém consegue usar, e o time volta para o passo manual sem "
                "avisar que voltou."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="ops_como_se_descobre_a_falha",
            pergunta="Quando quebrar em produção, o que avisa, e avisa antes de quem?",
            porque=(
                "Sistema cuja falha é descoberta pelo cliente já pagou o incidente "
                "inteiro antes de a equipe saber. Sem sinal próprio, todo investimento "
                "em resiliência fica invisível — inclusive para quem decide se ele "
                "continua."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="ops_indisponibilidade_aceitavel",
            pergunta="Quanto tempo fora do ar por mês é aceitável, e para quem?",
            porque=(
                "Este número separa o que precisa de redundância do que precisa "
                "apenas de um bom procedimento de religar, e a diferença de custo "
                "entre os dois é de ordem de grandeza. Sem ele, escolhe-se o caro por "
                "precaução ou o barato por otimismo."
            ),
            peso=7,
            universal=False,
        ),
        Lacuna(
            id="ops_custo_mensal",
            pergunta="Qual é o teto de custo mensal da infraestrutura, e quem vê essa conta?",
            porque=(
                "Infraestrutura é a parte que continua cobrando depois de pronta. "
                "Conta sem dono cresce até alguém se assustar, e o susto costuma "
                "chegar junto com uma ordem de desligar o que estava funcionando."
            ),
            peso=6,
            universal=False,
        ),
    ),
    # --- CONSTRUIR_IA: sete volumes do acervo (`07`, `08`, `26`–`30`) e nenhuma
    #     pergunta. É a classe onde a saída errada tem a melhor aparência.
    Intencao.CONSTRUIR_IA: (
        Lacuna(
            id="ia_criterio_de_acerto",
            pergunta="Como se sabe que a resposta do modelo está certa, e quem julga isso?",
            porque=(
                "Sistema de IA sem critério de acerto não se avalia e, por "
                "consequência, não se melhora: cada mudança de prompt é uma troca de "
                "impressão por impressão. A demonstração inicial é o pior juiz "
                "disponível, porque foi escolhida para funcionar."
            ),
            peso=10,
            universal=False,
        ),
        Lacuna(
            id="ia_o_que_acontece_no_erro",
            pergunta="Quando o modelo errar — e vai errar —, quem percebe antes de o erro virar ação?",
            porque=(
                "A saída errada de um modelo é fluente e confiante, e por isso circula "
                "com a mesma autoridade da correta. Sem ponto de revisão declarado, o "
                "erro não é filtrado por ninguém: ele é executado."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="ia_dado_que_sai_da_casa",
            pergunta="Que dado é enviado para o modelo, e ele pode sair da empresa?",
            porque=(
                "Prompt é dado entregue a terceiro, e quase nunca é tratado como tal. "
                "Descobrir isso depois de um mês de uso é descobrir um vazamento "
                "contínuo que já aconteceu, e para o qual não existe desfazer."
            ),
            peso=9,
            universal=False,
        ),
        Lacuna(
            id="ia_custo_por_uso",
            pergunta="Quanto custa cada chamada, e quantas por dia se espera no uso real?",
            porque=(
                "Custo por chamada transforma volume em conta mensal, e o volume real "
                "costuma ficar uma ordem de grandeza acima do estimado na "
                "demonstração. A conta chega depois da decisão de adotar, quando "
                "voltar atrás já custa."
            ),
            peso=7,
            universal=False,
        ),
    ),
}


#: Termo, intenção e confiança — a mesma forma das tabelas de `deteccao.py`.
#:
#: A ordem tem os mesmos dois papéis de lá: define qual termo produz a evidência
#: quando dois casam a mesma intenção (o primeiro ganha) e é a ordem de leitura de
#: quem revisar a tabela. Nenhum termo aparece em duas intenções, e
#: `validar_taxonomia` reprova se aparecer — termo compartilhado alimenta os dois
#: lados do placar e fabrica empate onde não havia dúvida.
#:
#: Um termo pode, e deve, repetir termo de `deteccao.py`: "automatizar" indica ao
#: mesmo tempo a plataforma AUTOMACAO e a intenção AUTOMATIZAR. Os eixos são
#: ortogonais, e o mesmo pedaço de texto pode provar coisas de eixos diferentes.
_TERMOS_INTENCAO: tuple[tuple[str, Intencao, str], ...] = (
    # --- MATERIALIZAR
    ("do zero", Intencao.MATERIALIZAR, CONFIANCA_ALTA),
    ("ainda nao existe", Intencao.MATERIALIZAR, CONFIANCA_ALTA),
    ("nao existe ainda", Intencao.MATERIALIZAR, CONFIANCA_ALTA),
    ("sistema novo", Intencao.MATERIALIZAR, CONFIANCA_ALTA),
    ("virar produto", Intencao.MATERIALIZAR, CONFIANCA_MEDIA),
    ("prototipo", Intencao.MATERIALIZAR, CONFIANCA_MEDIA),
    ("quero um sistema", Intencao.MATERIALIZAR, CONFIANCA_MEDIA),
    ("preciso de um sistema", Intencao.MATERIALIZAR, CONFIANCA_MEDIA),
    ("criar um", Intencao.MATERIALIZAR, CONFIANCA_BAIXA),
    # --- ARQUITETAR
    ("como estruturar", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("onde devo colocar", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("vale a pena separar", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("qual padrao usar", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("monolito", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("microservico", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("microservicos", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("acoplamento", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("decisao arquitetural", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    ("arquitetura", Intencao.ARQUITETAR, CONFIANCA_MEDIA),
    ("fronteira entre modulos", Intencao.ARQUITETAR, CONFIANCA_ALTA),
    # --- REVISAR
    ("revisar", Intencao.REVISAR, CONFIANCA_ALTA),
    ("revisa", Intencao.REVISAR, CONFIANCA_ALTA),
    ("revisao de codigo", Intencao.REVISAR, CONFIANCA_ALTA),
    ("code review", Intencao.REVISAR, CONFIANCA_ALTA),
    ("ta bom assim", Intencao.REVISAR, CONFIANCA_ALTA),
    ("esta bom assim", Intencao.REVISAR, CONFIANCA_ALTA),
    ("tem de errado", Intencao.REVISAR, CONFIANCA_ALTA),
    ("olha esse pr", Intencao.REVISAR, CONFIANCA_ALTA),
    ("esse bug", Intencao.REVISAR, CONFIANCA_MEDIA),
    ("stack trace", Intencao.REVISAR, CONFIANCA_MEDIA),
    # --- OTIMIZAR
    ("otimizar", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("ta lento", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("esta lento", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("demora demais", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("timeout", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("latencia", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("performance", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("desempenho", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("consumo de memoria", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("pico de cpu", Intencao.OTIMIZAR, CONFIANCA_ALTA),
    ("lento", Intencao.OTIMIZAR, CONFIANCA_MEDIA),
    ("mais rapido", Intencao.OTIMIZAR, CONFIANCA_MEDIA),
    ("trava", Intencao.OTIMIZAR, CONFIANCA_BAIXA),
    # --- DIAGRAMAR
    ("diagrama", Intencao.DIAGRAMAR, CONFIANCA_ALTA),
    ("fluxograma", Intencao.DIAGRAMAR, CONFIANCA_ALTA),
    ("mermaid", Intencao.DIAGRAMAR, CONFIANCA_ALTA),
    ("mostra o fluxo", Intencao.DIAGRAMAR, CONFIANCA_ALTA),
    ("como isso se conecta", Intencao.DIAGRAMAR, CONFIANCA_ALTA),
    ("desenha", Intencao.DIAGRAMAR, CONFIANCA_ALTA),
    ("desenhar", Intencao.DIAGRAMAR, CONFIANCA_MEDIA),
    ("organograma", Intencao.DIAGRAMAR, CONFIANCA_MEDIA),
    # --- EVOLUIR
    ("sistema existente", Intencao.EVOLUIR, CONFIANCA_ALTA),
    ("sistema atual", Intencao.EVOLUIR, CONFIANCA_ALTA),
    ("que ja roda", Intencao.EVOLUIR, CONFIANCA_ALTA),
    ("ja existe", Intencao.EVOLUIR, CONFIANCA_ALTA),
    ("nova funcionalidade", Intencao.EVOLUIR, CONFIANCA_ALTA),
    ("acrescentar ao sistema", Intencao.EVOLUIR, CONFIANCA_ALTA),
    ("legado", Intencao.EVOLUIR, CONFIANCA_ALTA),
    ("sem quebrar o que", Intencao.EVOLUIR, CONFIANCA_ALTA),
    ("mudar o comportamento", Intencao.EVOLUIR, CONFIANCA_MEDIA),
    ("em producao ha", Intencao.EVOLUIR, CONFIANCA_MEDIA),
    # --- AUTOMATIZAR
    ("automatizar", Intencao.AUTOMATIZAR, CONFIANCA_ALTA),
    ("automacao", Intencao.AUTOMATIZAR, CONFIANCA_ALTA),
    ("sem intervencao", Intencao.AUTOMATIZAR, CONFIANCA_ALTA),
    ("agendada", Intencao.AUTOMATIZAR, CONFIANCA_ALTA),
    ("agendado", Intencao.AUTOMATIZAR, CONFIANCA_MEDIA),
    ("toda noite", Intencao.AUTOMATIZAR, CONFIANCA_MEDIA),
    ("todo dia as", Intencao.AUTOMATIZAR, CONFIANCA_MEDIA),
    ("na mao hoje", Intencao.AUTOMATIZAR, CONFIANCA_MEDIA),
    ("manualmente", Intencao.AUTOMATIZAR, CONFIANCA_MEDIA),
    ("robo", Intencao.AUTOMATIZAR, CONFIANCA_MEDIA),
    ("rotina", Intencao.AUTOMATIZAR, CONFIANCA_BAIXA),
    # --- INTEGRAR
    ("integrar com", Intencao.INTEGRAR, CONFIANCA_ALTA),
    ("integracao com", Intencao.INTEGRAR, CONFIANCA_ALTA),
    ("sincronizar com", Intencao.INTEGRAR, CONFIANCA_ALTA),
    ("webhook", Intencao.INTEGRAR, CONFIANCA_ALTA),
    ("api do", Intencao.INTEGRAR, CONFIANCA_ALTA),
    ("api da", Intencao.INTEGRAR, CONFIANCA_ALTA),
    ("sistema de terceiro", Intencao.INTEGRAR, CONFIANCA_ALTA),
    ("conectar com", Intencao.INTEGRAR, CONFIANCA_MEDIA),
    ("puxar do", Intencao.INTEGRAR, CONFIANCA_MEDIA),
    ("importar de", Intencao.INTEGRAR, CONFIANCA_MEDIA),
    # --- TRATAR_DADOS
    ("planilha", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("excel", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("csv", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("etl", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("power query", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("consolidar", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("cruzar as bases", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("tratar os dados", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("limpar os dados", Intencao.TRATAR_DADOS, CONFIANCA_ALTA),
    ("base de dados", Intencao.TRATAR_DADOS, CONFIANCA_MEDIA),
    # --- TESTAR
    ("teste", Intencao.TESTAR, CONFIANCA_ALTA),
    ("testes", Intencao.TESTAR, CONFIANCA_ALTA),
    ("cobertura", Intencao.TESTAR, CONFIANCA_ALTA),
    ("pytest", Intencao.TESTAR, CONFIANCA_ALTA),
    ("suite", Intencao.TESTAR, CONFIANCA_ALTA),
    ("regressao", Intencao.TESTAR, CONFIANCA_MEDIA),
    ("qualidade do codigo", Intencao.TESTAR, CONFIANCA_MEDIA),
    # --- PROTEGER
    ("seguranca", Intencao.PROTEGER, CONFIANCA_ALTA),
    ("vulnerabilidade", Intencao.PROTEGER, CONFIANCA_ALTA),
    ("vazamento", Intencao.PROTEGER, CONFIANCA_ALTA),
    ("invasao", Intencao.PROTEGER, CONFIANCA_ALTA),
    ("criptografia", Intencao.PROTEGER, CONFIANCA_ALTA),
    ("lgpd", Intencao.PROTEGER, CONFIANCA_ALTA),
    ("senha exposta", Intencao.PROTEGER, CONFIANCA_ALTA),
    ("ataque", Intencao.PROTEGER, CONFIANCA_MEDIA),
    ("credencial", Intencao.PROTEGER, CONFIANCA_MEDIA),
    # --- DOCUMENTAR
    ("documentar", Intencao.DOCUMENTAR, CONFIANCA_ALTA),
    ("documentacao", Intencao.DOCUMENTAR, CONFIANCA_ALTA),
    ("readme", Intencao.DOCUMENTAR, CONFIANCA_ALTA),
    ("guia de uso", Intencao.DOCUMENTAR, CONFIANCA_ALTA),
    ("material de treinamento", Intencao.DOCUMENTAR, CONFIANCA_ALTA),
    ("manual", Intencao.DOCUMENTAR, CONFIANCA_MEDIA),
    ("explicar como funciona", Intencao.DOCUMENTAR, CONFIANCA_MEDIA),
    # --- OPERAR
    ("deploy", Intencao.OPERAR, CONFIANCA_ALTA),
    ("publicar em producao", Intencao.OPERAR, CONFIANCA_ALTA),
    ("infraestrutura", Intencao.OPERAR, CONFIANCA_ALTA),
    ("kubernetes", Intencao.OPERAR, CONFIANCA_ALTA),
    ("observabilidade", Intencao.OPERAR, CONFIANCA_ALTA),
    ("monitoramento", Intencao.OPERAR, CONFIANCA_ALTA),
    ("pipeline de entrega", Intencao.OPERAR, CONFIANCA_ALTA),
    ("docker", Intencao.OPERAR, CONFIANCA_MEDIA),
    ("servidor", Intencao.OPERAR, CONFIANCA_MEDIA),
    ("fora do ar", Intencao.OPERAR, CONFIANCA_MEDIA),
    # --- CONSTRUIR_IA
    ("prompt", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
    ("agente de ia", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
    ("llm", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
    ("modelo de linguagem", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
    ("inteligencia artificial", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
    ("chatbot", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
    ("embedding", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
    ("rag", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
    ("fine tuning", Intencao.CONSTRUIR_IA, CONFIANCA_ALTA),
)

#: Quanto vale cada nível de confiança no placar. Não é probabilidade: é ordem de
#: grandeza entre "o termo nomeia o trabalho" e "o termo aparece em quem faz esse
#: trabalho e em mais três". Três contra dois contra um mantém a propriedade que
#: interessa — dois sinais fracos não derrubam um forte, e dois fortes derrubam
#: qualquer coisa.
PONTOS_POR_CONFIANCA: Mapping[str, int] = {
    CONFIANCA_ALTA: 3,
    CONFIANCA_MEDIA: 2,
    CONFIANCA_BAIXA: 1,
}

#: Abaixo disto o texto não decide nada. Um único termo de confiança BAIXA — "rotina",
#: "trava", "criar um" — aparece em pedido de qualquer classe, e deixá-lo classificar
#: sozinho seria o chute com aparência de método. Dois pontos exigem ou um termo de
#: confiança média, ou dois fracos concordando.
PONTOS_MINIMOS = 2


def _como_intencao(valor: Intencao | str) -> Intencao:
    """Traduz texto para membro de `Intencao`, ou levanta `IntencaoDesconhecida`.

    Existe para que a fronteira do módulo aceite texto — que é o que atravessa
    arquivo de estado e linha de comando — sem que o erro de digitação vire silêncio.
    """
    if isinstance(valor, Intencao):
        return valor
    try:
        return Intencao(str(valor).strip().upper())
    except ValueError as erro:
        raise IntencaoDesconhecida(
            f"intencao {valor!r} nao existe na taxonomia; conhecidas: "
            f"{', '.join(i.value for i in Intencao)}"
        ) from erro


def _sinais(pedido: str) -> dict[Intencao, list[tuple[str, str, str]]]:
    """Para cada intenção, os termos que casaram: (termo, confiança, trecho original).

    Mesmo mecanismo de `deteccao._detectar`, com uma diferença deliberada: lá um alvo
    para no primeiro termo que casa, porque o que se produz é um palpite e um palpite
    basta uma evidência. Aqui todos os termos de uma intenção contam, porque o que se
    produz é um placar — e "está lento, dá timeout e a latência subiu" tem de pesar
    mais que uma menção solta a `revisar`.

    Dentro de um mesmo termo, ainda vale a primeira ocorrência: repetir a palavra
    quatro vezes na mesma frase não é evidência quatro vezes melhor.
    """
    dobrado, mapa = _dobrar(pedido or "")
    achados: dict[Intencao, list[tuple[str, str, str]]] = {}
    if not dobrado.strip():
        return achados

    for termo, intencao, confianca in _TERMOS_INTENCAO:
        posicao = 0
        while True:
            achou = dobrado.find(termo, posicao)
            if achou < 0:
                break
            if _fronteira(dobrado, achou, achou + len(termo)):
                achados.setdefault(intencao, []).append(
                    (termo, confianca, _trecho_em(pedido, mapa[achou]))
                )
                break
            posicao = achou + 1
    return achados


def _placar(pedido: str) -> list[tuple[int, Intencao]]:
    """Pontuação por intenção, da maior para a menor, com desempate estável por nome.

    O desempate por nome **não** escolhe vencedor: ele apenas torna a ordem do
    relatório previsível. Quem decide o empate é `classificar`, levantando.
    """
    achados = _sinais(pedido)
    return sorted(
        (
            (sum(PONTOS_POR_CONFIANCA[confianca] for _, confianca, _ in itens), intencao)
            for intencao, itens in achados.items()
        ),
        key=lambda par: (-par[0], par[1].name),
    )


def sinais_de_intencao(pedido: str) -> tuple[Palpite, ...]:
    """Um palpite por intenção detectada, com o trecho do texto que a produziu.

    Existe pelo mesmo motivo que `deteccao.detectar_plataformas`: quem recebe a
    classificação tem direito de perguntar "por que você achou isso?" e receber de
    volta um pedaço do que escreveu, e não a alegação de que uma tabela casou.

    A ordem é a da tabela de termos, e a evidência é a do primeiro termo que casou —
    as duas regras iguais às de `deteccao.py`, para que a mesma leitura sirva aos dois
    módulos. `confianca` é a do termo que deu a evidência, e não a do placar: um
    palpite não vira certeza por ter somado pontos.
    """
    return tuple(
        Palpite(
            valor=str(intencao),
            origem=Origem.INFERIDO,
            evidencia=itens[0][2],
            confianca=itens[0][1],
        )
        for intencao, itens in _sinais(pedido).items()
    )


def classificar(pedido: str) -> Intencao:
    """A intenção do pedido — ou `IntencaoIndeterminada`, que também é resposta.

    Três saídas e nenhum padrão. Vence quem tiver o maior placar, desde que o placar
    alcance `PONTOS_MINIMOS` e ninguém empate com ele. Ausência de sinal levanta;
    empate levanta com as candidatas dentro da exceção, para que quem chamou consiga
    perguntar em vez de sortear.

    **Por que não devolver a primeira da lista no empate.** É a regra R1 do acervo
    aplicada onde ela custa mais caro: sem evidência é pendência, não palpite. A
    classe escolhida aqui decide *quais perguntas existem* — errá-la não produz uma
    pergunta ruim no meio de vinte boas, produz uma entrevista inteira sobre outro
    trabalho, e a pessoa responde tudo antes de alguém notar. Uma pergunta de
    desempate custa um turno; o padrão silencioso custa a entrevista.
    """
    placar = _placar(pedido)
    if not placar:
        raise IntencaoIndeterminada(
            "nenhum sinal de intencao no pedido: nao da para dizer se e criar, "
            "evoluir, revisar, otimizar ou outra coisa - pergunte antes de seguir"
        )

    pontos, melhor = placar[0]
    if pontos < PONTOS_MINIMOS:
        raise IntencaoIndeterminada(
            f"sinal fraco demais para decidir (placar {pontos}, minimo "
            f"{PONTOS_MINIMOS}); o unico candidato seria {melhor.value}, e um termo "
            "de confianca baixa sozinho aparece em pedido de qualquer classe",
            candidatas=(melhor,),
        )

    empatadas = tuple(intencao for ponto, intencao in placar if ponto == pontos)
    if len(empatadas) > 1:
        raise IntencaoIndeterminada(
            "sinal ambiguo: "
            + " e ".join(intencao.value for intencao in empatadas)
            + f" empataram com {pontos} pontos; sao trabalhos diferentes e cada um "
            "abre um conjunto de perguntas proprio - pergunte qual vem primeiro",
            candidatas=empatadas,
        )
    return melhor


def lacunas_da_intencao(intencao: Intencao | str) -> tuple[Lacuna, ...]:
    """As lacunas que esta intenção acrescenta ao que plataforma e contexto já dão.

    Acrescenta é a palavra: nada aqui substitui o catálogo. Um pedido de otimização
    continua precisando saber quem usa e como se sabe que funcionou — o que muda é
    que ele passa a precisar também do número de hoje, e nenhuma plataforma jamais
    perguntaria isso.

    Intenção desconhecida levanta. Devolver tupla vazia faria a entrevista seguir sem
    nenhuma pergunta deste eixo e a especificação sair parecendo completa, que é o
    defeito que este módulo existe para não ter.
    """
    alvo = _como_intencao(intencao)
    try:
        return LACUNAS_POR_INTENCAO[alvo]
    except KeyError as erro:
        raise IntencaoDesconhecida(
            f"intencao {alvo.value} existe na enumeracao e nao tem lacuna declarada "
            "em LACUNAS_POR_INTENCAO: classificar por ela nao acrescentaria pergunta "
            "nenhuma, e o eixo ficaria decorativo"
        ) from erro


def lacunas_do_pedido(
    pedido: str,
    plataformas: Iterable[Plataforma] = (),
    contextos: Iterable[Contexto] = (),
    *,
    intencao: Intencao | str | None = None,
    catalogo: Iterable[Lacuna] = CATALOGO,
) -> tuple[Lacuna, ...]:
    """O cruzamento dos três eixos: o conjunto completo de lacunas ativas.

    Primeiro as do catálogo que plataforma e contexto destravam, na ordem do
    catálogo; depois as da intenção, na ordem em que estão declaradas. União, nunca
    escolha: acrescentar um eixo só pode acrescentar pergunta, e essa propriedade é
    o que permite conduzir a entrevista sem revisitar decisão anterior.

    `intencao` explícita existe para quando a classificação já foi feita — por uma
    pergunta de desempate, por exemplo, depois de `IntencaoIndeterminada`. Sem ela,
    o pedido é classificado aqui, e a indeterminação **sobe**: uma entrevista que
    não sabe que trabalho está sendo pedido não tem como escolher perguntas, e
    seguir com as trinta e sete universais seria fingir que sabe.

    As lacunas de intenção ainda passam por `relevante_para`. Hoje nenhuma delas
    declara plataforma ou contexto, então todas entram; a filtragem fica no caminho
    para que a primeira que precisar de um segundo gatilho — uma pergunta que só faz
    sentido ao evoluir algo que roda em nuvem, digamos — funcione sem mudança aqui.
    """
    alvo = _como_intencao(intencao) if intencao is not None else classificar(pedido)
    p = frozenset(plataformas)
    c = frozenset(contextos)

    reunidas: dict[str, Lacuna] = {
        lacuna.id: lacuna for lacuna in lacunas_ativas(p, c, catalogo=catalogo)
    }
    for lacuna in lacunas_da_intencao(alvo):
        if lacuna.relevante_para(p, c):
            reunidas.setdefault(lacuna.id, lacuna)
    return tuple(reunidas.values())


def validar_taxonomia(
    mapa: Mapping[Intencao, tuple[Lacuna, ...]] = LACUNAS_POR_INTENCAO,
    *,
    catalogo: Iterable[Lacuna] = CATALOGO,
) -> Mapping[Intencao, tuple[Lacuna, ...]]:
    """Reprova taxonomia malformada e devolve o mapa validado.

    Mesma forma de `validar_catalogo` — devolve o próprio dado para que a garantia
    ande junto dele — e as mesmas regras de conteúdo, mais três que só existem aqui:

    1. **Intenção declarada sem lacuna.** Classe que classifica e não pergunta nada
       faz o eixo existir sem efeito, e o defeito é invisível: a entrevista roda,
       sai mais curta, e ninguém liga a falta ao mapa.
    2. **Intenção sem termo na tabela.** Pior que a anterior, porque a classe fica
       inalcançável: consta da enumeração, aparece na documentação, e nenhum pedido
       chega nela. Só se descobre procurando.
    3. **Id colidindo com o catálogo.** O cruzamento indexa por id; colisão faz uma
       das duas lacunas sumir do conjunto sem erro nenhum.

    E mais uma, de fronteira entre os eixos: lacuna de intenção marcada `universal`
    não é lacuna de intenção. Universal vale para qualquer software, e o lugar dela é
    o catálogo — deixá-la aqui esconderia uma pergunta que devia ser feita sempre
    atrás de uma classificação que pode falhar.
    """
    do_catalogo = {lacuna.id for lacuna in catalogo}
    vistos: set[str] = set()

    faltando = [i for i in Intencao if i not in mapa]
    if faltando:
        raise TaxonomiaInvalida(
            "intencao sem lacuna declarada: "
            + ", ".join(i.value for i in faltando)
            + " - classe que classifica e nao acrescenta pergunta nenhuma deixa o "
            "eixo decorativo, e a falta nao aparece em execucao"
        )

    com_termo = {intencao for _, intencao, _ in _TERMOS_INTENCAO}
    sem_termo = [i for i in mapa if i not in com_termo]
    if sem_termo:
        raise TaxonomiaInvalida(
            "intencao sem termo em _TERMOS_INTENCAO: "
            + ", ".join(i.value for i in sem_termo)
            + " - `classificar` nunca chegaria nela, e a classe existiria so na "
            "enumeracao"
        )

    termos_vistos: set[str] = set()
    for termo, _, _ in _TERMOS_INTENCAO:
        if termo in termos_vistos:
            raise TaxonomiaInvalida(
                f"termo {termo!r} declarado para mais de uma intencao: ele somaria "
                "ponto para os dois lados do placar e fabricaria empate onde nao "
                "havia duvida"
            )
        termos_vistos.add(termo)

    for intencao, lacunas in mapa.items():
        if not lacunas:
            raise TaxonomiaInvalida(
                f"intencao {intencao.value} com conjunto de lacunas vazio: ela "
                "classifica e nao pergunta nada"
            )
        for lacuna in lacunas:
            identificador = lacuna.id.strip()
            if not identificador:
                raise TaxonomiaInvalida(
                    f"lacuna sem id em {intencao.value}: o id e a chave da resposta"
                )
            if identificador in vistos:
                raise TaxonomiaInvalida(
                    f"id {identificador!r} repetido na taxonomia: no cruzamento as "
                    "duas dividiriam o mesmo balde de resposta"
                )
            if identificador in do_catalogo:
                raise TaxonomiaInvalida(
                    f"id {identificador!r} de {intencao.value} ja existe no catalogo "
                    "de plataforma/contexto: o cruzamento indexa por id, e uma das "
                    "duas sumiria do conjunto sem erro nenhum"
                )
            vistos.add(identificador)
            if not PESO_MINIMO_VALIDO <= lacuna.peso <= PESO_MAXIMO_VALIDO:
                raise TaxonomiaInvalida(
                    f"peso {lacuna.peso} de {identificador!r} fora de "
                    f"{PESO_MINIMO_VALIDO}..{PESO_MAXIMO_VALIDO}: fora da faixa a "
                    "comparacao com o peso minimo da entrevista perde o significado"
                )
            if not lacuna.pergunta.strip():
                raise TaxonomiaInvalida(f"lacuna {identificador!r} sem pergunta")
            if not lacuna.porque.strip():
                raise TaxonomiaInvalida(
                    f"lacuna {identificador!r} sem motivo declarado: pergunta que nao "
                    "se justifica por escrito nao sobrevive a uma revisao honesta"
                )
            if lacuna.universal:
                raise TaxonomiaInvalida(
                    f"lacuna {identificador!r} marcada universal dentro de "
                    f"{intencao.value}: pergunta que vale para qualquer software "
                    "pertence ao catalogo, e nao atras de uma classificacao que pode "
                    "falhar"
                )

    sem_motor = [i for i in Intencao if i not in MOTOR_POR_INTENCAO]
    if sem_motor:
        raise TaxonomiaInvalida(
            "intencao fora de MOTOR_POR_INTENCAO: "
            + ", ".join(i.value for i in sem_motor)
            + " - sem entrada la, nem 'tem motor' nem 'nao tem motor' fica dito, e a "
            "ausencia de motor e justamente o achado que este mapa registra"
        )
    return mapa
