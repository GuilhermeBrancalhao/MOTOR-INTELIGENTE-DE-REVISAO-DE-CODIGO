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


def test_gravacao_e_atomica(tmp_path, monkeypatch):
    """Se `os.replace` falhar no meio da escrita, o arquivo antigo continua intacto.

    Só checar que não sobra `*.tmp` passaria mesmo com uma escrita direta no alvo;
    o que a atomicidade compra é isto: uma falha no `replace` nunca corrompe (nem
    apaga) o que já estava gravado.
    """
    estado.novo_ciclo(tmp_path, "x", AGORA)
    alvo = estado.caminho(tmp_path)
    conteudo_antigo = alvo.read_text(encoding="utf-8")

    def replace_quebrado(origem, destino):
        raise OSError("falha simulada no os.replace")

    monkeypatch.setattr(estado.os, "replace", replace_quebrado)

    with pytest.raises(OSError):
        estado.gravar(tmp_path, {"ativo": False, "marca": "nao deveria persistir"})

    assert alvo.read_text(encoding="utf-8") == conteudo_antigo


def test_desligar_sobre_estado_corrompido_preserva_original(tmp_path):
    pasta = tmp_path / ".engine"
    pasta.mkdir()
    alvo = estado.caminho(tmp_path)
    conteudo_quebrado = "{isso nao e json valido"
    alvo.write_text(conteudo_quebrado, encoding="utf-8")

    dados = estado.desligar(tmp_path, agora="20260730140211")

    assert dados["ativo"] is False
    preservado = pasta / "estado.corrompido-20260730140211.json"
    assert preservado.is_file()
    assert preservado.read_text(encoding="utf-8") == conteudo_quebrado
    assert alvo.is_file()
    novo_conteudo = json.loads(alvo.read_text(encoding="utf-8"))
    assert novo_conteudo["ativo"] is False


def test_registrar_diff_sobre_estado_corrompido_levanta(tmp_path):
    pasta = tmp_path / ".engine"
    pasta.mkdir()
    estado.caminho(tmp_path).write_text("{isso nao e json valido", encoding="utf-8")

    with pytest.raises(estado.EstadoCorrompido):
        estado.registrar_diff(tmp_path, "app/servico.py")


def test_novo_ciclo_sobre_ciclo_ativo_levanta(tmp_path):
    estado.novo_ciclo(tmp_path, "primeiro objetivo", AGORA)
    with pytest.raises(estado.CicloJaAtivo):
        estado.novo_ciclo(tmp_path, "segundo objetivo", AGORA)


def test_novo_ciclo_com_forcar_sobrescreve_ciclo_ativo(tmp_path):
    estado.novo_ciclo(tmp_path, "primeiro objetivo", AGORA)
    dados = estado.novo_ciclo(tmp_path, "segundo objetivo", AGORA, forcar=True)
    assert dados["ciclo"]["objetivo"] == "segundo objetivo"
    assert dados["ativo"] is True


def test_novo_ciclo_dois_no_mesmo_dia_recebem_ids_diferentes(tmp_path):
    primeiro = estado.novo_ciclo(tmp_path, "primeiro objetivo", AGORA)
    estado.desligar(tmp_path)
    segundo = estado.novo_ciclo(tmp_path, "segundo objetivo", AGORA)

    assert primeiro["ciclo"]["id"] == "2026-07-30-1"
    assert segundo["ciclo"]["id"] == "2026-07-30-2"
    assert segundo["historico"] == ["2026-07-30-1", "2026-07-30-2"]
