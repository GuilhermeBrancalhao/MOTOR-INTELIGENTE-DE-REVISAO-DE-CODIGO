"""Apoio de teste: fechar a entrevista de descoberta de um ciclo já ligado.

Não é `test_*.py` e não é coletado: é código de apoio, importado por quem precisa de
um ciclo que **passe** no gate de `DESCOBERTA -> ANALISE`. Vive num módulo próprio
porque dois arquivos de teste precisam do mesmo preparo — `test_gate_fase.py`, que
exercita o gate, e `test_hooks.py`, que só quer chegar em BUILD para testar outra
coisa — e duas cópias divergiriam no primeiro ajuste do catálogo de lacunas.

**Responde de verdade, não desliga o gate.** O preparo passa pela mesma API pública
que uma sessão real usaria (`descoberta.registrar` e `descoberta.responder`), e não
por um atalho que injete `liberado_para_planejar=True` no estado. Um atalho faria os
testes que atravessam a fase pararem de exercitar o gate — e ele deixaria de ser
protegido justamente pelos testes que mais o atravessam.
"""
from __future__ import annotations

from pathlib import Path

from ferramentas import descoberta
from ferramentas.elicitacao import universo_completo

#: Pedido com sinal de intenção explícito. A intenção também é passada à mão em
#: `fechar_descoberta` para o preparo não depender do classificador de texto: mudar um
#: termo da taxonomia não pode quebrar testes que não são sobre classificação.
PEDIDO_PADRAO = "construir um sistema novo que soma dois numeros"

#: Teto do laço de respostas. Responder uma lacuna pode ativar outras (é o predicado
#: B1 fazendo o seu trabalho), então o laço não tem número fixo de voltas — mas laço de
#: teste sem teto vira suíte pendurada quando alguém introduz um ciclo na regra.
LIMITE_DE_VOLTAS = 40


def fechar_descoberta(
    raiz: Path,
    pedido: str = PEDIDO_PADRAO,
    *,
    intencao: str = "MATERIALIZAR",
    agora: str = "2026-08-05T10:00:00",
) -> tuple[str, ...]:
    """Registra a descoberta e responde todas as bloqueantes. Devolve os ids respondidos."""
    descoberta.registrar(raiz, pedido, intencao=intencao, agora=agora)
    return responder_bloqueantes(raiz, agora=agora)


def resposta_para(lacuna_id: str, intencao: str = "MATERIALIZAR") -> str:
    """Uma resposta **admissível** para a lacuna: a primeira opção, quando ela tem opções.

    Lacuna com `opcoes` declaradas só aceita uma delas — `descoberta.responder` recusa o
    resto, porque é sobre esse conjunto que B1 prevê o que responder destrava. Texto
    livre em `onde_roda` era gravado e não ativava plataforma nenhuma: a lacuna fechava,
    o bloco WEB nunca entrava, e o preparo produzia um ciclo que passava no gate com um
    ramo inteiro da entrevista por existir. O preparo tem de responder como uma sessão
    real responderia, ou ele deixa de preparar o que promete.
    """
    for lacuna in universo_completo(intencao):
        if lacuna.id == lacuna_id:
            return lacuna.opcoes[0] if lacuna.opcoes else f"resposta de teste para {lacuna_id}"
    return f"resposta de teste para {lacuna_id}"


def responder_bloqueantes(raiz: Path, *, agora: str = "2026-08-05T10:00:00") -> tuple[str, ...]:
    """Responde uma bloqueante por vez, reavaliando entre cada resposta.

    Reavaliar a cada volta não é preciosismo: B3 muda o veredito das outras lacunas
    conforme as partes do critério de aceite vão sendo cobertas, e B1 pode ativar
    lacunas que nem existiam quando o laço começou. Responder a lista inicial de uma vez
    deixaria bloqueante nova aberta e o gate recusaria a transição no meio de um teste
    que não é sobre isso.
    """
    respondidas: list[str] = []
    for _ in range(LIMITE_DE_VOLTAS):
        avaliacao = descoberta.avaliar_do_disco(raiz)
        if not avaliacao.bloqueantes:
            return tuple(respondidas)
        alvo = avaliacao.bloqueantes[0]
        intencao = avaliacao.intencao.value if avaliacao.intencao else "MATERIALIZAR"
        descoberta.responder(raiz, alvo.id, resposta_para(alvo.id, intencao), agora=agora)
        respondidas.append(alvo.id)
    raise AssertionError(
        f"{LIMITE_DE_VOLTAS} respostas e ainda há bloqueante aberta: "
        f"{[decisao.id for decisao in descoberta.avaliar_do_disco(raiz).bloqueantes]}"
    )
