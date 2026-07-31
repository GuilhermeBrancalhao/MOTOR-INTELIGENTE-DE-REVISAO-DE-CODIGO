"""Testes da máquina de fases e da persistência do estado."""
import json

import pytest

from ferramentas import estado

AGORA = "2026-07-30T14:02:11"


def test_novo_ciclo_grava_em_disco_e_comeca_na_descoberta(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "somar dois numeros", AGORA)
    assert dados["ativo"] is True
    assert dados["fase"] == "DESCOBERTA"
    assert dados["ciclo"]["objetivo"] == "somar dois numeros"
    assert dados["ciclo"]["iniciado_em"] == AGORA
    gravado = json.loads(estado.caminho(tmp_path).read_text(encoding="utf-8"))
    assert gravado == dados


def test_carregar_sem_estado_devolve_none(tmp_path):
    assert estado.carregar(tmp_path) is None


def test_transicao_valida_avanca_e_registra(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "x", AGORA)
    dados = estado.transicionar(dados, "ANALISE")
    assert dados["fase"] == "ANALISE"
    assert dados["fases_concluidas"] == ["DESCOBERTA"]


def test_transicao_invalida_levanta(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "x", AGORA)
    with pytest.raises(estado.TransicaoInvalida):
        estado.transicionar(dados, "ENTREGA")


def test_teste_volta_para_build(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "x", AGORA)
    for destino in ("ANALISE", "PLANO", "BUILD", "TESTE"):
        dados = estado.transicionar(dados, destino)
    dados = estado.transicionar(dados, "BUILD")
    assert dados["fase"] == "BUILD"


def test_todas_as_fases_do_grafo_sao_alcancaveis():
    alcancadas = {"DESCOBERTA"}
    fronteira = ["DESCOBERTA"]
    while fronteira:
        atual = fronteira.pop()
        for destino in estado.TRANSICOES[atual]:
            if destino not in alcancadas:
                alcancadas.add(destino)
                fronteira.append(destino)
    assert alcancadas == set(estado.FASES)


def test_desligar_preserva_o_ciclo(tmp_path):
    estado.novo_ciclo(tmp_path, "x", AGORA)
    dados = estado.desligar(tmp_path)
    assert dados["ativo"] is False
    assert dados["ciclo"]["objetivo"] == "x"


def test_registrar_diff_nao_duplica(tmp_path):
    estado.novo_ciclo(tmp_path, "x", AGORA)
    estado.registrar_diff(tmp_path, "app/servico.py")
    dados = estado.registrar_diff(tmp_path, "app/servico.py")
    assert dados["diffs_pendentes"] == ["app/servico.py"]


def test_gravacao_e_atomica(tmp_path):
    """Não pode sobrar arquivo temporário depois de gravar."""
    estado.novo_ciclo(tmp_path, "x", AGORA)
    restos = list((tmp_path / ".engine").glob("*.tmp"))
    assert restos == []
