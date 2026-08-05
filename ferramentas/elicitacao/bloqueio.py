"""A regra de bloqueio: qual lacuna **impede** planejar, e qual apenas fica aberta.

Este é o critério central do motor de elicitação, e ele existe porque as duas saídas
fáceis são péssimas. Bloquear em tudo devolve o interrogatório de quarenta itens que
`entrevista.py` existe para evitar; não bloquear em nada devolve o plano escrito sobre
suposição, que é o defeito que a elicitação inteira foi construída para não ter.

A regra
-------
Uma lacuna é **BLOQUEANTE** se, e só se, existem duas respostas admissíveis r₁ ≠ r₂
tais que ao menos um destes três predicados difere entre elas:

- **B1 — muda o conjunto de lacunas ativas**: `lacunas_ativas(r₁) ≠ lacunas_ativas(r₂)`.
  Responder abre ou fecha outras perguntas, então perguntar depois é perguntar tarde:
  a entrevista já terá seguido por um ramo que talvez não exista.
- **B2 — a lacuna é `universal=True`**: não existe caso em que ela seja dispensável.
  É a mesma assimetria que `especificacao.completa` já aplica, aqui em forma de porta.
- **B3 — impede escrever o critério de aceite**: sem a resposta não dá para redigir um
  critério falsificável de nenhum ciclo do plano.

Todo o resto é **ASSUMÍVEL**. E assumível **não significa preenchido**: a lacuna
assumível sai como *decisão aberta com a pergunta inteira*, exatamente como
`entrevista.decisoes_abertas` já as devolve, e nunca como valor chutado.
`Origem.PADRAO_ASSUMIDO` está nomeado em `deteccao.py` justamente para poder ser
proibido de circular como decisão — e aqui ele é proibido por escrito, em
`PadraoAssumidoProibido`.

Dois critérios que esta regra PROÍBE
------------------------------------
**1. Confiança do modelo não é critério.** No caso medido pelo acervo, a inferência de
confiança BAIXA era a certa e as de ALTA/MÉDIA erraram. Confiança é resultado, não
critério: ela ordena a conversa de confirmação (`deteccao.Palpite.confianca`) e não
decide o que trava o plano. Nenhuma das três funções de predicado deste módulo recebe
`Palpite`, e nenhuma lê `confianca` — a ausência é o desenho, e há teste sobre o
código-fonte cobrando essa ausência.

**2. Peso alto ≠ bloqueante.** `peso` governa a ORDEM da entrevista e o limiar de
parada (`entrevista.peso_minimo`), não o bloqueio. Confundir os dois transforma o gate
em "pergunte tudo acima de 7", que é o interrogatório de novo, agora com número. Há
lacuna de peso 10 assumível (`evo_comportamento_preservado` fora de um pedido de
evolução) e lacuna de peso 7 bloqueante (`fora_de_escopo`, universal) — e é assim que
tem de ser.

Por que três funções separadas
------------------------------
`_b1_muda_lacunas_ativas`, `_b2_universal` e `_b3_impede_aceite` são funções separadas
e testáveis isoladamente porque o aceite deste ciclo exige mutar **uma de cada vez** e
ver cair um teste que nomeia aquela mutação. Um predicado único com três `or` embutidos
passaria no aceite por acidente: mutar qualquer ramo derrubaria os mesmos testes, e
ninguém saberia qual dos três está de fato sustentando o gate.

O que este módulo deliberadamente NÃO faz: não persiste nada (isso é
`ferramentas/descoberta.py`, que fica fora do pacote porque este aqui só pode importar
biblioteca padrão), não pergunta, não infere e não decide fase nenhuma. Ele recebe as
lacunas abertas e devolve o veredito de cada uma, com os predicados que dispararam.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum

from .catalogo import CATALOGO, Contexto, Lacuna, Plataforma, lacunas_ativas
from .entrevista import PalpiteDesconhecido, _como_plataforma_ou_contexto
from .taxonomia import LACUNAS_POR_INTENCAO, Intencao, lacunas_da_intencao


class Predicado(StrEnum):
    """Qual dos três predicados fez a lacuna bloquear.

    Viaja junto do veredito, e não ao lado, pelo mesmo motivo que `Origem` viaja junto
    da resposta: o gate que recusa uma transição precisa dizer **por que** aquela
    pergunta trava o plano, e "porque sim" não sobrevive a uma pessoa com pressa.
    """

    B1_MUDA_LACUNAS = "B1_MUDA_LACUNAS"
    B2_UNIVERSAL = "B2_UNIVERSAL"
    B3_IMPEDE_ACEITE = "B3_IMPEDE_ACEITE"


#: A frase que explica cada predicado a quem leu "bloqueado" na tela. É conteúdo
#: revisado, como o `porque` do catálogo: texto montado na hora seria plausível e não
#: seria revisável.
MOTIVO_DO_PREDICADO: Mapping[Predicado, str] = {
    Predicado.B1_MUDA_LACUNAS: (
        "responder muda quais outras perguntas existem: seguir sem a resposta é "
        "escolher um ramo da entrevista no escuro"
    ),
    Predicado.B2_UNIVERSAL: (
        "vale para qualquer software, sem gatilho: não existe caso em que ela seja "
        "dispensável"
    ),
    Predicado.B3_IMPEDE_ACEITE: (
        "sem esta resposta não se redige critério de aceite falsificável para nenhum "
        "ciclo do plano"
    ),
}


class ParteDoAceite(StrEnum):
    """Qual pedaço de um critério falsificável a resposta fornece.

    Um critério de aceite falsificável tem forma fixa: *alguém observa **o quê**, e
    compara com **qual número ou condição**, por **qual procedimento**, contra **qual
    estado anterior** quando a promessa é de melhora*. Faltando um desses pedaços, o
    que se escreve não é critério — é intenção, e intenção não reprova ninguém.

    A enumeração existe para que B3 seja verificável em vez de opinativo. Sem ela, "sem
    esta resposta não dá para escrever o aceite" seria julgamento caso a caso, que é
    outro nome para confiança do modelo — o critério que este módulo proíbe.
    """

    SUJEITO = "SUJEITO"
    LIMIAR = "LIMIAR"
    LINHA_DE_BASE = "LINHA_DE_BASE"
    PROCEDIMENTO = "PROCEDIMENTO"


#: Que pedaço do critério de aceite cada lacuna fornece. É declaração de conteúdo,
#: revisável como o catálogo, e não caso especial escondido dentro de um `if`: quem
#: discorda de uma linha discute a linha.
#:
#: `validar_bloqueio` reprova id que não existe em nenhum dos dois eixos — sem isso, um
#: id digitado errado aqui viraria uma lacuna que **deixa** de bloquear, em silêncio, e
#: o efeito só apareceria como plano escrito sem aceite.
PARTES_DO_ACEITE: Mapping[str, ParteDoAceite] = {
    # --- SUJEITO: o que se observa quando alguém for verificar.
    # Sem o problema declarado não há o que observar: qualquer saída "resolve" um
    # problema que ninguém escreveu.
    "problema": ParteDoAceite.SUJEITO,
    # "O que a pessoa consegue fazer no dia seguinte" é literalmente o sujeito da
    # frase do aceite.
    "capacidade_nova": ParteDoAceite.SUJEITO,
    # Revisão sem recorte não tem o que declarar revisado.
    "rev_alvo": ParteDoAceite.SUJEITO,
    # Em evolução, o aceite principal é de não-regressão, e o sujeito dele é o que
    # tem de continuar igual.
    "evo_comportamento_preservado": ParteDoAceite.SUJEITO,
    # Teste vale pelo que protege; sem o que protege, "cobertura" não é critério.
    "teste_o_que_nao_pode_quebrar": ParteDoAceite.SUJEITO,
    # Segurança sem ativo nomeado só produz lista de boas práticas, que ninguém
    # consegue reprovar.
    "seg_o_que_protege": ParteDoAceite.SUJEITO,
    # O aceite de um diagrama é a pergunta que o leitor passa a conseguir responder.
    "dia_pergunta_do_leitor": ParteDoAceite.SUJEITO,
    # --- LIMIAR: o número ou a condição que separa passou de não passou.
    "sucesso": ParteDoAceite.LIMIAR,
    "perf_meta": ParteDoAceite.LIMIAR,
    # O total que tem de fechar é o limiar de uma transformação de dados.
    "dado_regra_de_fechamento": ParteDoAceite.LIMIAR,
    "ops_indisponibilidade_aceitavel": ParteDoAceite.LIMIAR,
    # --- LINHA_DE_BASE: o estado anterior, sem o qual "melhorou" não se afirma.
    "perf_medicao_atual": ParteDoAceite.LINHA_DE_BASE,
    # A automação se aceita contra o processo manual que ela substitui; sem ele
    # descrito, não há com o que comparar a saída.
    "auto_processo_manual_hoje": ParteDoAceite.LINHA_DE_BASE,
    # --- PROCEDIMENTO: como a verificação é feita, e por quem.
    # "Como se sabe que a resposta do modelo está certa, e quem julga" é o
    # procedimento inteiro; sem ele, avaliar sistema de IA é troca de impressão.
    "ia_criterio_de_acerto": ParteDoAceite.PROCEDIMENTO,
}


class BloqueioInvalido(ValueError):
    """`PARTES_DO_ACEITE` aponta para lacuna que não existe, ou parte sem nenhuma fonte.

    Levanta pelo mesmo motivo que `CatalogoInvalido` e `TaxonomiaInvalida`: é erro de
    programa com consequência silenciosa. Id inexistente aqui não dá erro em execução —
    faz B3 nunca disparar por aquela linha, e o efeito é um plano que passa no gate sem
    ter aceite possível. Parte declarada sem nenhuma lacuna que a forneça é o mesmo
    defeito pelo outro lado: a enumeração cresce e o critério não muda.
    """


class PadraoAssumidoProibido(ValueError):
    """Alguém tentou gravar uma lacuna aberta como se tivesse sido respondida.

    `Origem.PADRAO_ASSUMIDO` existe nomeado em `deteccao.py` exatamente para poder ser
    proibido de circular como decisão, e este é o lugar onde a proibição vira código.
    Assumível quer dizer "o motor segue sem perguntar"; não quer dizer "o motor decide
    no lugar de alguém e não conta". A diferença entre as duas é a única coisa que
    separa uma especificação honesta de um documento que parece completo.
    """


@dataclass(frozen=True, slots=True)
class DecisaoAberta:
    """Uma lacuna sem resposta, com o veredito da regra de bloqueio.

    **Não existe campo de valor aqui, e a ausência é o desenho.** Uma decisão aberta
    não tem valor — nem `None`, nem `""`, nem "a definir": um campo vazio é preenchido
    por alguém em algum momento, e a partir daí a suposição viaja com a mesma
    autoridade de uma resposta. O que ela carrega é a pergunta inteira e o motivo dela,
    que é o que alguém precisa para decidir de olho aberto.

    Congelada porque é retrato: responder a lacuna produz outra avaliação, e ter as
    duas permite comparar.
    """

    id: str
    pergunta: str
    porque: str
    peso: int
    universal: bool
    predicados: tuple[Predicado, ...]

    @property
    def bloqueante(self) -> bool:
        """Bloqueia se ao menos um predicado disparou. Vazio é assumível.

        A disjunção é a regra escrita: basta um dos três diferir entre duas respostas
        admissíveis. Exigir dois seria pedir que a lacuna prove duas vezes o mesmo
        ponto, e o custo do falso negativo aqui é um plano inteiro.
        """
        return bool(self.predicados)

    @property
    def motivos(self) -> tuple[str, ...]:
        """A explicação de cada predicado que disparou, na ordem B1, B2, B3."""
        return tuple(MOTIVO_DO_PREDICADO[predicado] for predicado in self.predicados)

    def como_dicionario(self) -> dict:
        """Forma serializável, para o estado e para a mensagem do gate.

        Sem chave de valor, pela mesma razão da classe: um `"valor": null` no
        `estado.json` é um convite para alguém preencher à mão e seguir.
        """
        return {
            "id": self.id,
            "pergunta": self.pergunta,
            "porque": self.porque,
            "peso": self.peso,
            "universal": self.universal,
            "bloqueante": self.bloqueante,
            "predicados": [str(predicado) for predicado in self.predicados],
        }


def aplicar_resposta(
    valor: str,
    plataformas: Iterable[Plataforma] = (),
    contextos: Iterable[Contexto] = (),
) -> tuple[frozenset[Plataforma], frozenset[Contexto]]:
    """Os conjuntos como ficariam se esta resposta fosse dada.

    É a mesma regra genérica de `entrevista.responder`, e de propósito: se o efeito de
    responder fosse calculado aqui por uma regra própria, B1 passaria a prever um
    comportamento que a entrevista não tem. Resposta que não nomeia plataforma nem
    contexto não muda nada — e não mudar nada é informação, não erro.

    Pública porque a persistência (`ferramentas/descoberta.py`) precisa exatamente
    desta regra ao gravar uma resposta. Duas cópias dela — uma que prevê e outra que
    aplica — divergiriam no primeiro ajuste, e a divergência apareceria como gate que
    trava depois de a pessoa já ter respondido.
    """
    plataformas = frozenset(plataformas)
    contextos = frozenset(contextos)
    try:
        alvo = _como_plataforma_ou_contexto(valor)
    except PalpiteDesconhecido:
        return plataformas, contextos
    if isinstance(alvo, Plataforma):
        return plataformas | {alvo}, contextos
    return plataformas, contextos | {alvo}


def _b1_muda_lacunas_ativas(
    lacuna: Lacuna,
    *,
    plataformas: Iterable[Plataforma] = (),
    contextos: Iterable[Contexto] = (),
    universo: Iterable[Lacuna] = CATALOGO,
) -> bool:
    """Duas respostas admissíveis produzem conjuntos de lacunas ativas diferentes?

    O conjunto de respostas admissíveis é `lacuna.opcoes`. Não é um recorte por
    preguiça: é o único conjunto **declarado** que existe. Para pergunta de resposta
    livre, "todas as respostas possíveis" é o conjunto de todas as frases da língua, e
    aí o predicado ou vira "sempre verdadeiro" (bloqueia tudo, e o gate morre de
    ruído) ou vira palpite sobre o que a pessoa poderia escrever — que é confiança do
    modelo com outro nome.

    Isso deixa B1 estreito de propósito, e é aceitável porque nada some: uma pergunta
    de resposta livre que muda o rumo da entrevista está declarando gatilho pela
    estrutura errada, e o lugar de corrigir isso é o catálogo — dando `opcoes` a ela —,
    não uma heurística aqui dentro.

    `universo` é o conjunto onde a mudança é medida, e ele tem de ser o conjunto
    **completo** — inclusive as lacunas que ainda não estão ativas. Medir a mudança
    sobre as lacunas ativas de agora zeraria o predicado justamente no caso que ele
    existe para pegar: sem plataforma nenhuma confirmada, o bloco `WEB` ainda não
    entrou, e responder `onde_roda` "não mudaria nada" porque não há nada para mudar.
    `universo_completo` monta esse conjunto para os três eixos.
    """
    p = frozenset(plataformas)
    c = frozenset(contextos)
    catalogo = tuple(universo)

    efeitos: set[frozenset[str]] = set()
    for resposta in lacuna.opcoes:
        depois_p, depois_c = aplicar_resposta(resposta, p, c)
        efeitos.add(
            frozenset(
                ativa.id for ativa in lacunas_ativas(depois_p, depois_c, catalogo=catalogo)
            )
        )
        if len(efeitos) > 1:
            return True
    return False


def _b2_universal(lacuna: Lacuna) -> bool:
    """A lacuna vale para qualquer software, sem gatilho?

    O predicado mais simples dos três, e o que mais se tenta afrouxar no dia do prazo.
    Ele é o mesmo critério que `especificacao.completa` já aplica — especificação com
    lacuna universal aberta não se declara completa —, e mantê-los idênticos evita a
    incoerência de um plano bloqueado por uma especificação que se diz pronta, ou o
    contrário.

    Não lê `peso`. Universal de peso 7 (`fora_de_escopo`) bloqueia; condicional de peso
    10 (`perf_medicao_atual` fora de um pedido de otimização) não bloqueia por aqui.
    """
    return bool(lacuna.universal)


def _b3_impede_aceite(lacuna: Lacuna, *, respondidas: Iterable[str] = ()) -> bool:
    """Sem esta resposta, falta um pedaço do critério de aceite que ninguém mais dá?

    Duas condições, e a segunda é o que impede o predicado de virar uma lista fixa de
    perguntas obrigatórias:

    1. A lacuna fornece um pedaço do critério (`PARTES_DO_ACEITE`).
    2. **Nenhuma lacuna já respondida fornece o mesmo pedaço.** Se o número que separa
       passou de não passou já veio de `sucesso`, o de `perf_meta` deixa de ser o que
       impede escrever o aceite — continua valendo a pena perguntar, e é isso que a
       decisão aberta registra, mas não trava mais o plano.

    A segunda condição é o que torna B3 dinâmico: responder muda o veredito das outras,
    que é exatamente o comportamento que o C4 precisa para destravar a transição depois
    da entrevista, sem que ninguém tenha de reclassificar nada na mão.
    """
    parte = PARTES_DO_ACEITE.get(lacuna.id)
    if parte is None:
        return False
    ja_respondidas = set(respondidas)
    coberta_por_outra = any(
        outro_id in ja_respondidas and outra_parte is parte
        for outro_id, outra_parte in PARTES_DO_ACEITE.items()
        if outro_id != lacuna.id
    )
    return not coberta_por_outra


def avaliar_lacuna(
    lacuna: Lacuna,
    *,
    plataformas: Iterable[Plataforma] = (),
    contextos: Iterable[Contexto] = (),
    respondidas: Iterable[str] = (),
    universo: Iterable[Lacuna] = CATALOGO,
) -> DecisaoAberta:
    """O veredito de uma lacuna: os predicados que dispararam, ou nenhum.

    Devolve `DecisaoAberta` tanto para bloqueante quanto para assumível, e o mesmo tipo
    para os dois casos é intencional: assumível **é** decisão aberta, com a pergunta
    inteira, e não uma lacuna resolvida por padrão. Ter dois tipos diferentes abriria a
    porta para o assumível ganhar um campo de valor um dia.
    """
    predicados: list[Predicado] = []
    if _b1_muda_lacunas_ativas(
        lacuna, plataformas=plataformas, contextos=contextos, universo=universo
    ):
        predicados.append(Predicado.B1_MUDA_LACUNAS)
    if _b2_universal(lacuna):
        predicados.append(Predicado.B2_UNIVERSAL)
    if _b3_impede_aceite(lacuna, respondidas=respondidas):
        predicados.append(Predicado.B3_IMPEDE_ACEITE)

    return DecisaoAberta(
        id=lacuna.id,
        pergunta=lacuna.pergunta,
        porque=lacuna.porque,
        peso=lacuna.peso,
        universal=lacuna.universal,
        predicados=tuple(predicados),
    )


def universo_completo(
    intencao: Intencao | str | None = None, *, catalogo: Iterable[Lacuna] = CATALOGO
) -> tuple[Lacuna, ...]:
    """Todas as lacunas que **podem** existir para este pedido, ativas ou não.

    É o conjunto que B1 precisa para medir mudança, e é diferente do que
    `lacunas_do_pedido` devolve: aquele já filtrou pelo que está ativo agora, e o que
    B1 pergunta é justamente o que passaria a existir. Um conjunto já filtrado faria o
    predicado responder "não muda nada" sobre a única lacuna do catálogo que declara,
    por escrito, mudar quais outras existem.

    Sem intenção, é só o catálogo. Com intenção, o catálogo mais as lacunas dela, sem
    duplicar id — a mesma ordem e a mesma regra de união de `lacunas_do_pedido`.
    """
    reunidas: dict[str, Lacuna] = {lacuna.id: lacuna for lacuna in catalogo}
    if intencao is not None:
        for lacuna in lacunas_da_intencao(intencao):
            reunidas.setdefault(lacuna.id, lacuna)
    return tuple(reunidas.values())


def classificar_lacunas(
    abertas: Iterable[Lacuna],
    *,
    plataformas: Iterable[Plataforma] = (),
    contextos: Iterable[Contexto] = (),
    respondidas: Iterable[str] = (),
    universo: Iterable[Lacuna] = CATALOGO,
) -> tuple[DecisaoAberta, ...]:
    """Todas as lacunas abertas avaliadas, na ordem recebida.

    `universo` é o conjunto completo onde B1 mede a mudança, e **não** é o conjunto de
    abertas: as respondidas saíram das abertas e continuam existindo, e as inativas
    ainda vão existir se alguém responder o que as destrava. O padrão é o catálogo
    inteiro; com eixo de intenção, passe `universo_completo(intencao)`.

    A ordem é a de entrada, e não a de peso, porque quem chama já ordenou pelo critério
    dele (`entrevista.decisoes_abertas` ordena por peso; `lacunas_do_pedido` pela ordem
    dos eixos). Reordenar aqui esconderia a escolha de quem chamou dentro de uma função
    cujo nome promete só classificar.
    """
    referencia = tuple(universo)
    return tuple(
        avaliar_lacuna(
            lacuna,
            plataformas=plataformas,
            contextos=contextos,
            respondidas=respondidas,
            universo=referencia,
        )
        for lacuna in abertas
    )


def bloqueantes_abertas(
    abertas: Iterable[Lacuna],
    *,
    plataformas: Iterable[Plataforma] = (),
    contextos: Iterable[Contexto] = (),
    respondidas: Iterable[str] = (),
    universo: Iterable[Lacuna] = CATALOGO,
) -> tuple[DecisaoAberta, ...]:
    """As lacunas abertas que travam o plano — a combinação dos três predicados.

    É a função que o gate chama. Tupla vazia significa uma coisa só: nenhuma lacuna
    aberta dispara B1, B2 ou B3. **Não** significa que a especificação está completa —
    palpite não confirmado e decisão aberta assumível continuam existindo, e quem julga
    isso é `especificacao.completa`.
    """
    return tuple(
        decisao
        for decisao in classificar_lacunas(
            abertas,
            plataformas=plataformas,
            contextos=contextos,
            respondidas=respondidas,
            universo=universo,
        )
        if decisao.bloqueante
    )


def assumiveis_abertas(
    abertas: Iterable[Lacuna],
    *,
    plataformas: Iterable[Plataforma] = (),
    contextos: Iterable[Contexto] = (),
    respondidas: Iterable[str] = (),
    universo: Iterable[Lacuna] = CATALOGO,
) -> tuple[DecisaoAberta, ...]:
    """As abertas que não travam — e que mesmo assim saem inteiras, como pergunta.

    Existe como função pública, e não como "o resto que sobrou", porque a lista das
    assumíveis é entrega e não subproduto: é ela que impede o motor de decidir em
    silêncio o que escolheu não perguntar. Cada item traz a pergunta e o motivo, nunca
    um valor adotado.
    """
    return tuple(
        decisao
        for decisao in classificar_lacunas(
            abertas,
            plataformas=plataformas,
            contextos=contextos,
            respondidas=respondidas,
            universo=universo,
        )
        if not decisao.bloqueante
    )


def exigir_origem_declarada(origem: object) -> None:
    """Recusa `Origem.PADRAO_ASSUMIDO` como origem de resposta gravada.

    Fica aqui, e não no módulo de persistência, porque é regra e não mecanismo: quem
    escrever um segundo caminho de gravação amanhã encontra a proibição no mesmo lugar
    onde encontra a definição de bloqueante, em vez de ter de reparar que ela existia.

    A comparação é por texto para não exigir que quem chama importe `Origem` — o valor
    atravessa `estado.json` como texto de qualquer forma.
    """
    if str(origem) == "PADRAO_ASSUMIDO":
        raise PadraoAssumidoProibido(
            "resposta com origem PADRAO_ASSUMIDO: lacuna sem resposta sai como decisão "
            "aberta com a pergunta inteira, nunca como valor adotado pelo motor - "
            "assumível quer dizer que o motor segue sem perguntar, não que ele decide "
            "no lugar de alguém e não conta"
        )


def validar_bloqueio(
    partes: Mapping[str, ParteDoAceite] = PARTES_DO_ACEITE,
    *,
    catalogo: Iterable[Lacuna] = CATALOGO,
) -> Mapping[str, ParteDoAceite]:
    """Reprova mapa de aceite malformado e devolve o mapa validado.

    Mesma forma de `validar_catalogo` e `validar_taxonomia` — devolve o próprio dado
    para que a garantia ande junto dele — e duas regras:

    1. **Id que não existe em nenhum dos dois eixos.** Erro de digitação aqui não
       levanta nada em execução: a linha simplesmente nunca casa, B3 deixa de disparar
       para aquela lacuna, e o plano passa no gate sem aceite possível. É o defeito mais
       silencioso deste módulo.
    2. **Parte declarada sem nenhuma fonte.** Membro de `ParteDoAceite` que nenhuma
       lacuna fornece é enumeração crescendo sem o critério mudar — e pior, sugere a
       quem lê que aquele pedaço do aceite está coberto por alguém.
    """
    conhecidos = {lacuna.id for lacuna in catalogo}
    for lacunas in LACUNAS_POR_INTENCAO.values():
        conhecidos.update(lacuna.id for lacuna in lacunas)

    for identificador in partes:
        if identificador not in conhecidos:
            raise BloqueioInvalido(
                f"PARTES_DO_ACEITE aponta para {identificador!r}, que não existe no "
                "catálogo nem na taxonomia: a linha nunca casaria, B3 deixaria de "
                "disparar por ela e o defeito não aparece em execução"
            )

    sem_fonte = [parte for parte in ParteDoAceite if parte not in partes.values()]
    if sem_fonte:
        raise BloqueioInvalido(
            "parte do aceite sem nenhuma lacuna que a forneça: "
            + ", ".join(parte.value for parte in sem_fonte)
            + " - a enumeração cresceria sem o critério mudar, e quem lê acharia que "
            "esse pedaço do aceite está coberto"
        )
    return partes
