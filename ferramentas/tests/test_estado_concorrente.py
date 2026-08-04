"""Colisão entre sessões no `.engine/estado.json` — o arquivo único.

O defeito, medido antes da correção
-----------------------------------
`.engine/estado.json` é um arquivo só, e o Claude Code pode ter mais de uma sessão
aberta na mesma pasta. Toda mutação do motor era **ler → alterar → gravar** em três
passos soltos. Duas sessões fazendo isso ao mesmo tempo produziam *lost update*: a
segunda lia antes de a primeira gravar, e a gravação da segunda apagava o que a
primeira tinha acabado de escrever.

Não era corrupção — `gravar` sempre foi atômico (`os.replace`). Era pior: o estado
final era JSON perfeitamente válido, só que sem a transição de fase que a CLI já
tinha confirmado ao usuário na tela. `CLAUDE.md` registrava isso como armadilha
conhecida com a instrução "não ligar o motor em pasta com mais de uma sessão
aberta" — um contorno humano, não uma trava.

Os testes deste módulo usam **subprocessos de verdade**, não threads. A exclusão
mútua é entre processos (o Claude Code roda cada hook como um processo novo), e
threads sob o GIL mascarariam a corrida que precisa ser reproduzida.
"""
from __future__ import annotations

import json
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import pytest

from ferramentas import estado

RAIZ_DO_MOTOR = Path(__file__).resolve().parent.parent.parent

#: Quantos processos disputam o estado ao mesmo tempo.
CONCORRENTES = 6

#: Quanto tempo cada mutador segura a seção crítica. É este atraso que transforma a
#: corrida de "provável" em "certa": sem cadeado, os seis leem o mesmo estado antes
#: de qualquer um gravar, e cinco contribuições se perdem. Sob cadeado, os seis
#: passam em fila e o custo total é ~6x este valor.
ATRASO_NA_SECAO_CRITICA = 0.05


_TRABALHADOR = textwrap.dedent(
    """
    import sys, time
    from pathlib import Path

    sys.path.insert(0, {raiz!r})
    from ferramentas import estado

    raiz = Path(sys.argv[1])
    marca = sys.argv[2]
    partida = float(sys.argv[3])
    atraso = float(sys.argv[4])

    # Todos os processos comecam a disputar no MESMO instante de relogio de parede.
    # Sem esta barreira o custo de arranque do interpretador (dezenas de ms, e
    # diferente a cada processo) espalharia as tentativas e a corrida nao
    # aconteceria nem sem cadeado -- o teste passaria por acidente.
    while time.time() < partida:
        time.sleep(0.001)

    def mutar(atual):
        if atual is None:
            atual = {{"marcas": []}}
        marcas = list(atual.get("marcas", []))
        time.sleep(atraso)          # a janela entre ler e gravar
        marcas.append(marca)
        atual["marcas"] = marcas
        return atual

    try:
        estado.atualizar(raiz, mutar, espera=30.0)
    except Exception as erro:
        print(f"{{type(erro).__name__}}: {{erro}}", file=sys.stderr)
        raise SystemExit(1)
    """
)


