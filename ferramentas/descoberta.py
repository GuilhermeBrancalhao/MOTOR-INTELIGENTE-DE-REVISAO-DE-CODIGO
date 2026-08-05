"""A entrevista de descoberta gravada no estado — para o gate poder lê-la depois.

O pacote `ferramentas/elicitacao` sabe perguntar, classificar e decidir o que bloqueia,
e não sabe onde nada disso mora: ele só importa biblioteca padrão e não conhece
`estado.py`. Este módulo é a costura entre os dois. Ele guarda, sob a chave
`descoberta` do `.engine/estado.json`, o que foi perguntado e respondido, e devolve a
avaliação — bloqueantes e assumíveis — recalculada a partir do que está no disco.

**Por que no estado, e não num arquivo próprio.** O gate de fase (C4) e o gate do
programa (C5) já leem o estado, sob o mesmo cadeado, no mesmo instante em que decidem.
Um segundo arquivo criaria um segundo momento de leitura e a possibilidade de os dois
discordarem — e o modo de falhar seria o pior possível: a transição passa porque o
outro arquivo ainda não tinha a bloqueante.

**Só o que foi dito é gravado.** O bloco guarda pedido, intenção, eixos confirmados,
respostas e palpites pendentes. As decisões abertas e a lista de bloqueantes **não**
são gravadas: são derivadas, e derivada persistida envelhece. Responder uma lacuna
muda o veredito das outras (é o que B3 faz de propósito), e um retrato congelado no
disco diria "bloqueado" depois de a bloqueante ter sido respondida — ou, muito pior,
diria "livre" depois de uma regra mudar. Quem quer o veredito chama `avaliar`.

**Retrocompatibilidade.** `estado.VERSAO` continua 1 e não existe migração escrita, e
por isso nada aqui pode exigir a chave nova: estado antigo, sem `descoberta`, carrega,
lê e avalia sem levantar — a avaliação apenas responde `registrada=False`. O que ela
**não** faz é responder "sem bloqueante": não saber e estar livre são coisas
diferentes, e é o gate que decide o que fazer com a diferença (fechado, se seguir a
doutrina do motor).

**Quem muta usa `estado.atualizar()`, nunca `gravar()` direto.** Toda função de escrita
daqui passa por um mutador dentro do cadeado, e `test_nenhum_gravar_fora_do_estado`
varre este arquivo junto com os outros de produção — por texto, o que significa que nem
esta documentação pode escrever a chamada proibida por extenso.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ferramentas import estado
from ferramentas.elicitacao import (
    Contexto,
    DecisaoAberta,
    Intencao,
    Lacuna,
    LacunaDesconhecida,
    Origem,
    Palpite,
    Plataforma,
    aplicar_resposta,
    classificar_lacunas,
    classificar,
    detectar_contextos,
    detectar_plataformas,
    exigir_origem_declarada,
    lacunas_do_pedido,
    universo_completo,
)

#: A chave própria dentro do `estado.json`, ao lado de `pendencias`. Nome curto e
#: estável: ele viaja em arquivo de estado de projeto alheio e renomear custa migração.
CHAVE = "descoberta"

#: Versão do formato **deste bloco**, independente de `estado.VERSAO`. Separada porque
#: a elicitação vai evoluir num ritmo próprio, e amarrar as duas obrigaria a subir a
#: versão do estado inteiro — com a migração de tudo junto — para acrescentar um campo
#: aqui dentro.
VERSAO_BLOCO = 1


class DescobertaAusente(KeyError):
    """Mutação pedida sobre um estado que não tem bloco de descoberta.

    Herda de `KeyError` porque é isso: chave ausente. Levanta em vez de criar o bloco
    na hora porque criar exigiria inventar o pedido e a intenção — e intenção inventada
    escolhe *quais perguntas existem*, que é o erro mais caro deste motor.
    """


class DescobertaInvalida(ValueError):
    """O bloco existe e não é legível: versão desconhecida ou conteúdo estranho.

    Falha FECHADO, como todo predicado que libera portão neste repositório. Um bloco de
    versão futura lido por um motor antigo produziria uma avaliação plausível sobre
    campos que mudaram de significado, e o resultado dela liberaria uma transição.
    """


@dataclass(frozen=True, slots=True)
class Avaliacao:
    """O retrato da descoberta agora: o que está aberto, o que trava, o que não trava.

    Congelada, como `Especificacao`, e pelo mesmo motivo: é retrato. Responder uma
    lacuna produz outra avaliação, e ter as duas permite mostrar o que a resposta
    destravou.
    """

    registrada: bool
    pedido: str
    intencao: Intencao | None
    plataformas: tuple[Plataforma, ...]
    contextos: tuple[Contexto, ...]
    respondidas: tuple[str, ...]
    palpites_pendentes: tuple[Palpite, ...]
    abertas: tuple[DecisaoAberta, ...]

    @property
    def bloqueantes(self) -> tuple[DecisaoAberta, ...]:
        """As abertas que travam o plano, na ordem dos eixos."""
        return tuple(decisao for decisao in self.abertas if decisao.bloqueante)

    @property
    def assumiveis(self) -> tuple[DecisaoAberta, ...]:
        """As abertas que não travam — e que mesmo assim saem como pergunta inteira.

        Nenhuma delas carrega valor: `DecisaoAberta` não tem campo para isso. Assumível
        quer dizer que o motor segue sem perguntar, e não que ele decidiu no lugar de
        alguém.
        """
        return tuple(decisao for decisao in self.abertas if not decisao.bloqueante)

    @property
    def liberado_para_planejar(self) -> bool:
        """Só quando há descoberta registrada **e** nenhuma bloqueante aberta.

        Descoberta ausente devolve `False`, e essa é a metade que costuma ser escrita
        errada: "não há bloqueante registrada" e "não há bloqueante" parecem a mesma
        frase e são opostas. Predicado que libera portão falha fechado.
        """
        return self.registrada and not self.bloqueantes

    def resumo(self) -> str:
        """Texto para quem leu "bloqueado" na tela e quer saber o que falta.

        Cada bloqueante sai com a pergunta inteira e com o motivo do predicado que a
        travou; cada assumível sai com a pergunta inteira também. Em nenhum dos dois
        casos aparece valor adotado — a lista de assumíveis existe justamente para que
        o que o motor escolheu não perguntar fique escrito.
        """
        if not self.registrada:
            return (
                "Descoberta não registrada neste ciclo: não se sabe que trabalho foi "
                "pedido, nem quais lacunas estão abertas."
            )

        linhas = [
            f"Intenção: {self.intencao.value if self.intencao else '(indeterminada)'}",
            f"Respondidas: {len(self.respondidas)} | "
            f"Bloqueantes abertas: {len(self.bloqueantes)} | "
            f"Assumíveis abertas: {len(self.assumiveis)}",
        ]
        if self.bloqueantes:
            linhas += ["", "BLOQUEANTES (o plano não anda sem estas):"]
            for decisao in self.bloqueantes:
                linhas.append(f"- [{decisao.id}] {decisao.pergunta}")
                for motivo in decisao.motivos:
                    linhas.append(f"    porque {motivo}")
        else:
            linhas += ["", "BLOQUEANTES: nenhuma."]

        if self.assumiveis:
            linhas += [
                "",
                "DECISÕES ABERTAS assumíveis (o motor segue sem perguntar, e NÃO "
                "decide por ninguém):",
            ]
            linhas += [f"- [{d.id}] {d.pergunta}" for d in self.assumiveis]
        return "\n".join(linhas)


# ---------------------------------------------------------------------------
# Leitura
# ---------------------------------------------------------------------------


def do_estado(dados: dict | None) -> dict | None:
    """O bloco de descoberta de dentro de um estado já lido, ou `None`.

    Estado ausente e estado sem a chave dão o mesmo `None`: os dois significam "esta
    pasta nunca registrou descoberta", e distingui-los aqui só produziria dois ramos
    idênticos em quem chama. O que **não** é tolerado é bloco de versão desconhecida,
    que levanta.
    """
    if not isinstance(dados, dict):
        return None
    bloco = dados.get(CHAVE)
    if bloco is None:
        return None
    if not isinstance(bloco, dict):
        raise DescobertaInvalida(
            f"chave {CHAVE!r} do estado não é um objeto JSON: {type(bloco).__name__}"
        )
    versao = bloco.get("versao")
    if versao != VERSAO_BLOCO:
        raise DescobertaInvalida(
            f"bloco de descoberta na versão {versao!r}, esperada {VERSAO_BLOCO}: um "
            "motor antigo lendo bloco novo produziria avaliação plausível sobre campos "
            "que mudaram de significado - e essa avaliação libera transição"
        )
    return bloco


def ler(raiz: Path) -> dict | None:
    """O bloco de descoberta gravado nesta pasta, ou `None`."""
    return do_estado(estado.carregar(raiz))


def _eixos(bloco: dict) -> tuple[tuple[Plataforma, ...], tuple[Contexto, ...]]:
    try:
        plataformas = tuple(Plataforma(valor) for valor in bloco.get("plataformas", []))
        contextos = tuple(Contexto(valor) for valor in bloco.get("contextos", []))
    except (ValueError, TypeError) as erro:
        raise DescobertaInvalida(f"eixo desconhecido no bloco de descoberta: {erro}") from erro
    return plataformas, contextos


def _intencao(bloco: dict) -> Intencao:
    try:
        return Intencao(str(bloco.get("intencao", "")).strip().upper())
    except ValueError as erro:
        raise DescobertaInvalida(
            f"intenção {bloco.get('intencao')!r} no bloco de descoberta não existe na "
            "taxonomia"
        ) from erro


def _respostas(bloco: dict) -> dict[str, dict]:
    respostas = bloco.get("respostas") or {}
    if not isinstance(respostas, dict):
        raise DescobertaInvalida("`respostas` do bloco de descoberta não é um objeto")
    return respostas


def ativas(bloco: dict) -> tuple[Lacuna, ...]:
    """As lacunas que fazem sentido para este pedido agora, respondidas ou não.

    O cruzamento dos três eixos com a intenção **já decidida** — nunca reclassificando
    o texto. Reclassificar a cada leitura faria o conjunto de perguntas mudar debaixo de
    uma entrevista em andamento se alguém corrigisse uma palavra do pedido.
    """
    plataformas, contextos = _eixos(bloco)
    return lacunas_do_pedido(
        bloco.get("pedido", ""),
        plataformas,
        contextos,
        intencao=_intencao(bloco),
    )


def avaliar(dados: dict | None) -> Avaliacao:
    """A avaliação da descoberta a partir de um estado já lido. Nunca escreve.

    Pura de propósito: o gate a chama de dentro do mutador de `estado.atualizar`, com o
    cadeado na mão, e uma função que fizesse E/S ali dentro tentaria pegar o cadeado de
    novo — que não é reentrante e travaria até o timeout.

    Estado sem descoberta devolve `registrada=False` com todos os campos vazios, e não
    levanta: é o caso do estado antigo, anterior a este ciclo, e ele tem de carregar.
    """
    bloco = do_estado(dados)
    if bloco is None:
        return Avaliacao(
            registrada=False,
            pedido="",
            intencao=None,
            plataformas=(),
            contextos=(),
            respondidas=(),
            palpites_pendentes=(),
            abertas=(),
        )

    intencao = _intencao(bloco)
    plataformas, contextos = _eixos(bloco)
    respostas = _respostas(bloco)
    abertas = tuple(
        lacuna for lacuna in ativas(bloco) if lacuna.id not in respostas
    )

    decisoes = classificar_lacunas(
        abertas,
        plataformas=plataformas,
        contextos=contextos,
        respondidas=tuple(respostas),
        universo=universo_completo(intencao),
    )
    return Avaliacao(
        registrada=True,
        pedido=bloco.get("pedido", ""),
        intencao=intencao,
        plataformas=plataformas,
        contextos=contextos,
        respondidas=tuple(respostas),
        palpites_pendentes=tuple(
            Palpite(
                valor=str(item.get("valor", "")),
                origem=Origem.INFERIDO,
                evidencia=str(item.get("evidencia", "")),
                confianca=str(item.get("confianca", "")),
            )
            for item in bloco.get("palpites_pendentes", [])
        ),
        abertas=decisoes,
    )


def avaliar_do_disco(raiz: Path) -> Avaliacao:
    """`avaliar` sobre o estado desta pasta. Conveniência para quem só quer olhar."""
    return avaliar(estado.carregar(raiz))


# ---------------------------------------------------------------------------
# Escrita — sempre por `estado.atualizar`
# ---------------------------------------------------------------------------


def registrar(
    raiz: Path,
    pedido: str,
    *,
    intencao: Intencao | str | None = None,
    plataformas: tuple[Plataforma | str, ...] = (),
    contextos: tuple[Contexto | str, ...] = (),
    agora: str | None = None,
) -> dict:
    """Abre a descoberta do ciclo: classifica o pedido e guarda os palpites.

    `intencao` explícita existe para depois de uma pergunta de desempate; sem ela, o
    pedido é classificado aqui e `IntencaoIndeterminada` **sobe**, sem gravar nada.
    Registrar com intenção chutada seria escolher em silêncio quais perguntas existem —
    o erro que a taxonomia inteira foi escrita para não cometer.

    Os palpites de plataforma e contexto entram como **pendentes**, nunca aplicados:
    inferência não vira eixo confirmado sem alguém dizer que sim (`confirmar`), e
    enquanto estiver pendente ela consta do bloco como palpite, com a evidência.

    Só a chave `descoberta` é tocada. O mutador devolve o mesmo dicionário do disco com
    uma chave a mais — `cartoes`, `decisoes`, `pendencias` e o resto do ciclo passam
    intactos, e é por isso que isto usa `atualizar` e não monta um estado novo.
    """
    alvo = Intencao(str(intencao).strip().upper()) if intencao is not None else classificar(pedido)
    palpites = [*detectar_plataformas(pedido), *detectar_contextos(pedido)]
    p = tuple(Plataforma(str(valor)) for valor in plataformas)
    c = tuple(Contexto(str(valor)) for valor in contextos)

    def _mutar(dados: dict | None) -> dict | None:
        if dados is None:
            raise DescobertaAusente(
                "não há estado nesta pasta: ligue o ENGINE antes de registrar a "
                "descoberta - descoberta sem ciclo não tem a quem bloquear"
            )
        dados[CHAVE] = {
            "versao": VERSAO_BLOCO,
            "pedido": pedido,
            "intencao": alvo.value,
            "plataformas": [str(valor) for valor in p],
            "contextos": [str(valor) for valor in c],
            "respostas": {},
            "palpites_pendentes": [
                {
                    "valor": palpite.valor,
                    "evidencia": palpite.evidencia,
                    "confianca": palpite.confianca,
                }
                for palpite in palpites
            ],
            "registrado_em": agora,
            "atualizado_em": agora,
        }
        return dados

    return _bloco_apos(estado.atualizar(raiz, _mutar))


def responder(
    raiz: Path,
    lacuna_id: str,
    valor: str,
    *,
    origem: Origem | str = Origem.RESPONDIDO,
    agora: str | None = None,
) -> dict:
    """Grava a resposta de uma lacuna, preservando todo o resto do bloco.

    Três coisas acontecem, e nenhuma delas é reconstruir a entrevista: a resposta entra
    no mapa por id; se o valor nomear plataforma ou contexto, o eixo correspondente é
    atualizado pela **mesma** regra que B1 usa para prever o efeito
    (`bloqueio.aplicar_resposta`); e o carimbo de atualização anda. Responder de novo o
    mesmo id substitui o valor — correção é normal em entrevista.

    `Origem.PADRAO_ASSUMIDO` é recusado por `exigir_origem_declarada`. Uma lacuna sem
    resposta sai como decisão aberta com a pergunta inteira, e não como valor que o
    motor adotou e não contou a ninguém.

    Id que não está ativo para este pedido levanta `LacunaDesconhecida`, e nada é
    gravado. Aceitar em silêncio guardaria a resposta num balde que ninguém lê,
    deixaria a lacuna verdadeira aberta, e a pessoa lembraria de ter respondido.
    """
    exigir_origem_declarada(origem)

    def _mutar(dados: dict | None) -> dict | None:
        bloco = _exigir(dados)
        conhecidas = {lacuna.id for lacuna in ativas(bloco)}
        if lacuna_id not in conhecidas:
            raise LacunaDesconhecida(
                f"lacuna {lacuna_id!r} não está ativa para este pedido "
                f"({_intencao(bloco).value}); ativas agora: {len(conhecidas)}"
            )
        respostas = dict(_respostas(bloco))
        respostas[lacuna_id] = {"valor": valor, "origem": str(origem), "em": agora}
        bloco["respostas"] = respostas

        plataformas, contextos = _eixos(bloco)
        depois_p, depois_c = aplicar_resposta(valor, plataformas, contextos)
        bloco["plataformas"] = [p.value for p in Plataforma if p in depois_p]
        bloco["contextos"] = [c.value for c in Contexto if c in depois_c]
        bloco["atualizado_em"] = agora
        return dados

    return _bloco_apos(estado.atualizar(raiz, _mutar))


def confirmar(raiz: Path, valor: str, *, agora: str | None = None) -> dict:
    """Aceita um palpite: tira da pendência e aplica o eixo que ele nomeia.

    Aplicar pode destravar um bloco inteiro de lacunas — é o mesmo efeito de responder
    `onde_roda` —, e por isso confirmar palpite vem antes de perguntar no laço da
    entrevista.
    """
    return _resolver_palpite(raiz, valor, aplicar=True, agora=agora)


def recusar(raiz: Path, valor: str, *, agora: str | None = None) -> dict:
    """Rejeita um palpite: tira da pendência e **não** aplica nada.

    Recusar é diferente de ignorar. Ignorado, o palpite continua pendente e a
    especificação corretamente não se declara completa. Recusado, ele sai sem deixar
    rastro de valor assumido em lugar nenhum.
    """
    return _resolver_palpite(raiz, valor, aplicar=False, agora=agora)


def _resolver_palpite(raiz: Path, valor: str, *, aplicar: bool, agora: str | None) -> dict:
    alvo = str(valor).strip().upper()

    def _mutar(dados: dict | None) -> dict | None:
        bloco = _exigir(dados)
        bloco["palpites_pendentes"] = [
            item
            for item in bloco.get("palpites_pendentes", [])
            if str(item.get("valor", "")).strip().upper() != alvo
        ]
        if aplicar:
            plataformas, contextos = _eixos(bloco)
            depois_p, depois_c = aplicar_resposta(alvo, plataformas, contextos)
            bloco["plataformas"] = [p.value for p in Plataforma if p in depois_p]
            bloco["contextos"] = [c.value for c in Contexto if c in depois_c]
        bloco["atualizado_em"] = agora
        return dados

    return _bloco_apos(estado.atualizar(raiz, _mutar))


def _exigir(dados: dict | None) -> dict:
    bloco = do_estado(dados)
    if bloco is None:
        raise DescobertaAusente(
            f"o estado desta pasta não tem a chave {CHAVE!r}: registre a descoberta "
            "antes de responder - criar o bloco aqui exigiria inventar o pedido e a "
            "intenção, e intenção inventada escolhe quais perguntas existem"
        )
    return bloco


def _bloco_apos(dados: dict | None) -> dict:
    """O bloco recém-gravado, para quem chamou não ter de reler o disco."""
    bloco = do_estado(dados)
    if bloco is None:  # pragma: no cover - `atualizar` só devolve `None` se o mutador devolver
        raise DescobertaAusente("a gravação não produziu bloco de descoberta")
    return bloco
