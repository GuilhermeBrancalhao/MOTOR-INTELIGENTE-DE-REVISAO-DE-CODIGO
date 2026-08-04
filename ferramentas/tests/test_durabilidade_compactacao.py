"""Durabilidade do modo através da compactação de contexto.

O que estava em aberto
----------------------
O `README.md` registrava a durabilidade como **projeto, não fato observado**: o
motor nunca tinha atravessado uma sessão longa com compactação de verdade, e
`aceite/simular_turnos.py` dispara UMA compactação, no turno 10, numa sequência
fixa. Isso demonstra a mecânica num ponto; não estabelece a propriedade.

O que este módulo estabelece
----------------------------
A durabilidade não é uma aposta sobre o que a compactação faz — é consequência de
uma propriedade verificável do hook que injeta o cartão:

    o cartão é função APENAS do disco (`.engine/`, config, projeto),
    e de nada que a compactação possa destruir.

A compactação destrói contexto e reescreve a transcrição. Se o hook nunca lê
transcrição, `session_id`, mensagens ou qualquer coisa derivada do contexto, então
não existe caminho pelo qual a compactação altere a saída dele. É isso que
`test_o_cartao_nao_depende_de_nada_que_a_compactacao_destroi` trava, estaticamente,
e é a razão mecânica de a durabilidade valer.

Os demais testes exercem a propriedade dinamicamente, com os hooks REAIS rodando
como subprocesso — compactação em TODO limite de turno, compactações seguidas, e
compactação interrompida no meio — comparando sempre contra uma execução de
controle sem compactação nenhuma.

O que continua não observado (e não é isto que estes testes afirmam): uma sessão
real do Claude Code atravessando auto-compactação. Aqui a compactação é o hook
`PreCompact` disparado de verdade mais o descarte de contexto — que para o motor é
um não-evento justamente porque ele não lê contexto. O resíduo é o contrato do
Claude Code (disparar `PreCompact` e preservar o `cwd`), não o motor.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from ferramentas import estado

RAIZ_DO_MOTOR = Path(__file__).resolve().parent.parent.parent
HOOK_CONTEXTO = RAIZ_DO_MOTOR / "hooks" / "engine_contexto.py"
HOOK_SALVAR = RAIZ_DO_MOTOR / "hooks" / "engine_salvar.py"

TURNOS = 12

#: Campos do evento de hook que a compactação destrói ou reescreve. Ler qualquer um
#: deles para montar o cartão criaria a dependência que quebra a durabilidade.
CAMPOS_VOLATEIS = (
    "transcript_path",
    "session_id",
    "messages",
    "conversation",
    "history",
    "prompt",
    "context",
    "compaction_trigger",
)


def _rodar(hook: Path, payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(hook)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(cwd),
        timeout=120,
    )


def _cartao(raiz: Path, **extras) -> str:
    """Um turno de `UserPromptSubmit`: o cartão que o motor injeta no contexto."""
    evento = {"cwd": str(raiz), "hook_event_name": "UserPromptSubmit", **extras}
    resultado = _rodar(HOOK_CONTEXTO, evento, raiz)
    assert resultado.returncode == 0, resultado.stderr
    return resultado.stdout


def _compactar(raiz: Path, gatilho: str = "auto") -> subprocess.CompletedProcess:
    """Uma compactação: o `PreCompact` real, seguido do descarte de contexto.

    O descarte não precisa ser encenado — o cartão é regerado do zero a cada turno
    a partir do disco, então "contexto descartado" e "contexto intacto" produzem a
    mesma chamada. Essa indiferença é a propriedade sob teste.
    """
    evento = {"cwd": str(raiz), "hook_event_name": "PreCompact", "compaction_trigger": gatilho}
    resultado = _rodar(HOOK_SALVAR, evento, raiz)
    # PreCompact NUNCA pode sair != 0: saída 2 bloquearia a compactação.
    assert resultado.returncode == 0, resultado.stderr
    return resultado


def _projeto(tmp_path: Path) -> Path:
    raiz = tmp_path / "projeto"
    raiz.mkdir(parents=True)
    estado.novo_ciclo(raiz, "provar durabilidade sob compactacao", "2026-08-04T10:00:00")
    return raiz


def _normalizar(cartao: str) -> str:
    """Tira do cartão o que varia por relógio, não por compactação.

    `ultima_consolidacao` é gravada pelo PreCompact, então ela DEVE diferir entre a
    execução com compactação e a de controle — comparar o cartão bruto acusaria
    diferença onde há funcionamento correto. Tudo o mais tem de bater byte a byte.
    """
    cartao = re.sub(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", "<CARIMBO>", cartao)
    return "\n".join(
        linha
        for linha in cartao.splitlines()
        if "consolida" not in linha.lower()
    )


# --------------------------------------------------------------------------
# A razão mecânica: o cartão não olha para o que a compactação leva
# --------------------------------------------------------------------------


def _chaves_do_evento(arvore: ast.AST) -> set[str]:
    """Toda chave que o código lê de `evento`, por `.get("x")` ou por `evento["x"]`."""
    chaves: set[str] = set()
    for no in ast.walk(arvore):
        if (
            isinstance(no, ast.Call)
            and isinstance(no.func, ast.Attribute)
            and no.func.attr == "get"
            and isinstance(no.func.value, ast.Name)
            and no.func.value.id == "evento"
            and no.args
            and isinstance(no.args[0], ast.Constant)
        ):
            chaves.add(no.args[0].value)
        elif (
            isinstance(no, ast.Subscript)
            and isinstance(no.value, ast.Name)
            and no.value.id == "evento"
            and isinstance(no.slice, ast.Constant)
        ):
            chaves.add(no.slice.value)
    return chaves


def _literais_de_codigo(arvore: ast.AST) -> set[str]:
    """Strings que o código usa de fato — sem docstrings, e comentários nem entram
    na árvore. Prosa citando "contexto" ou "prompt" não pode reprovar a trava."""
    docstrings = {
        no.body[0].value
        for no in ast.walk(arvore)
        if isinstance(no, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        and no.body
        and isinstance(no.body[0], ast.Expr)
        and isinstance(no.body[0].value, ast.Constant)
        and isinstance(no.body[0].value.value, str)
    }
    return {
        no.value
        for no in ast.walk(arvore)
        if isinstance(no, ast.Constant)
        and isinstance(no.value, str)
        and no not in docstrings
    }


def test_o_cartao_nao_depende_de_nada_que_a_compactacao_destroi():
    """A trava estrutural — a durabilidade sai daqui, não de observação.

    `engine_contexto.py` lê do evento apenas `cwd`. Enquanto isso for verdade, não
    existe caminho pelo qual a compactação (que descarta contexto e reescreve a
    transcrição) mude o cartão: o hook nem chega a olhar para essas coisas.

    Se alguém acrescentar uma leitura de `transcript_path` — para enriquecer o
    cartão com o histórico, que é uma ideia natural —, a durabilidade deixa de
    valer no mesmo commit, e em silêncio. Este teste é o que faz esse commit ficar
    vermelho.
    """
    arvore = ast.parse(HOOK_CONTEXTO.read_text(encoding="utf-8"))

    chaves_lidas = _chaves_do_evento(arvore)
    assert chaves_lidas == {"cwd"}, (
        "engine_contexto.py passou a ler do evento além de 'cwd': "
        f"{sorted(chaves_lidas)} — se o que ele lê é destruído pela compactação, "
        "o modo deixa de sobreviver a ela"
    )

    volateis_usados = sorted(_literais_de_codigo(arvore) & set(CAMPOS_VOLATEIS))
    assert not volateis_usados, (
        "engine_contexto.py usa campo volátil de contexto como literal: "
        f"{volateis_usados} — o cartão tem de ser função só do disco"
    )


def test_o_cartao_ignora_evento_com_transcricao_e_sessao(tmp_path):
    """A contraprova dinâmica da trava acima: enfiar os campos voláteis no evento,
    com valores absurdos, não muda um byte do cartão."""
    raiz = _projeto(tmp_path)

    limpo = _cartao(raiz)
    sujo = _cartao(
        raiz,
        transcript_path=str(tmp_path / "nao-existe.jsonl"),
        session_id="sessao-que-a-compactacao-vai-trocar",
        messages=["contexto", "que", "some"],
        compaction_trigger="auto",
    )

    assert limpo.strip()
    assert limpo == sujo


# --------------------------------------------------------------------------
# A propriedade, exercida com os hooks reais
# --------------------------------------------------------------------------


def test_compactacao_em_todo_limite_de_turno_nao_muda_o_cartao(tmp_path):
    """Compactar entre TODOS os turnos produz a mesma sequência de cartões que
    não compactar nenhuma vez.

    `aceite/simular_turnos.py` compacta uma vez, no turno 10. Um turno específico
    não é a propriedade; "qualquer turno, quantas vezes for" é.
    """
    controle = _projeto(tmp_path / "a")
    compactado = _projeto(tmp_path / "b")

    cartoes_controle = [_normalizar(_cartao(controle)) for _ in range(TURNOS)]

    cartoes_compactado = []
    for _ in range(TURNOS):
        _compactar(compactado)
        cartoes_compactado.append(_normalizar(_cartao(compactado)))

    assert cartoes_controle == cartoes_compactado
    assert cartoes_controle[0].strip(), "o cartão de controle veio vazio"


def test_compactacoes_seguidas_nao_degradam_o_estado(tmp_path):
    """Auto-compactação pode disparar em rajada. O estado tem de sair idêntico,
    exceto pelo carimbo que o próprio PreCompact grava."""
    raiz = _projeto(tmp_path)
    antes = estado.carregar_estrito(raiz)

    for _ in range(10):
        _compactar(raiz)

    depois = estado.carregar_estrito(raiz)

    assert depois["ciclo"] == antes["ciclo"]
    assert depois["fase"] == antes["fase"]
    assert depois["historico"] == antes["historico"]
    assert depois["ativo"] is True
    assert "ultima_consolidacao" in depois


def test_compactacao_no_meio_de_um_ciclo_preserva_a_fase(tmp_path):
    """A fase é o que o usuário perde se a durabilidade falhar. Compactar em cada
    fase do caminho não pode fazer o ciclo regredir."""
    raiz = _projeto(tmp_path)

    caminho_de_fases = ["ANALISE", "PLANO", "BUILD", "TESTE", "REVISAO", "DOC", "ENTREGA"]
    for destino in caminho_de_fases:
        _compactar(raiz)
        estado.atualizar(raiz, lambda atual, d=destino: estado.transicionar(atual, d))
        _compactar(raiz)

        assert estado.carregar(raiz)["fase"] == destino
        assert f"fase: {destino}".lower() in _cartao(raiz).lower()

    final = estado.carregar_estrito(raiz)
    assert final["fase"] == "ENTREGA"
    assert final["fases_concluidas"] == ["DESCOBERTA"] + caminho_de_fases[:-1]


def test_compactacao_interrompida_no_meio_nao_estraga_o_estado(tmp_path):
    """PreCompact morto no meio da escrita.

    A compactação não espera o hook para sempre, e a máquina pode cair. O estado
    tem de continuar legível: é a única memória que sobra depois que o contexto
    foi descartado. `gravar` troca o arquivo por `os.replace` num temporário
    próprio, então ou a escrita inteira aconteceu ou nenhuma parte dela.
    """
    raiz = _projeto(tmp_path)
    antes = estado.carregar_estrito(raiz)

    for _ in range(15):
        processo = subprocess.Popen(
            [sys.executable, str(HOOK_SALVAR)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(raiz),
        )
        processo.stdin.write(json.dumps({"cwd": str(raiz), "hook_event_name": "PreCompact"}))
        processo.stdin.close()
        processo.kill()
        processo.wait(timeout=60)

    depois = estado.carregar_estrito(raiz)  # levanta EstadoCorrompido se quebrou
    assert depois["ciclo"] == antes["ciclo"]
    assert depois["fase"] == antes["fase"]
    assert _cartao(raiz).strip(), "o cartão parou de ser injetado depois do PreCompact morto"

    sobras = list((raiz / ".engine").glob("estado.json.*.tmp"))
    assert not sobras, f"temporário de escrita ficou para trás: {sobras}"


def test_estado_desligado_continua_desligado_depois_da_compactacao(tmp_path):
    """A durabilidade vale nos dois sentidos: compactar não pode RESSUSCITAR um
    ciclo desligado, o que seria o motor reaparecendo sozinho no contexto."""
    raiz = _projeto(tmp_path)
    estado.desligar(raiz)

    for _ in range(3):
        _compactar(raiz)

    assert estado.carregar(raiz)["ativo"] is False
    assert _cartao(raiz) == ""


def test_compactacao_concorrente_com_outra_sessao_nao_perde_a_fase(tmp_path):
    """Onde os dois defeitos se encontram.

    O PreCompact é o pior lugar possível para um *lost update*: ele dispara
    exatamente quando o contexto vai ser descartado, então o que ele apagar do
    estado não sobra em lugar nenhum. Antes do cadeado, uma transição de fase feita
    por outra sessão entre o `carregar` e o `gravar` do PreCompact sumia no
    instante em que o disco virava a única memória do motor.
    """
    raiz = _projeto(tmp_path)

    compactacao = subprocess.Popen(
        [sys.executable, str(HOOK_SALVAR)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(raiz),
    )
    try:
        # A outra sessão avança a fase enquanto o PreCompact roda.
        estado.atualizar(raiz, lambda atual: estado.transicionar(atual, "ANALISE"))
        compactacao.stdin.write(json.dumps({"cwd": str(raiz), "hook_event_name": "PreCompact"}))
        compactacao.stdin.close()
        assert compactacao.wait(timeout=60) == 0
    finally:
        if compactacao.poll() is None:
            compactacao.kill()

    assert estado.carregar(raiz)["fase"] == "ANALISE", (
        "o PreCompact gravou por cima da transição de outra sessão"
    )
