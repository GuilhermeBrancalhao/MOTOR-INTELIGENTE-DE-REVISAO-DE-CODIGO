"""`programa abortar`: o verbo destrutivo que não tinha porta nenhuma.

O defeito, como estava
----------------------
`cli.py` fazia três linhas soltas — `novo = dict(dados)`, `novo["estado"] =
"CONCLUIDO"`, carimbo — e gravava. Nenhuma passava por `transicionar`. Quatro
consequências, e cada teste deste arquivo cobra uma:

1. **funcionava de qualquer estado**, inclusive de um programa já fechado, porque não
   havia grafo a consultar;
2. **gravava o desfecho errado**: "CONCLUIDO" é a palavra reservada para aceite de
   sistema verde e passou a nomear também a desistência — quem lesse o arquivo depois
   não teria como distinguir os dois;
3. **abria a porta de trás de `novo()`**, que libera a pasta quando o estado é
   CONCLUIDO: `abortar` seguido de `programa <objetivo>` descartava um plano-mestre
   aprovado na porta P1 sem a palavra "forçar" aparecer em lugar nenhum;
4. era o **único verbo destrutivo que não registrava na trilha**, apesar de a mensagem
   impressa afirmar, por escrito, que "a trilha e a decomposição ficam preservadas".

A decisão de desenho, e por que ela é esta
------------------------------------------
`ABORTADO` é um terminal PRÓPRIO, e **não** libera a pasta sozinho. A regra, escrita em
`programa.ESTADOS_QUE_LIBERAM_A_PASTA`: o motor abre um programa por cima do anterior
sem `--forcar` só quando o fim foi **verificado** — e `CONCLUIDO` só existe depois de um
aceite de sistema verde, que é veredito conferido pela máquina. `ABORTADO` é fim
**declarado**: alguém disse que acabou, e nada foi provado. Liberar por declaração daria
um segundo caminho, mais silencioso, para o que `--forcar` já faz em voz alta.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PLUGIN))

from ferramentas import programa, trilha  # noqa: E402

AGORA = "2026-08-05T10:00:00"
OBJETIVO = "construir um sistema novo que soma dois numeros"


def _plano(*ids_e_deps):
    return [
        {
            "id": cid,
            "objetivo": f"construir {cid}",
            "depende_de": list(deps),
            "aceite": f"pytest tests/{cid.lower()} -q sai 0",
        }
        for cid, deps in ids_e_deps
    ]


def _ate_execucao(tmp_path):
    dados = programa.novo(tmp_path, "sistema de teste", AGORA)
    dados = programa.propor_plano(
        dados, _plano(("C1", []), ("C2", ["C1"])), "o sistema sobe e responde"
    )
    return programa.aprovar(dados, AGORA)


def _cli(raiz: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(RAIZ_PLUGIN / "ferramentas" / "cli.py"), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )


# --------------------------------------------------------------------------
# 1. abortar passa pela máquina de estados
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "estado_do_programa", ["CONCEPCAO", "PLANO_MESTRE", "EXECUCAO", "DESVIO", "ACEITE_SISTEMA"]
)
def test_abortar_vale_de_todo_estado_vivo(tmp_path, estado_do_programa):
    """Desistir é legítimo em qualquer ponto vivo — o que não é legítimo é desistir por fora.

    Mutação alvo: esquecer a aresta para ABORTADO em algum estado do grafo. O verbo
    passaria a recusar num ponto em que abortar faz todo sentido, e o usuário voltaria a
    editar o JSON à mão.
    """
    dados = programa.novo(tmp_path, "sistema", AGORA)
    if estado_do_programa != "CONCEPCAO":
        dados = programa.propor_plano(dados, _plano(("C1", [])), "sobe e responde")
    if estado_do_programa in ("EXECUCAO", "DESVIO", "ACEITE_SISTEMA"):
        dados = programa.aprovar(dados, AGORA)
    if estado_do_programa == "DESVIO":
        dados = programa.desviar(dados, "aceite-inalcancavel", "não dá")
    if estado_do_programa == "ACEITE_SISTEMA":
        dados = programa.registrar_aceite(dados, "C1", passou=True)
        dados = programa.entrar_em_aceite(dados)
    assert dados["estado"] == estado_do_programa

    abortado = programa.abortar(dados, AGORA)

    assert abortado["estado"] == "ABORTADO"
    assert abortado["abortado_em"] == AGORA


def test_abortado_e_terminal_e_nao_e_concluido(tmp_path):
    """Mutação alvo: reusar CONCLUIDO como destino do abort.

    São desfechos diferentes: um foi verificado por um aceite de sistema, o outro foi
    declarado. Com um nome só, quem abre o arquivo seis meses depois não distingue os
    dois — e nem `novo()` distingue, que é como a porta de trás nascia.
    """
    assert programa.TRANSICOES["ABORTADO"] == ()
    assert "ABORTADO" in programa.TERMINAIS and "CONCLUIDO" in programa.TERMINAIS

    dados = _ate_execucao(tmp_path)
    abortado = programa.abortar(dados, AGORA)
    assert abortado["estado"] != "CONCLUIDO"

    with pytest.raises(programa.TransicaoInvalida):
        programa.transicionar(abortado, "EXECUCAO")


@pytest.mark.parametrize("terminal", ["CONCLUIDO", "ABORTADO"])
def test_abortar_um_programa_ja_terminado_e_recusado(tmp_path, terminal):
    """Mutação alvo: escrever o estado direto, sem consultar o grafo — como era antes.

    Abortar um CONCLUIDO reescreveria um desfecho verificado como desistência, que é
    perda de informação; abortar um ABORTADO só mexeria no carimbo. Nos dois casos não
    há o que encerrar, e recusar é mais útil do que obedecer.
    """
    dados = _ate_execucao(tmp_path)
    if terminal == "CONCLUIDO":
        for cid in ("C1", "C2"):
            dados = programa.registrar_aceite(dados, cid, passou=True)
        dados = programa.concluir(programa.entrar_em_aceite(dados), True, AGORA)
    else:
        dados = programa.abortar(dados, AGORA)
    assert dados["estado"] == terminal

    with pytest.raises(programa.TransicaoInvalida, match="já terminou"):
        programa.abortar(dados, AGORA)


def test_abortar_preserva_a_decomposicao(tmp_path):
    """Mutação alvo: limpar `ciclos` ao abortar.

    A mensagem impressa promete que a decomposição fica preservada, e a promessa tem de
    valer: ela é o registro do que se tinha planejado, e é o que permite reabrir o
    assunto depois sem redescobrir tudo.
    """
    dados = _ate_execucao(tmp_path)
    dados = programa.registrar_aceite(dados, "C1", passou=True)

    abortado = programa.abortar(dados, AGORA)

    por_id = {c["id"]: c["status"] for c in abortado["ciclos"]}
    assert por_id == {"C1": "CONCLUIDO", "C2": "PENDENTE"}
    assert abortado["aceite_de_sistema"] == "o sistema sobe e responde"


# --------------------------------------------------------------------------
# 2. a porta de trás de `novo()`
# --------------------------------------------------------------------------


def test_programa_novo_continua_recusando_por_cima_de_um_abortado(tmp_path):
    """A decisão de desenho, cobrada: fim DECLARADO não libera a pasta sozinho.

    Mutação alvo: pôr `ABORTADO` em `ESTADOS_QUE_LIBERAM_A_PASTA` (ou voltar a carimbar
    CONCLUIDO no abort). `abortar` + `programa <objetivo>` passaria a descartar um
    plano-mestre aprovado na porta P1 sem a palavra "forçar" em lugar nenhum — um
    segundo caminho, mais silencioso, para o que `--forcar` já faz em voz alta.
    """
    dados = _ate_execucao(tmp_path)
    programa.gravar(tmp_path, programa.abortar(dados, AGORA))

    with pytest.raises(programa.ProgramaJaAtivo, match="ABORTADO"):
        programa.novo(tmp_path, "outro sistema", AGORA)

    forcado = programa.novo(tmp_path, "outro sistema", AGORA, forcar=True)
    assert forcado["objetivo"] == "outro sistema"
    assert forcado["estado"] == "CONCEPCAO"


def test_programa_novo_segue_liberando_por_cima_de_um_concluido(tmp_path):
    """O par: fim VERIFICADO libera, e continua liberando.

    Mutação alvo: esvaziar `ESTADOS_QUE_LIBERAM_A_PASTA` por excesso de zelo. Um
    programa que chegou ao aceite de sistema verde acabou; exigir `--forcar` depois
    disso treinaria o usuário a digitar `--forcar` no automático, e aí a bandeira não
    protege mais nada.
    """
    dados = _ate_execucao(tmp_path)
    for cid in ("C1", "C2"):
        dados = programa.registrar_aceite(dados, cid, passou=True)
    programa.gravar(
        tmp_path, programa.concluir(programa.entrar_em_aceite(dados), True, AGORA)
    )

    seguinte = programa.novo(tmp_path, "o próximo sistema", AGORA)
    assert seguinte["objetivo"] == "o próximo sistema"


# --------------------------------------------------------------------------
# 3. pela CLI: trilha, código de saída, e o que a mensagem promete
# --------------------------------------------------------------------------


def _preparar_pela_cli(raiz: Path) -> None:
    """Programa em EXECUCAO, montado pela máquina e gravado — a CLI só aborta."""
    programa.gravar(raiz, _ate_execucao(raiz))


def test_abortar_pela_cli_registra_na_trilha(tmp_path):
    """Mutação alvo: omitir `_prog_trilha` no sub-verbo — como estava.

    Era o único verbo destrutivo sem linha na trilha, e ao mesmo tempo o único que
    imprimia a promessa de que a trilha ficava preservada. Sem o registro, o programa
    desaparecia do fluxo sem nada dizer quando, nem por qual comando.
    """
    _preparar_pela_cli(tmp_path)

    saida = _cli(tmp_path, "programa", "abortar")

    assert saida.returncode == 0, saida.stdout + saida.stderr
    acoes = [linha.get("alvo", "") for linha in trilha.ler(tmp_path)["linhas"]]
    assert any(a.startswith("programa-abortado") for a in acoes), acoes


def test_abortar_pela_cli_carimba_abortado_e_nao_concluido(tmp_path):
    """Mutação alvo: voltar a escrever `estado = "CONCLUIDO"` no dicionário.

    O teste olha o disco, não a mensagem: é o arquivo que sobrevive à sessão, e é dele
    que `novo()` tira a decisão de liberar ou não a pasta.
    """
    _preparar_pela_cli(tmp_path)

    saida = _cli(tmp_path, "programa", "abortar")

    assert programa.carregar(tmp_path)["estado"] == "ABORTADO"
    assert "ABORTADO" in saida.stdout


def test_a_cli_recusa_abortar_duas_vezes_sem_traceback(tmp_path):
    """Mutação alvo: deixar a `TransicaoInvalida` do segundo abort escapar como traceback.

    Nenhum verbo pode terminar em traceback — é a regra do topo do `cli.py`, e a skill
    lê esta saída para decidir o que reportar.
    """
    _preparar_pela_cli(tmp_path)
    assert _cli(tmp_path, "programa", "abortar").returncode == 0

    saida = _cli(tmp_path, "programa", "abortar")

    assert saida.returncode == 1
    assert "Traceback" not in saida.stdout + saida.stderr
    assert "já terminou" in saida.stdout


def test_a_cli_recusa_abrir_programa_por_cima_de_um_abortado(tmp_path):
    """A porta de trás, medida de ponta a ponta pela CLI.

    Mutação alvo: qualquer das duas — carimbar CONCLUIDO no abort, ou pôr ABORTADO
    entre os estados que liberam a pasta. Os dois reabrem o mesmo buraco, e este é o
    caminho de dois comandos que o usuário realmente digitaria.
    """
    _preparar_pela_cli(tmp_path)
    assert _cli(tmp_path, "programa", "abortar").returncode == 0

    saida = _cli(tmp_path, "programa", "outro sistema qualquer")

    assert saida.returncode == 1, saida.stdout
    assert "ABORTADO" in saida.stdout and "forcar" in saida.stdout
    assert programa.carregar(tmp_path)["objetivo"] == "sistema de teste"

    forcado = _cli(tmp_path, "programa", "outro sistema qualquer", "--forcar")
    assert forcado.returncode == 0, forcado.stdout
    assert programa.carregar(tmp_path)["objetivo"] == "outro sistema qualquer"


def test_o_status_de_um_abortado_nao_anuncia_proximo_ciclo(tmp_path):
    """Mutação alvo: manter o `elif r["proximo"]` valendo em qualquer estado.

    Os ciclos PENDENTE continuam no arquivo — é isso que preserva a decomposição —, e
    anunciá-los como "próximo elegível" convidaria a seguir executando um programa que
    foi encerrado.
    """
    _preparar_pela_cli(tmp_path)
    assert _cli(tmp_path, "programa", "abortar").returncode == 0

    saida = _cli(tmp_path, "programa", "status")

    assert saida.returncode == 0
    assert "Próximo ciclo elegível" not in saida.stdout
    assert "ABORTADO" in saida.stdout
