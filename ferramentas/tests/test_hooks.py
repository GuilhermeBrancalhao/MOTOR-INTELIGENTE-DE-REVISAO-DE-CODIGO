"""Testes dos hooks: entrada JSON no stdin, decisão pelo código de saída."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
HOOK_RISCO = RAIZ_PLUGIN / "hooks" / "engine_risco.py"
HOOK_CONTEXTO = RAIZ_PLUGIN / "hooks" / "engine_contexto.py"
HOOK_TRILHA = RAIZ_PLUGIN / "hooks" / "engine_trilha.py"

sys.path.insert(0, str(RAIZ_PLUGIN))
from ferramentas import estado, trilha  # noqa: E402


def _rodar(hook: Path, payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(hook)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env={**os.environ},
    )


def _rodar_stdin_cru(hook: Path, stdin_cru: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(hook)],
        input=stdin_cru,
        capture_output=True,
        text=True,
        cwd=str(cwd),
        env={**os.environ},
    )


def _ligar(raiz: Path) -> None:
    estado.novo_ciclo(raiz, "teste", "2026-07-30T00:00:00")


def _ligar_modo_seco(raiz: Path) -> None:
    estado.novo_ciclo(raiz, "teste", "2026-07-30T00:00:00", modo="dry")


def test_motor_desligado_nao_bloqueia_nada(tmp_path):
    saida = _rodar(
        HOOK_RISCO,
        {"tool_name": "Bash", "tool_input": {"command": "rm -rf x"}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0


def test_acao_travada_bloqueia_com_motivo(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(
        HOOK_RISCO,
        {
            "tool_name": "Bash",
            "tool_input": {"command": "git push origin main"},
            "cwd": str(tmp_path),
        },
        tmp_path,
    )
    assert saida.returncode == 2
    assert "R2" in saida.stderr


def test_acao_livre_passa(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(
        HOOK_RISCO,
        {"tool_name": "Bash", "tool_input": {"command": "pytest -q"}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0


def test_acao_rastreada_passa_e_registra_o_diff(tmp_path):
    _ligar(tmp_path)
    alvo = tmp_path / "servico.py"
    alvo.write_text("x = 1", encoding="utf-8")
    saida = _rodar(
        HOOK_RISCO,
        {"tool_name": "Edit", "tool_input": {"file_path": str(alvo)}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0
    dados = estado.carregar(tmp_path)
    assert str(alvo) in dados["diffs_pendentes"]


def test_stdin_invalido_bloqueia(tmp_path):
    _ligar(tmp_path)
    saida = subprocess.run(
        [sys.executable, str(HOOK_RISCO)],
        input="isso nao e json",
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
    )
    assert saida.returncode == 2


# --- IMPORTANTE 3: o modo seco tem que bloquear escrita e liberar leitura --------


def test_modo_seco_bloqueia_escrita_em_arquivo_novo(tmp_path):
    _ligar_modo_seco(tmp_path)
    alvo = tmp_path / "novo_arquivo.py"
    saida = _rodar(
        HOOK_RISCO,
        {"tool_name": "Write", "tool_input": {"file_path": str(alvo)}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 2
    assert "seco" in saida.stderr


def test_modo_seco_libera_leitura(tmp_path):
    _ligar_modo_seco(tmp_path)
    alvo = tmp_path / "comum.py"
    alvo.write_text("x = 1", encoding="utf-8")
    saida = _rodar(
        HOOK_RISCO,
        {"tool_name": "Read", "tool_input": {"file_path": str(alvo)}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0


# --- IMPORTANTE 4: cwd num subdiretório do projeto ainda acha o estado -----------


def test_cwd_em_subdiretorio_ainda_encontra_estado_e_bloqueia(tmp_path):
    _ligar(tmp_path)
    subdiretorio = tmp_path / "pacote" / "subpacote"
    subdiretorio.mkdir(parents=True)
    saida = _rodar(
        HOOK_RISCO,
        {
            "tool_name": "Bash",
            "tool_input": {"command": "git push origin main"},
            "cwd": str(subdiretorio),
        },
        tmp_path,
    )
    assert saida.returncode == 2
    assert "R2" in saida.stderr


# --- CRÍTICO 1: nenhuma entrada malformada pode sair com código != 0 e != 2 ------


@pytest.mark.parametrize(
    "payload_json",
    [
        "null",
        "[]",
        '"texto"',
        "{}",
        '{"cwd": 5}',
        '{"tool_name": "X", "tool_input": "texto em vez de objeto"}',
        "",
        '{"tool_name":',  # JSON truncado
    ],
)
def test_evento_malformado_nunca_sai_1_sempre_2(tmp_path, payload_json):
    _ligar(tmp_path)  # motor LIGADO: é o caminho que mais exercita o código
    saida = _rodar_stdin_cru(HOOK_RISCO, payload_json, tmp_path)
    assert saida.returncode == 2
    assert saida.returncode != 1


# --- Hook UserPromptSubmit: o cartão de estado ------------------------------------


def _importar_contexto():
    sys.path.insert(0, str(RAIZ_PLUGIN / "hooks"))
    import engine_contexto

    return engine_contexto


def test_motor_desligado_nao_injeta_nada(tmp_path):
    saida = _rodar(HOOK_CONTEXTO, {"cwd": str(tmp_path)}, tmp_path)
    assert saida.returncode == 0
    assert saida.stdout.strip() == ""


def test_cartao_traz_fase_objetivo_e_invariantes(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(HOOK_CONTEXTO, {"cwd": str(tmp_path)}, tmp_path)
    assert saida.returncode == 0
    assert "DESCOBERTA" in saida.stdout
    assert "teste" in saida.stdout
    assert "Nunca afirmar sucesso sem ter olhado" in saida.stdout


def test_cartao_respeita_o_teto_de_linhas():
    from ferramentas import config

    contexto = _importar_contexto()
    cfg = dict(config.PADRAO)
    dados = {
        "ativo": True,
        "fase": "BUILD",
        "ciclo": {"objetivo": "o" * 400, "modo": "normal"},
        "cartoes": [f"cartao-{i}" for i in range(50)],
        "decisoes": [{"o_que": f"decisao {i}", "porque": "motivo"} for i in range(50)],
        "diffs_pendentes": [f"arquivo_{i}.py" for i in range(50)],
        "pendencias": [],
    }
    cartao = contexto.montar_cartao(dados, cfg)
    assert len(cartao.splitlines()) <= cfg["teto_cartao_linhas"]


def test_cwd_em_subdiretorio_ainda_encontra_o_cartao(tmp_path):
    _ligar(tmp_path)
    subdiretorio = tmp_path / "pacote" / "subpacote"
    subdiretorio.mkdir(parents=True)
    saida = _rodar(HOOK_CONTEXTO, {"cwd": str(subdiretorio)}, tmp_path)
    assert saida.returncode == 0
    assert "DESCOBERTA" in saida.stdout


def test_evento_malformado_nao_injeta_nada_e_nao_bloqueia(tmp_path):
    _ligar(tmp_path)
    saida = _rodar_stdin_cru(HOOK_CONTEXTO, "isso nao e json", tmp_path)
    assert saida.returncode == 0
    assert saida.stdout.strip() == ""


def test_avisos_de_config_tambem_respeitam_o_teto():
    contexto = _importar_contexto()
    cfg = {"teto_cartao_linhas": 5, "_avisos": [f"aviso {i}" for i in range(50)]}
    cartao = contexto._com_avisos("linha 1\nlinha 2\nlinha 3", cfg)
    assert len(cartao.splitlines()) <= cfg["teto_cartao_linhas"]


# --- Correção: piso do teto do cartão garante cabeçalho e invariantes ------------
#
# `linhas[:teto]` com `teto` negativo remove as últimas N linhas em vez de
# limitar a N; e mesmo um teto pequeno positivo (< 9) cortava cabeçalho e/ou
# rodapé antes da correção. O piso `MINIMO_CARTAO = 9` (3 de cabeçalho + 6 de
# rodapé) garante que fase, objetivo e os cinco invariantes sempre cabem.


@pytest.mark.parametrize("teto", [0, -5, 3])
def test_teto_abaixo_do_piso_produz_cartao_com_exatamente_9_linhas(teto):
    from ferramentas import config

    contexto = _importar_contexto()
    cfg = dict(config.PADRAO)
    cfg["teto_cartao_linhas"] = teto
    dados = {
        "ativo": True,
        "fase": "DESCOBERTA",
        "ciclo": {"objetivo": "objetivo do ciclo", "modo": "normal"},
        "cartoes": [],
        "decisoes": [{"o_que": f"decisao {i}", "porque": "motivo"} for i in range(50)],
        "diffs_pendentes": [],
        "pendencias": [],
    }
    cartao = contexto.montar_cartao(dados, cfg)
    linhas = cartao.splitlines()
    assert len(linhas) == 9
    assert "DESCOBERTA" in cartao
    assert "objetivo do ciclo" in cartao
    for invariante in contexto.INVARIANTES:
        assert invariante in cartao


def test_teto_nao_numerico_cai_no_default_sem_levantar_excecao():
    from ferramentas import config

    contexto = _importar_contexto()
    cfg = dict(config.PADRAO)
    cfg["teto_cartao_linhas"] = "quarenta"
    dados = {
        "ativo": True,
        "fase": "BUILD",
        "ciclo": {"objetivo": "objetivo qualquer", "modo": "normal"},
        "cartoes": [],
        "decisoes": [],
        "diffs_pendentes": [],
        "pendencias": [],
    }
    cartao = contexto.montar_cartao(dados, cfg)
    assert len(cartao.splitlines()) <= 40
    for invariante in contexto.INVARIANTES:
        assert invariante in cartao


def test_teto_12_com_muitas_decisoes_e_diffs_mantem_os_cinco_invariantes():
    from ferramentas import config

    contexto = _importar_contexto()
    cfg = dict(config.PADRAO)
    cfg["teto_cartao_linhas"] = 12
    dados = {
        "ativo": True,
        "fase": "BUILD",
        "ciclo": {"objetivo": "objetivo qualquer", "modo": "normal"},
        "cartoes": [],
        "decisoes": [{"o_que": f"decisao {i}", "porque": "motivo"} for i in range(50)],
        "diffs_pendentes": [f"arquivo_{i}.py" for i in range(50)],
        "pendencias": [],
    }
    cartao = contexto.montar_cartao(dados, cfg)
    linhas = cartao.splitlines()
    assert len(linhas) <= 12
    for invariante in contexto.INVARIANTES:
        assert invariante in cartao


# --- Hook PostToolUse: a trilha auditável ----------------------------------------


def test_trilha_motor_ligado_gera_linha_com_os_seis_campos(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(
        HOOK_TRILHA,
        {
            "tool_name": "Bash",
            "tool_input": {"command": "pytest -q"},
            "cwd": str(tmp_path),
        },
        tmp_path,
    )
    assert saida.returncode == 0
    dados = trilha.ler(tmp_path)
    assert dados["_avisos"] == []
    assert len(dados["linhas"]) == 1
    linha = dados["linhas"][0]
    assert set(linha.keys()) == {"quando", "fase", "ferramenta", "alvo", "risco", "regra"}
    assert linha["fase"] == "DESCOBERTA"
    assert linha["ferramenta"] == "Bash"
    assert linha["alvo"] == "pytest -q"
    assert linha["risco"] == "rastreado"


def test_trilha_motor_desligado_nao_gera_nada(tmp_path):
    saida = _rodar(
        HOOK_TRILHA,
        {"tool_name": "Bash", "tool_input": {"command": "pytest -q"}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0
    assert not trilha.caminho(tmp_path).is_file()


def test_trilha_reclassifica_acao_travada_e_registra_a_regra(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(
        HOOK_TRILHA,
        {
            "tool_name": "Bash",
            "tool_input": {"command": "git push origin main"},
            "cwd": str(tmp_path),
        },
        tmp_path,
    )
    assert saida.returncode == 0
    dados = trilha.ler(tmp_path)
    linha = dados["linhas"][0]
    assert linha["risco"] == "travado"
    assert linha["regra"] == "R2"


def test_trilha_registra_alvo_de_ferramenta_de_arquivo(tmp_path):
    _ligar(tmp_path)
    alvo = tmp_path / "servico.py"
    saida = _rodar(
        HOOK_TRILHA,
        {"tool_name": "Write", "tool_input": {"file_path": str(alvo)}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0
    dados = trilha.ler(tmp_path)
    assert dados["linhas"][0]["alvo"] == str(alvo)


def test_trilha_linha_corrompida_pre_existente_nao_impede_append_e_ler_avisa(tmp_path):
    _ligar(tmp_path)
    caminho_trilha = trilha.caminho(tmp_path)
    caminho_trilha.parent.mkdir(parents=True, exist_ok=True)
    caminho_trilha.write_text("isso nao e json\n", encoding="utf-8")

    saida = _rodar(
        HOOK_TRILHA,
        {"tool_name": "Bash", "tool_input": {"command": "pytest -q"}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0

    dados = trilha.ler(tmp_path)
    assert len(dados["linhas"]) == 1
    assert len(dados["_avisos"]) == 1


def test_trilha_stdin_malformado_sai_0(tmp_path):
    _ligar(tmp_path)
    saida = _rodar_stdin_cru(HOOK_TRILHA, "isso nao e json", tmp_path)
    assert saida.returncode == 0
    assert not trilha.caminho(tmp_path).is_file()


def test_trilha_evento_sem_tool_name_sai_0_sem_gravar(tmp_path):
    _ligar(tmp_path)
    saida = _rodar(HOOK_TRILHA, {"cwd": str(tmp_path)}, tmp_path)
    assert saida.returncode == 0
    assert not trilha.caminho(tmp_path).is_file()


def test_trilha_cwd_em_subdiretorio_ainda_encontra_o_estado(tmp_path):
    _ligar(tmp_path)
    subdiretorio = tmp_path / "pacote" / "subpacote"
    subdiretorio.mkdir(parents=True)
    saida = _rodar(
        HOOK_TRILHA,
        {"tool_name": "Bash", "tool_input": {"command": "pytest -q"}, "cwd": str(subdiretorio)},
        tmp_path,
    )
    assert saida.returncode == 0
    dados = trilha.ler(tmp_path)
    assert len(dados["linhas"]) == 1


def test_avisos_com_teto_apertado_e_muitas_decisoes_fica_dentro_do_teto():
    contexto = _importar_contexto()
    cfg = {"teto_cartao_linhas": 3, "_avisos": [f"aviso {i}" for i in range(50)]}
    dados = {
        "ativo": True,
        "fase": "DESCOBERTA",
        "ciclo": {"objetivo": "objetivo qualquer", "modo": "normal"},
        "cartoes": [],
        "decisoes": [{"o_que": f"decisao {i}", "porque": "motivo"} for i in range(50)],
        "diffs_pendentes": [f"arquivo_{i}.py" for i in range(50)],
        "pendencias": [],
    }
    cartao = contexto.montar_cartao(dados, cfg)
    cartao = contexto._com_avisos(cartao, cfg)
    assert len(cartao.splitlines()) <= cfg["teto_cartao_linhas"]