def _disparar(raiz: Path, quantos: int, atraso: float) -> list[subprocess.CompletedProcess]:
    script = raiz / "_trabalhador.py"
    script.write_text(_TRABALHADOR.format(raiz=str(RAIZ_DO_MOTOR)), encoding="utf-8")

    partida = time.time() + 1.0
    processos = [
        subprocess.Popen(
            [sys.executable, str(script), str(raiz), f"m{n}", str(partida), str(atraso)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        for n in range(quantos)
    ]
    resultados = []
    for processo in processos:
        saida, erro = processo.communicate(timeout=120)
        resultados.append(
            subprocess.CompletedProcess(processo.args, processo.returncode, saida, erro)
        )
    return resultados


# --------------------------------------------------------------------------
# A corrida
# --------------------------------------------------------------------------


def test_seis_sessoes_simultaneas_nao_perdem_escrita(tmp_path):
    """Nenhuma contribuição some quando seis processos mutam o estado juntos.

    Este é o teste que reproduz o defeito. Trocar `estado.atualizar` por
    `carregar` + mutação + `gravar` no trabalhador faz ele reprovar com uma ou
    duas marcas em vez de seis.
    """
    estado.gravar(tmp_path, {"ativo": True, "marcas": []})

    resultados = _disparar(tmp_path, CONCORRENTES, ATRASO_NA_SECAO_CRITICA)

    falhas = [r for r in resultados if r.returncode != 0]
    assert not falhas, "processo concorrente falhou: " + "; ".join(
        r.stderr.strip() for r in falhas
    )

    final = json.loads(estado.caminho(tmp_path).read_text(encoding="utf-8"))
    assert sorted(final["marcas"]) == [f"m{n}" for n in range(CONCORRENTES)], (
        "escrita perdida: o estado final tem "
        f"{len(final['marcas'])} das {CONCORRENTES} contribuições"
    )


def test_estado_continua_json_valido_sob_concorrencia(tmp_path):
    """O arquivo nunca é observado pela metade — `gravar` troca, não reescreve.

    Esta propriedade já existia (`os.replace`) e continua valendo: o cadeado é
    sobre PERDA de escrita, não sobre corrupção. O teste está aqui para que uma
    troca futura da escrita atômica por escrita direta não passe despercebida.
    """
    estado.gravar(tmp_path, {"ativo": True, "marcas": []})
    _disparar(tmp_path, CONCORRENTES, ATRASO_NA_SECAO_CRITICA)

    dados = estado.carregar_estrito(tmp_path)
    assert isinstance(dados, dict)
    assert dados["ativo"] is True


# --------------------------------------------------------------------------
# O cadeado em si
# --------------------------------------------------------------------------


def test_cadeado_e_exclusivo(tmp_path):
    with estado.cadeado(tmp_path):
        with pytest.raises(estado.EstadoOcupado):
            with estado.cadeado(tmp_path, espera=0.05):
                pytest.fail("dois cadeados ao mesmo tempo sobre a mesma raiz")


def test_cadeado_e_solto_mesmo_com_excecao(tmp_path):
    """Cadeado preso por erro travaria o motor naquele projeto até alguém apagar
    o arquivo à mão — modo de falhar pior do que a corrida que ele previne."""
    with pytest.raises(ValueError):
        with estado.cadeado(tmp_path):
            raise ValueError("erro dentro da seção crítica")

    assert not estado.caminho_cadeado(tmp_path).exists()
    with estado.cadeado(tmp_path, espera=0.05):
        pass


def test_cadeado_abandonado_e_quebrado_por_idade(tmp_path):
    """Dono morto sem soltar (sessão fechada no meio, processo morto).

    Sem a quebra por idade, o cadeado órfão travaria o motor para sempre naquela
    pasta — e o usuário não teria como saber que o conserto é apagar um arquivo
    dentro de `.engine/`, que o próprio classificador de risco protege (R9).
    """
    alvo = estado.caminho_cadeado(tmp_path)
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_text("99999\n", encoding="utf-8")

    with pytest.raises(estado.EstadoOcupado):
        with estado.cadeado(tmp_path, espera=0.05, idade_maxima=3600):
            pytest.fail("cadeado recente não pode ser quebrado")

    with estado.cadeado(tmp_path, espera=0.05, idade_maxima=-1):
        pass  # tratado como abandonado, quebrado, e retomado


def test_quebrar_cadeado_abandonado_da_direito_a_tentativa_imediata(tmp_path):
    """Quebrar e mesmo assim desistir deixa o caminho livre para o próximo, não para si.

    A quebra por idade acontecia e logo em seguida a checagem de prazo derrubava
    quem quebrou. Com `espera=0` — prazo já vencido na primeira volta do laço — o
    resultado era `EstadoOcupado` levantado contra um cadeado que este mesmo
    processo tinha acabado de apagar: o erro reportava ocupação que não existia
    mais, e o benefício da quebra ia para o processo seguinte.
    """
    alvo = estado.caminho_cadeado(tmp_path)
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_text("99999\n", encoding="utf-8")

    with estado.cadeado(tmp_path, espera=0, idade_maxima=-1):
        assert alvo.exists(), "o cadeado precisa estar em minhas mãos aqui dentro"

    assert not alvo.exists(), "o cadeado precisa ser solto na saída"


def test_atualizar_nao_grava_quando_o_mutador_devolve_none(tmp_path):
    estado.gravar(tmp_path, {"ativo": True, "marca": "original"})

    assert estado.atualizar(tmp_path, lambda _atual: None) is None

    assert estado.carregar(tmp_path)["marca"] == "original"
    assert not estado.caminho_cadeado(tmp_path).exists()


def test_atualizar_ve_o_disco_e_nao_o_que_quem_chamou_leu(tmp_path):
    """O coração da correção: o mutador recebe o estado relido DE DENTRO do cadeado.

    Se `atualizar` aceitasse um dicionário lido antes, o cadeado seria decorativo —
    serializaria as gravações e mesmo assim perderia escrita.
    """
    estado.gravar(tmp_path, {"ativo": True, "contador": 0})
    lido_antes = estado.carregar(tmp_path)

    estado.gravar(tmp_path, {"ativo": True, "contador": 7})  # outra sessão escreveu

    vistos: list[int] = []

    def _mutar(atual):
        vistos.append(atual["contador"])
        atual["contador"] += 1
        return atual

    estado.atualizar(tmp_path, _mutar)

    assert lido_antes["contador"] == 0
    assert vistos == [7], "o mutador viu um estado velho em vez do que está no disco"
    assert estado.carregar(tmp_path)["contador"] == 8


# --------------------------------------------------------------------------
# A trava contra reintrodução
# --------------------------------------------------------------------------

#: `estado.py` é a casa do cadeado e chama `gravar` por dentro; os testes montam
#: cenário e podem gravar direto.
_PODEM_GRAVAR_DIRETO = {"estado.py"}


def test_nenhum_gravar_fora_do_estado():
    """Mutação de estado passa por `atualizar`, nunca por `gravar` solto.

    `gravar` continua público porque testes e ferramentas de montagem precisam
    dele, mas em código de produção ele é a metade insegura da operação: grava sem
    reler, que é exatamente o *lost update*. Esta trava existe porque a correção
    de 2026-08-04 teve de encontrar os cinco sítios um a um (`cli.py` em dois
    lugares, `engine_gate.py`, `engine_salvar.py`, `estado.registrar_diff`) — o
    sexto que alguém acrescentar tem que aparecer sozinho.
    """
    producao = [
        arquivo
        for pasta in ("ferramentas", "hooks")
        for arquivo in (RAIZ_DO_MOTOR / pasta).glob("*.py")
        if arquivo.name not in _PODEM_GRAVAR_DIRETO
    ]
    assert producao, "esperava encontrar módulos de produção para inspecionar"

    culpados = [
        arquivo.name
        for arquivo in producao
        if "estado.gravar(" in arquivo.read_text(encoding="utf-8", errors="ignore")
    ]

    assert not culpados, (
        "módulo de produção gravando estado sem cadeado (use `estado.atualizar`): "
        + ", ".join(culpados)
    )
