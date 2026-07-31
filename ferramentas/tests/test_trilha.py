"""Testes de `ferramentas/trilha.py`: trilha append-only em `.engine/trilha.jsonl`."""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PLUGIN))

from ferramentas import trilha  # noqa: E402


def test_caminho_aponta_para_engine_trilha_jsonl(tmp_path):
    assert trilha.caminho(tmp_path) == tmp_path / ".engine" / "trilha.jsonl"


def test_registrar_cria_diretorio_e_grava_uma_linha(tmp_path):
    entrada = {
        "quando": "2026-07-30T10:00:00",
        "fase": "BUILD",
        "ferramenta": "Bash",
        "alvo": "pytest -q",
        "risco": "rastreado",
        "regra": "",
    }
    trilha.registrar(tmp_path, entrada)
    assert trilha.caminho(tmp_path).is_file()
    dados = trilha.ler(tmp_path)
    assert dados["linhas"] == [entrada]
    assert dados["_avisos"] == []


def test_registrar_faz_append_sem_apagar_linha_anterior(tmp_path):
    primeira = {"quando": "1", "fase": "BUILD", "ferramenta": "Bash", "alvo": "a", "risco": "livre", "regra": ""}
    segunda = {"quando": "2", "fase": "TESTE", "ferramenta": "Edit", "alvo": "b", "risco": "rastreado", "regra": ""}
    trilha.registrar(tmp_path, primeira)
    trilha.registrar(tmp_path, segunda)
    dados = trilha.ler(tmp_path)
    assert dados["linhas"] == [primeira, segunda]


def test_ler_arquivo_ausente_devolve_listas_vazias(tmp_path):
    dados = trilha.ler(tmp_path)
    assert dados == {"linhas": [], "_avisos": []}


def test_ler_pula_linha_corrompida_e_reporta_aviso(tmp_path):
    caminho = trilha.caminho(tmp_path)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    boa = {"quando": "1", "fase": "BUILD", "ferramenta": "Bash", "alvo": "a", "risco": "livre", "regra": ""}
    import json

    with caminho.open("w", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(boa, ensure_ascii=False) + "\n")
        arquivo.write("isso nao e json\n")
        arquivo.write("\n")  # linha vazia: ignorada silenciosamente, não é aviso

    dados = trilha.ler(tmp_path)
    assert dados["linhas"] == [boa]
    assert len(dados["_avisos"]) == 1
    assert "2" in dados["_avisos"][0]  # aponta o número da linha corrompida


def test_linha_corrompida_pre_existente_nao_impede_novo_append(tmp_path):
    caminho = trilha.caminho(tmp_path)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("isso nao e json\n", encoding="utf-8")

    nova = {"quando": "2", "fase": "TESTE", "ferramenta": "Edit", "alvo": "b", "risco": "rastreado", "regra": ""}
    trilha.registrar(tmp_path, nova)

    dados = trilha.ler(tmp_path)
    assert dados["linhas"] == [nova]
    assert len(dados["_avisos"]) == 1


def test_ler_linha_corrompida_que_nao_e_objeto_json_vira_aviso(tmp_path):
    caminho = trilha.caminho(tmp_path)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8") as arquivo:
        arquivo.write("[1, 2, 3]\n")  # JSON válido, mas não é objeto

    dados = trilha.ler(tmp_path)
    assert dados["linhas"] == []
    assert len(dados["_avisos"]) == 1


def test_registrar_nunca_propaga_excecao_com_diretorio_sem_permissao(tmp_path, monkeypatch):
    entrada = {"quando": "1", "fase": "BUILD", "ferramenta": "Bash", "alvo": "a", "risco": "livre", "regra": ""}

    def _mkdir_falha(self, *args, **kwargs):
        raise PermissionError("sem permissao")

    monkeypatch.setattr(Path, "mkdir", _mkdir_falha)
    # não deve levantar
    trilha.registrar(tmp_path, entrada)


def test_registrar_nunca_propaga_excecao_com_escrita_falhando(tmp_path, monkeypatch):
    entrada = {"quando": "1", "fase": "BUILD", "ferramenta": "Bash", "alvo": "a", "risco": "livre", "regra": ""}
    import builtins

    original_open = builtins.open

    def _open_falha(*args, **kwargs):
        if args and str(args[0]).endswith("trilha.jsonl"):
            raise OSError("disco cheio")
        return original_open(*args, **kwargs)

    monkeypatch.setattr(builtins, "open", _open_falha)
    trilha.registrar(tmp_path, entrada)
