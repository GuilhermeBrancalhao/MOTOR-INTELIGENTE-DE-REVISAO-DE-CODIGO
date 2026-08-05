"""Testes do terceiro eixo: intenção, e o cruzamento dela com plataforma e contexto.

Convenção da suíte: cada docstring nomeia **a mutação que derrubaria o teste**. O que
se prova aqui não é que o código faz o que o código faz — é que as três propriedades
que justificam o módulo continuam valendo: toda classe declarada pergunta alguma
coisa, pedido conhecido cai na classe certa, e ausência de sinal levanta em vez de
chutar.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

from ferramentas import elicitacao
from ferramentas.elicitacao import (
    CATALOGO,
    LACUNAS_POR_INTENCAO,
    MOTOR_POR_INTENCAO,
    PESO_MAXIMO_VALIDO,
    PESO_MINIMO_VALIDO,
    PONTOS_MINIMOS,
    Contexto,
    Intencao,
    IntencaoDesconhecida,
    IntencaoIndeterminada,
    Lacuna,
    Origem,
    Plataforma,
    TaxonomiaInvalida,
    classificar,
    lacunas_ativas,
    lacunas_da_intencao,
    lacunas_do_pedido,
    sinais_de_intencao,
    validar_taxonomia,
)

RAIZ = Path(elicitacao.__file__).resolve().parents[2]

#: Pedido conhecido e a classe que ele tem de produzir. Um por intenção declarada —
#: e o teste cobra que a tabela cubra todas, para que uma classe nova sem pedido de
#: prova não passe despercebida.
PEDIDOS_CONHECIDOS: tuple[tuple[str, Intencao], ...] = (
    (
        "Quero um sistema novo, do zero, para a recepção da clínica.",
        Intencao.MATERIALIZAR,
    ),
    (
        "Como estruturar isso: monólito ou microserviços? O acoplamento está ruim.",
        Intencao.ARQUITETAR,
    ),
    ("Revisa isso aqui pra mim, tá bom assim?", Intencao.REVISAR),
    ("Está lento demais, dá timeout e a latência subiu.", Intencao.OTIMIZAR),
    ("Desenha um diagrama de como isso se conecta.", Intencao.DIAGRAMAR),
    (
        "Preciso acrescentar ao sistema que já roda uma nova funcionalidade.",
        Intencao.EVOLUIR,
    ),
    (
        "Automatizar a rotina que roda toda noite sem intervenção.",
        Intencao.AUTOMATIZAR,
    ),
    (
        "Integrar com a API do banco e sincronizar com o sistema de terceiro.",
        Intencao.INTEGRAR,
    ),
    (
        "Consolidar as planilhas de Excel num CSV único e limpar os dados.",
        Intencao.TRATAR_DADOS,
    ),
    ("Escrever testes com pytest e medir cobertura.", Intencao.TESTAR),
    (
        "Auditoria de segurança: achei vulnerabilidade e senha exposta.",
        Intencao.PROTEGER,
    ),
    ("Documentar o projeto num README e num guia de uso.", Intencao.DOCUMENTAR),
    (
        "Configurar o deploy e o monitoramento da infraestrutura.",
        Intencao.OPERAR,
    ),
    ("Um agente de IA com prompt e RAG em cima do acervo.", Intencao.CONSTRUIR_IA),
)


# --- (a) toda classe declarada tem conjunto de lacunas não-vazio ---------


def test_toda_intencao_declarada_tem_lacuna():
    """Derrubaria este teste: acrescentar membro na `Intencao` sem escrever as lacunas.

    É o critério que dá sentido ao eixo. Uma classe que classifica e não acrescenta
    pergunta nenhuma deixa a entrevista exatamente como estava — o eixo passa a
    existir na documentação e a não existir na conversa, e ninguém percebe porque
    nada quebra.
    """
    assert len(Intencao) == 14, "5 dos motores + 9 descobertas; mudou, revise o mapa"
    for intencao in Intencao:
        lacunas = lacunas_da_intencao(intencao)
        assert lacunas, f"{intencao.value} não acrescenta pergunta nenhuma"
        assert all(isinstance(lacuna, Lacuna) for lacuna in lacunas)


def test_toda_lacuna_de_intencao_tem_motivo_e_peso_na_faixa():
    """Derrubaria este teste: `porque=""` numa lacuna nova, ou peso 0 / peso 20.

    O motivo declarado é a regra que o próprio catálogo impõe: pergunta que não se
    justifica por escrito não sobrevive a uma revisão honesta, e o motor precisa dele
    para responder "por que isso importa?" sem inventar na hora. Peso fora de 1..10
    quebra a comparação com o `peso_minimo` da entrevista sem sinal nenhum.
    """
    for intencao, lacunas in LACUNAS_POR_INTENCAO.items():
        for lacuna in lacunas:
            rotulo = f"{intencao.value}/{lacuna.id}"
            assert lacuna.pergunta.strip(), f"{rotulo} sem pergunta"
            assert lacuna.porque.strip(), f"{rotulo} sem motivo declarado"
            assert PESO_MINIMO_VALIDO <= lacuna.peso <= PESO_MAXIMO_VALIDO, rotulo
            assert not lacuna.universal, (
                f"{rotulo} marcada universal: pergunta que vale para qualquer "
                "software pertence ao catálogo, não atrás de uma classificação"
            )


def test_nenhum_id_de_intencao_colide_com_o_catalogo():
    """Derrubaria este teste: batizar uma lacuna nova de `problema` ou `auto_disparo`.

    O cruzamento junta os dois eixos num conjunto indexado por id. Id repetido não dá
    erro: faz uma das duas lacunas sumir do conjunto — e a que some é a de intenção,
    justamente a que este módulo existe para acrescentar.
    """
    do_catalogo = {lacuna.id for lacuna in CATALOGO}
    vistos: set[str] = set()
    for lacunas in LACUNAS_POR_INTENCAO.values():
        for lacuna in lacunas:
            assert lacuna.id not in do_catalogo, f"{lacuna.id} já existe no catálogo"
            assert lacuna.id not in vistos, f"{lacuna.id} repetido na taxonomia"
            vistos.add(lacuna.id)


# --- (b) pedido conhecido devolve a classe esperada ----------------------


def test_pedido_conhecido_cai_na_classe_esperada():
    """Derrubaria este teste: mexer nos termos de uma intenção sem olhar as vizinhas.

    A tabela de termos é o único lugar onde as quatorze classes competem entre si, e
    o efeito de acrescentar um termo genérico numa delas aparece nas outras — como
    empate, que levanta. Estes catorze pedidos são o piso: se um deles parar de
    classificar, ou passar a classificar como outra coisa, a tabela regrediu.
    """
    for pedido, esperada in PEDIDOS_CONHECIDOS:
        assert classificar(pedido) is esperada, f"{pedido!r} deixou de ser {esperada}"


def test_a_tabela_de_prova_cobre_todas_as_intencoes():
    """Derrubaria este teste: criar classe nova e não escrever pedido de prova para ela.

    Sem isto, o teste anterior passa por vacuidade sobre a classe nova: ela existe,
    tem lacunas, e nenhum pedido jamais provou que `classificar` chega nela. Classe
    inalcançável é o defeito mais silencioso deste módulo.
    """
    cobertas = {esperada for _, esperada in PEDIDOS_CONHECIDOS}
    assert cobertas == set(Intencao)


def test_classificar_ignora_acento_e_caixa():
    """Derrubaria este teste: casar o termo contra o texto cru em vez do dobrado.

    O mecanismo é o de `deteccao.py` — normaliza com `unicodedata` e compara em
    minúsculas — e a razão é que ninguém escreve pedido com acentuação uniforme. As
    duas formas abaixo são o mesmo pedido para qualquer pessoa; se deixarem de ser o
    mesmo para o classificador, metade dos pedidos reais some da tabela.
    """
    assert classificar("AUTOMAÇÃO da rotina") is Intencao.AUTOMATIZAR
    assert classificar("automacao da rotina") is Intencao.AUTOMATIZAR


def test_sinal_de_intencao_traz_trecho_do_texto_original():
    """Derrubaria este teste: devolver o texto dobrado, ou o nome do termo, como evidência.

    Mesma exigência de `deteccao.Palpite`: quem recebe a classificação pode perguntar
    "por que você achou isso?" e tem de receber de volta um pedaço do que escreveu —
    com acento e caixa como escreveu. Termo da tabela não serve de resposta: ele
    prova o que a tabela contém, não o que a pessoa disse.
    """
    pedido = "Preciso automatizar a conciliação que hoje é feita na mão."
    sinais = sinais_de_intencao(pedido)
    assert sinais, "esperava ao menos um sinal"
    for palpite in sinais:
        assert palpite.origem is Origem.INFERIDO
        assert palpite.evidencia in pedido, f"{palpite.evidencia!r} não é do texto"
    assert str(Intencao.AUTOMATIZAR) in {palpite.valor for palpite in sinais}


# --- (c) classe fora do catálogo levanta exceção nomeada -----------------


def test_intencao_fora_do_catalogo_levanta():
    """Derrubaria este teste: `lacunas_da_intencao` devolver `()` para valor desconhecido.

    Conjunto vazio é a pior saída possível: a entrevista segue sem nenhuma pergunta
    deste eixo e a especificação sai parecendo completa. Erro de digitação em id de
    intenção — que atravessa arquivo de estado e linha de comando como texto — tem de
    parar aqui, com o nome da classe que não existe.
    """
    for valor in ("CONSERTAR_TUDO", "materializar_ideia", "", "   ", "OTIMIZA"):
        try:
            lacunas_da_intencao(valor)
        except IntencaoDesconhecida:
            continue
        raise AssertionError(f"{valor!r} deveria ter levantado IntencaoDesconhecida")


def test_intencao_conhecida_aceita_texto_equivalente():
    """Derrubaria este teste: a recusa acima passar a recusar também o que é válido.

    Uma validação que reprova tudo passa no teste anterior e destrói a fronteira do
    módulo. `"OTIMIZAR"` em texto é a mesma coisa que `Intencao.OTIMIZAR`, porque o
    valor do `StrEnum` é o texto — e é assim que a classe volta de um arquivo de
    estado.

    A tolerância a caixa e a espaço em volta é a mesma de
    `entrevista._como_plataforma_ou_contexto`, de propósito: duas fronteiras do mesmo
    pacote aceitando texto com regras diferentes é defeito esperando acontecer, e
    quem escrever `"otimizar\\n"` lido de um arquivo não tem como adivinhar qual das
    duas é a rígida.
    """
    esperado = lacunas_da_intencao(Intencao.OTIMIZAR)
    for forma in ("OTIMIZAR", "otimizar", "  OTIMIZAR  ", "Otimizar\n"):
        assert lacunas_da_intencao(forma) == esperado, f"{forma!r} deveria ser aceito"


def test_pedido_ambiguo_levanta_em_vez_de_chutar():
    """Derrubaria este teste: desempatar pela ordem de declaração da enumeração.

    É a regra R1 aplicada onde ela custa mais caro. "Revisar e otimizar" são dois
    trabalhos com conjuntos de perguntas diferentes; escolher um por ordem de tabela
    não produz uma pergunta ruim, produz uma entrevista inteira sobre o trabalho
    errado — e a pessoa responde tudo antes de alguém notar. A exceção carrega as
    candidatas justamente para que dê para perguntar.
    """
    try:
        classificar("Preciso revisar e otimizar isso.")
    except IntencaoIndeterminada as erro:
        assert set(erro.candidatas) == {Intencao.REVISAR, Intencao.OTIMIZAR}
    else:
        raise AssertionError("empate deveria ter levantado IntencaoIndeterminada")


def test_pedido_sem_sinal_levanta_sem_candidata():
    """Derrubaria este teste: adotar uma intenção padrão quando o texto não diz nada.

    Ausência de sinal e empate são situações diferentes e a exceção distingue as
    duas: sem candidata, a pergunta ao usuário é aberta ("que tipo de trabalho é
    este?"); com candidatas, é de desempate. Colapsar as duas num `MATERIALIZAR`
    padrão é o `PADRAO_ASSUMIDO` circulando como decisão.
    """
    for pedido in ("", "   ", "faz aí pra mim", "bom dia, tudo bem?"):
        try:
            classificar(pedido)
        except IntencaoIndeterminada as erro:
            assert erro.candidatas == ()
        else:
            raise AssertionError(f"{pedido!r} não deveria classificar")


def test_sinal_fraco_sozinho_nao_decide():
    """Derrubaria este teste: baixar `PONTOS_MINIMOS` para 1.

    "Rotina" sozinha aparece em pedido de automação, de teste e de documentação. Um
    único termo de confiança BAIXA decidindo a classe é o chute com aparência de
    método — e é pior que o chute honesto, porque vem com uma evidência que parece
    justificar. Com um termo de confiança média junto, aí sim decide.
    """
    assert PONTOS_MINIMOS >= 2
    try:
        classificar("uma rotina qualquer")
    except IntencaoIndeterminada as erro:
        assert erro.candidatas == (Intencao.AUTOMATIZAR,)
    else:
        raise AssertionError("sinal fraco isolado não pode decidir")

    assert classificar("uma rotina que roda toda noite") is Intencao.AUTOMATIZAR


# --- `validar_taxonomia` reprova de verdade ------------------------------


def test_validar_taxonomia_aprova_o_mapa_real():
    """Derrubaria este teste: qualquer defeito de conteúdo no mapa declarado acima.

    O validador rodando sobre o dado real é o que distingue "as regras existem" de
    "as regras valem aqui dentro". Ele devolve o próprio mapa para que o chamador
    fique com a garantia junto do dado, como faz `validar_catalogo`.
    """
    assert validar_taxonomia() is LACUNAS_POR_INTENCAO


def test_classe_nova_sem_lacuna_quebra_a_validacao():
    """Derrubaria este teste: o validador só olhar as chaves que o mapa já tem.

    A ausência que importa é a de uma classe declarada na enumeração e esquecida no
    mapa — que é exatamente o que acontece quando alguém acrescenta um membro e para
    por aí. Varrer só o mapa passaria por vacuidade nesse caso, que é o único em que
    o defeito ocorre de verdade.
    """
    sem_uma = {i: LACUNAS_POR_INTENCAO[i] for i in Intencao if i is not Intencao.TESTAR}
    try:
        validar_taxonomia(sem_uma)
    except TaxonomiaInvalida as erro:
        assert "TESTAR" in str(erro)
    else:
        raise AssertionError("intenção fora do mapa deveria reprovar")

    vazia = dict(LACUNAS_POR_INTENCAO)
    vazia[Intencao.TESTAR] = ()
    try:
        validar_taxonomia(vazia)
    except TaxonomiaInvalida as erro:
        assert "TESTAR" in str(erro)
    else:
        raise AssertionError("intenção com tupla vazia deveria reprovar")


def test_lacuna_sem_motivo_ou_com_peso_fora_da_faixa_quebra_a_validacao():
    """Derrubaria este teste: o validador copiar só a checagem de id do catálogo.

    Motivo em branco e peso fora de 1..10 são os dois defeitos que passam despercebidos
    numa revisão de leitura — o texto está lá, a estrutura está certa, e o que falta é
    conteúdo. São também os dois que o `validar_catalogo` cobre, e perder um deles na
    versão nova do eixo seria regressão silenciosa.
    """
    base = dict(LACUNAS_POR_INTENCAO)

    sem_motivo = dict(base)
    sem_motivo[Intencao.TESTAR] = (
        Lacuna(
            id="teste_sem_motivo",
            pergunta="Pergunta que ninguém consegue justificar?",
            porque="   ",
            peso=5,
            universal=False,
        ),
    )
    try:
        validar_taxonomia(sem_motivo)
    except TaxonomiaInvalida as erro:
        assert "teste_sem_motivo" in str(erro)
    else:
        raise AssertionError("lacuna sem motivo deveria reprovar")

    peso_absurdo = dict(base)
    peso_absurdo[Intencao.TESTAR] = (
        Lacuna(
            id="teste_peso_absurdo",
            pergunta="Pergunta com peso fora da escala?",
            porque="Existe só para provar que a faixa de peso é verificada.",
            peso=PESO_MAXIMO_VALIDO + 1,
            universal=False,
        ),
    )
    try:
        validar_taxonomia(peso_absurdo)
    except TaxonomiaInvalida as erro:
        assert "teste_peso_absurdo" in str(erro)
    else:
        raise AssertionError("peso fora da faixa deveria reprovar")


def test_id_colidindo_com_o_catalogo_quebra_a_validacao():
    """Derrubaria este teste: validar a taxonomia isolada, sem olhar o catálogo.

    Este é o defeito que só existe porque há dois eixos: cada mapa está correto
    sozinho, e o cruzamento perde uma lacuna. Validação que não conhece o outro lado
    nunca o pegaria.
    """
    colidindo = dict(LACUNAS_POR_INTENCAO)
    colidindo[Intencao.TESTAR] = (
        Lacuna(
            id="problema",
            pergunta="Pergunta com id que já é do catálogo?",
            porque="Existe só para provar que a colisão entre os eixos é vista.",
            peso=5,
            universal=False,
        ),
    )
    try:
        validar_taxonomia(colidindo)
    except TaxonomiaInvalida as erro:
        assert "problema" in str(erro)
    else:
        raise AssertionError("id colidindo com o catálogo deveria reprovar")


# --- O cruzamento dos três eixos -----------------------------------------


def test_cruzamento_soma_os_tres_eixos():
    """Derrubaria este teste: `lacunas_do_pedido` devolver só um dos eixos.

    Um pedido de automação que mexe em dado pessoal tem de trazer as três origens ao
    mesmo tempo: as universais e as de `AUTOMACAO` pelo catálogo, as de
    `DADO_PESSOAL` pelo contexto, e as de `AUTOMATIZAR` pela intenção. Se qualquer
    uma das três sumir, o conjunto abaixo encolhe — e o que se perde é a pergunta que
    ninguém mais faz.
    """
    pedido = "Automatizar a rotina que toda noite exporta o cadastro de clientes com CPF."
    assert classificar(pedido) is Intencao.AUTOMATIZAR

    ids = {
        lacuna.id
        for lacuna in lacunas_do_pedido(
            pedido, [Plataforma.AUTOMACAO], [Contexto.DADO_PESSOAL]
        )
    }
    assert "problema" in ids, "perdeu as universais do catálogo"
    assert "auto_disparo" in ids, "perdeu as lacunas de Plataforma.AUTOMACAO"
    assert "pessoal_base_legal" in ids, "perdeu as lacunas de Contexto.DADO_PESSOAL"
    assert "auto_processo_manual_hoje" in ids, "perdeu as lacunas da intenção"

    do_catalogo = {lacuna.id for lacuna in lacunas_ativas([Plataforma.AUTOMACAO], [Contexto.DADO_PESSOAL])}
    da_intencao = {lacuna.id for lacuna in lacunas_da_intencao(Intencao.AUTOMATIZAR)}
    assert ids == do_catalogo | da_intencao
    assert do_catalogo < ids, "o eixo de intenção tem de acrescentar, não substituir"


def test_intencao_muda_o_conjunto_com_a_mesma_plataforma_e_contexto():
    """Derrubaria este teste: ignorar a intenção e devolver sempre `lacunas_ativas`.

    É a prova de que o eixo novo é ortogonal aos dois antigos, e é o buraco que o
    ciclo fecha: com plataforma e contexto idênticos, criar do zero e otimizar o que
    já roda recebiam as mesmas trinta e sete perguntas. Se os dois conjuntos abaixo
    voltarem a ser iguais, o módulo virou enfeite.
    """
    eixos = ([Plataforma.WEB], [Contexto.MULTIUSUARIO])
    criar = {
        lacuna.id
        for lacuna in lacunas_do_pedido("", *eixos, intencao=Intencao.MATERIALIZAR)
    }
    otimizar = {
        lacuna.id for lacuna in lacunas_do_pedido("", *eixos, intencao=Intencao.OTIMIZAR)
    }
    comum = {lacuna.id for lacuna in lacunas_ativas(*eixos)}

    assert criar != otimizar
    assert criar & otimizar == comum, "só o catálogo pode ser compartilhado"
    assert "perf_medicao_atual" in otimizar and "perf_medicao_atual" not in criar
    assert "mat_stack_imposta" in criar and "mat_stack_imposta" not in otimizar


def test_cruzamento_de_pedido_indeterminado_nao_inventa_conjunto():
    """Derrubaria este teste: cair nas universais quando `classificar` não decide.

    Devolver as universais parece inofensivo e é o defeito inteiro: a entrevista roda
    até o fim, a especificação sai, e nada registra que ninguém sabia que trabalho
    estava sendo pedido. A indeterminação tem de subir para quem consegue perguntar.
    """
    try:
        lacunas_do_pedido("bom dia", [Plataforma.WEB], [])
    except IntencaoIndeterminada:
        pass
    else:
        raise AssertionError("pedido sem sinal não pode produzir conjunto de lacunas")

    # Com a classe já decidida por fora — depois da pergunta de desempate — o mesmo
    # texto passa, e é assim que o chamador sai do impasse.
    assert lacunas_do_pedido("bom dia", [Plataforma.WEB], [], intencao=Intencao.REVISAR)


def test_ordem_do_cruzamento_e_estavel():
    """Derrubaria este teste: montar o conjunto com `set` em vez de dicionário ordenado.

    A ordem é a do catálogo primeiro e a da intenção depois, sempre igual para a
    mesma entrada. Ordem instável não quebra teste nenhum de conteúdo e estraga tudo
    o que se apoia nela: a entrevista, a especificação escrita e qualquer comparação
    de duas execuções.
    """
    argumentos = ("Está lento, dá timeout.", [Plataforma.WEB], [])
    primeira = [lacuna.id for lacuna in lacunas_do_pedido(*argumentos)]
    assert primeira == [lacuna.id for lacuna in lacunas_do_pedido(*argumentos)]
    assert primeira[: len(lacunas_ativas([Plataforma.WEB], []))] == [
        lacuna.id for lacuna in lacunas_ativas([Plataforma.WEB], [])
    ]
    assert primeira[-1] == lacunas_da_intencao(Intencao.OTIMIZAR)[-1].id


# --- O achado do ciclo, em dado -----------------------------------------


def test_as_cinco_intencoes_com_motor_apontam_para_motor_que_existe():
    """Derrubaria este teste: renomear pasta em `motores/` sem atualizar o mapa.

    O mapa afirma que cinco classes têm motor, e a afirmação é verificável contra o
    disco. Sem esta checagem, o nome apontado envelhece em silêncio e um despachante
    tentaria invocar uma skill que não existe mais.
    """
    apontados = {nome for nome in MOTOR_POR_INTENCAO.values() if nome}
    assert len(apontados) == 5
    for nome in apontados:
        assert (RAIZ / "motores" / nome / "SKILL.md").is_file(), (
            f"MOTOR_POR_INTENCAO aponta para motores/{nome}, que não existe"
        )


def test_nove_intencoes_declaram_que_nao_tem_motor():
    """Derrubaria este teste: apontar as nove descobertas para o motor menos errado.

    O `None` é o achado do ciclo, e ele vale por ser explícito: um despachante que lê
    este mapa diz "não há motor para isto" em vez de encaminhar automação para
    `materializar-ideia` porque era o mais parecido. Preencher os nove sem escrever
    os motores apagaria a única evidência de que eles faltam.
    """
    sem_motor = {i for i, nome in MOTOR_POR_INTENCAO.items() if nome is None}
    assert len(sem_motor) == 9
    assert Intencao.EVOLUIR in sem_motor
    assert Intencao.MATERIALIZAR not in sem_motor
    assert set(MOTOR_POR_INTENCAO) == set(Intencao)


# --- A trava de dependência, estendida ao módulo novo --------------------


def test_taxonomia_so_importa_biblioteca_padrao():
    """Derrubaria este teste: trazer uma biblioteca de fora para classificar texto.

    A tentação aqui é maior que nos outros módulos do pacote — classificação de texto
    é o lugar onde alguém sugere um modelo pronto — e a regra é a mesma: o plugin se
    instala em projeto alheio e não arrasta dependência. A varredura é por `ast`,
    sobre o código-fonte, para pegar também import dentro de função.
    """
    arquivo = Path(elicitacao.__file__).resolve().parent / "taxonomia.py"
    arvore = ast.parse(arquivo.read_text(encoding="utf-8"), filename=str(arquivo))
    externos: list[str] = []
    internos = 0
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            nomes = [alias.name.split(".")[0] for alias in no.names]
        elif isinstance(no, ast.ImportFrom):
            if no.level:
                internos += 1
                continue
            nomes = [(no.module or "").split(".")[0]]
        else:
            continue
        externos.extend(n for n in nomes if n and n not in sys.stdlib_module_names)

    assert internos >= 2, "esperava os imports relativos de catalogo e deteccao"
    assert not externos, f"taxonomia.py só pode importar stdlib; encontrei {externos}"
