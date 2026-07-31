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


# --- Revisão adversarial, CRÍTICO 2: segredo nunca chega ao disco em claro ------
#
# Os dois comandos abaixo são os que o revisor verificou por execução: ambos são
# `rastreado` (executam, não travam) e iam literais para a trilha, de onde o
# relatório de fase e o verbo `retomar` os traziam de volta para o contexto.


def _entrada(alvo: str) -> dict:
    return {
        "quando": "2026-07-31T10:00:00",
        "fase": "BUILD",
        "ferramenta": "Bash",
        "alvo": alvo,
        "risco": "rastreado",
        "regra": "",
    }


def test_registrar_redige_senha_embutida_em_url(tmp_path):
    comando = 'psql "postgresql://admin:S3nh4Secreta@db.prod:5432/app"'
    trilha.registrar(tmp_path, _entrada(comando))

    bruto = trilha.caminho(tmp_path).read_text(encoding="utf-8")
    assert "S3nh4Secreta" not in bruto
    assert trilha.MARCA_REDIGIDO in bruto
    # O que não é segredo continua legível: sem isso a trilha perde utilidade.
    assert "admin" in bruto
    assert "db.prod" in bruto


def test_registrar_redige_valor_do_cabecalho_authorization(tmp_path):
    segredo = "sk-proj-ABCdefGHIjklMNOpqrs1234567890"
    comando = f'curl -H "Authorization: Bearer {segredo}" https://api.exemplo/v1/x'
    trilha.registrar(tmp_path, _entrada(comando))

    bruto = trilha.caminho(tmp_path).read_text(encoding="utf-8")
    assert segredo not in bruto
    assert "Bearer" not in bruto
    assert trilha.MARCA_REDIGIDO in bruto
    assert "curl" in bruto
    assert "https://api.exemplo/v1/x" in bruto


def test_redigir_cobre_os_padroes_de_chave_conhecida_do_modulo_de_risco():
    casos = [
        "AKIA1234567890ABCDEF",
        "ghp_abcdefghijklmnopqrstuvwxyz0123",
        "github_pat_abcdefghijklmnopqrstuvwxyz0123456789",
        "xoxb-1234567890-abcdefghij",
        "-----BEGIN RSA PRIVATE KEY-----",
    ]
    for segredo in casos:
        redigido = trilha.redigir(f"echo {segredo} >> saida.txt")
        assert segredo not in redigido, f"não redigiu {segredo!r}"
        assert trilha.MARCA_REDIGIDO in redigido


def test_redigir_nao_mexe_em_comando_sem_credencial():
    comando = "python -m pytest ferramentas/tests -q"
    assert trilha.redigir(comando) == comando


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
