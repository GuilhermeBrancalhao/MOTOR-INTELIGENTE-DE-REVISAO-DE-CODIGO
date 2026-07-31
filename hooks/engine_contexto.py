#!/usr/bin/env python3
"""Hook UserPromptSubmit do ENGINE.

Injeta o cartão de estado a cada turno. É este hook — e não o texto de nenhuma
skill — que faz o modo do motor sobreviver à compactação do contexto: skills são
texto de instrução que o modelo pode esquecer depois de compactar; o estado em
disco (`ferramentas.estado`) não esquece, e este hook o traz de volta para dentro
do turno a cada prompt do usuário.

Contrato (confirmado na documentação oficial do Claude Code, hooks.md): para a
maioria dos eventos de hook, o stdout só vai para o log de depuração. `UserPromptSubmit`
é uma das exceções explícitas — "stdout is added as context that Claude can see and
act on" — então basta imprimir o cartão em texto puro no stdout e sair com `0`; não é
preciso (nem obrigatório) devolver JSON com `hookSpecificOutput.additionalContext`.
JSON só seria necessário para usar `decision: "block"`, o que este hook nunca faz.

Falha segura NA DIREÇÃO OPOSTA à do PreToolUse (`engine_risco.py`): lá, erro
bloqueia a ação por segurança. Aqui, o cartão é conveniência, não trava — bloquear o
turno do usuário porque o cartão não montou seria pior que não ter o cartão. Por
isso qualquer falha no caminho (estado ilegível, config ilegível, montagem do
cartão) devolve `0` sem imprimir nada, nunca propaga a exceção.

Teto duro de linhas, lido de `teto_cartao_linhas`: acima dele, o motor passa a
competir com o pedido do usuário pelo mesmo espaço de atenção — que é exatamente a
doença que ele veio curar. O teto vale para qualquer estado, inclusive um com 50
decisões, 50 cartões e 50 diffs pendentes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from _comum import forcar_utf8, raiz_do_ciclo  # noqa: E402

# Ver `_comum.forcar_utf8`: sem isso, acento no cartão sai como mojibake no console
# do Windows.
forcar_utf8()

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ferramentas import config, estado, trilha  # noqa: E402

INVARIANTES = (
    "1. Nunca afirmar sucesso sem ter olhado. Rodou, cola a saída; não rodou, diz que não rodou.",
    "2. Nunca ajustar o teste para o código passar. O teste é o contrato.",
    "3. Nunca inventar arquivo, API, número ou regra de negócio. Sem evidência, é pendência.",
    "4. Nunca tocar em item fora do escopo declarado do ciclo.",
    "5. Toda decisão técnica sai com a justificativa junto.",
)

# Piso do teto de linhas do cartão: as 3 linhas de cabeçalho (título, fase/modo,
# objetivo) mais as 6 do rodapé (título "Invariantes:" + os 5 invariantes). Um
# teto configurado abaixo disso é erro de configuração, não instrução — por isso
# vira piso, não é obedecido ao pé da letra.
MINIMO_CARTAO = 9

#: Default do teto quando a configuração não traz um valor utilizável.
_TETO_DEFAULT = 40


def _teto_bruto(cfg: dict) -> int:
    """Lê `cfg['teto_cartao_linhas']` e normaliza pra inteiro com segurança.

    Valor não numérico (ex.: `"abc"`) cai no default — NUNCA deixa o
    `ValueError`/`TypeError` subir, porque no hook isso viraria "cartão inteiro
    some por um erro de digitação na configuração". Todo leitor do teto neste
    arquivo passa por aqui; ninguém faz `int(cfg.get(...))` direto.
    """
    bruto = cfg.get("teto_cartao_linhas", _TETO_DEFAULT)
    try:
        return int(bruto)
    except (TypeError, ValueError):
        return _TETO_DEFAULT


def _teto_efetivo(cfg: dict) -> int:
    """Teto normalizado (`_teto_bruto`) com o piso `MINIMO_CARTAO` aplicado.

    Sem isso, `linhas[:teto]` com `teto` negativo vira "remova as últimas N
    linhas" em vez de "limite a N" — e um teto positivo mas menor que o piso
    corta cabeçalho e/ou rodapé, que são inegociáveis.
    """
    return max(_teto_bruto(cfg), MINIMO_CARTAO)


def _cortar(texto: str, limite: int) -> str:
    """Colapsa espaços e corta com reticência — protege o teto de linhas de um
    único campo gigante (ex.: objetivo de 400 caracteres) virando várias linhas."""
    texto = " ".join(str(texto).split())
    return texto if len(texto) <= limite else texto[: limite - 1] + "…"


def _campo(texto, limite: int) -> str:
    """Redige credenciais e corta no limite — todo texto vindo do estado passa aqui.

    A redação é `trilha.redigir`, de propósito por referência e não por cópia: a
    trilha é a fonte única do que conta como credencial, e duas listas de padrões
    em dois arquivos divergem na primeira vez que uma delas ganha um padrão novo.
    O cartão precisa da MESMA proteção da trilha — pior, até: a trilha é lida sob
    demanda, o cartão volta ao contexto do modelo a cada turno.

    Redigir ANTES de cortar: um token truncado pelo corte ainda seria
    reconhecível; redigido primeiro, o que sobra é só a marca.
    """
    return _cortar(trilha.redigir(str(texto)), limite)


def montar_cartao(dados: dict, cfg: dict) -> str:
    """Monta o cartão de estado, sempre dentro do teto efetivo de linhas.

    O teto de `cfg['teto_cartao_linhas']` passa por `_teto_efetivo`: normalizado
    pra inteiro (valor não numérico cai no default 40) e nunca abaixo do piso
    `MINIMO_CARTAO`. Com o piso garantido, cabeçalho (fase/modo/objetivo) e
    rodapé (invariantes) NUNCA são cortados — são inegociáveis. Quem cede quando
    o orçamento de linhas aperta é o corpo (cartões, decisões, diffs pendentes,
    pendências), que pode ficar vazio.
    """
    teto = _teto_efetivo(cfg)
    ciclo = dados.get("ciclo", {})
    cabecalho = [
        "== ENGINE ativo ==",
        f"Fase: {dados.get('fase', '?')}   Modo: {ciclo.get('modo', 'normal')}",
        f"Objetivo do ciclo: {_campo(ciclo.get('objetivo', ''), 160)}",
    ]
    rodape = ["Invariantes:", *INVARIANTES]

    orcamento = max(teto - len(cabecalho) - len(rodape), 0)
    corpo: list[str] = []

    def acrescentar(linha: str) -> None:
        if len(corpo) < orcamento:
            corpo.append(linha)

    cartoes = dados.get("cartoes") or []
    if cartoes:
        acrescentar(f"Cartões: {_campo(', '.join(map(str, cartoes)), 120)}")

    decisoes = dados.get("decisoes") or []
    if decisoes:
        acrescentar("Decisões fechadas:")
        for item in decisoes:
            acrescentar(
                f"  - {_campo(item.get('o_que', ''), 70)}: {_campo(item.get('porque', ''), 70)}"
            )

    diffs = dados.get("diffs_pendentes") or []
    if diffs:
        acrescentar(
            f"Diffs por apresentar ({len(diffs)}): {_campo(', '.join(map(str, diffs)), 120)}"
        )

    pendencias = dados.get("pendencias") or []
    if pendencias:
        acrescentar(
            f"Pendências ({len(pendencias)}): {_campo('; '.join(map(str, pendencias)), 120)}"
        )

    linhas = cabecalho + corpo[:orcamento] + rodape
    return "\n".join(linhas[:teto])


def _com_avisos(cartao: str, cfg: dict) -> str:
    """Acrescenta os avisos de configuração (`cfg['_avisos']`) ao cartão, sem nunca
    furar o teto de linhas — os avisos entram no mesmo orçamento, não por fora dele.

    O teto passa por `_teto_bruto` (nunca por `int(cfg.get(...))` direto): um valor
    não numérico aqui derrubava o cartão inteiro — o `ValueError` subia até o
    `try/except` de `principal()`, que devolve 0 sem imprimir nada. E teto zero ou
    negativo não é "limite apertado", é erro de configuração: `linhas[:0]` apagava
    o cartão por completo e `linhas[:-n]` removia as últimas linhas — os
    invariantes do rodapé e o próprio aviso que deveria aparecer. Nesses casos o
    teto cai no default, o mesmo destino do valor não numérico. Teto positivo
    continua sendo obedecido à risca, como sempre foi.
    """
    avisos = cfg.get("_avisos") or []
    if not avisos:
        return cartao
    teto = _teto_bruto(cfg)
    if teto < 1:
        teto = _TETO_DEFAULT
    linhas = cartao.splitlines()
    for aviso in avisos:
        # Aviso também é texto que veio de fora (nome de chave, item de config do
        # projeto): recebe a mesma redação do resto do cartão.
        linhas.append(f"ENGINE aviso: {trilha.redigir(str(aviso))}")
    return "\n".join(linhas[:teto])


def principal() -> int:
    # Ao contrário do PreToolUse, aqui qualquer falha no caminho (entrada
    # ilegível, estado corrompido, config quebrada, bug na montagem do cartão)
    # devolve 0 sem imprimir nada. Nunca deixa a exceção subir: o cartão é
    # conveniência, não pode atrapalhar o turno do usuário.
    try:
        try:
            evento = json.load(sys.stdin)
        except Exception:  # noqa: BLE001
            return 0

        if not isinstance(evento, dict):
            return 0

        raiz = raiz_do_ciclo(Path(evento.get("cwd") or "."))

        dados = estado.carregar(raiz)
        if not dados or not dados.get("ativo"):
            return 0

        cfg = config.carregar(raiz)
        cartao = montar_cartao(dados, cfg)
        cartao = _com_avisos(cartao, cfg)

        if cartao.strip():
            print(cartao)
        return 0
    except Exception:  # noqa: BLE001
        return 0


if __name__ == "__main__":
    sys.exit(principal())
