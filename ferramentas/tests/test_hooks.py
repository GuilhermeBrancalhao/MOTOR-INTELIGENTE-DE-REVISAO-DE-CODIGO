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
HOOK_SALVAR = RAIZ_PLUGIN / "hooks" / "engine_salvar.py"
HOOK_GATE = RAIZ_PLUGIN / "hooks" / "engine_gate.py"

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


def test_cartao_respeita_o_teto_de_linhas(tmp_path):
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
    cartao = contexto.montar_cartao_estendido(dados, cfg, tmp_path, str(tmp_path))
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
def test_teto_abaixo_do_piso_produz_cartao_com_exatamente_9_linhas(teto, tmp_path):
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
    cartao = contexto.montar_cartao_estendido(dados, cfg, tmp_path, str(tmp_path))
    linhas = cartao.splitlines()
    assert len(linhas) == 9
    assert "DESCOBERTA" in cartao
    assert "objetivo do ciclo" in cartao
    for invariante in contexto.INVARIANTES:
        assert invariante in cartao


def test_teto_nao_numerico_cai_no_default_sem_levantar_excecao(tmp_path):
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
    cartao = contexto.montar_cartao_estendido(dados, cfg, tmp_path, str(tmp_path))
    assert len(cartao.splitlines()) <= 40
    for invariante in contexto.INVARIANTES:
        assert invariante in cartao


def test_teto_12_com_muitas_decisoes_e_diffs_mantem_os_cinco_invariantes(tmp_path):
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
    cartao = contexto.montar_cartao_estendido(dados, cfg, tmp_path, str(tmp_path))
    linhas = cartao.splitlines()
    assert len(linhas) <= 12
    for invariante in contexto.INVARIANTES:
        assert invariante in cartao


# --- Hook PostToolUse: a trilha auditável ----------------------------------------


def test_trilha_motor_ligado_gera_linha_com_os_campos_do_contrato(tmp_path):
    """Sete campos: os seis originais mais `ciclo`.

    `ciclo` entrou na correção da revisão adversarial da Fase 2 (CRÍTICO 3): sem o
    id do ciclo na linha, o relatório do ciclo 2 contava as ações do ciclo 1. Este
    teste tinha `== {seis campos}` e é o único teste pré-existente que a correção
    obrigou a mexer — não há como gravar o id do ciclo e manter o conjunto de seis.
    `do_motor` não aparece aqui porque só é gravado quando é verdadeiro (ação da
    própria CLI do ENGINE), e `pytest -q` não é.
    """
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
    assert set(linha.keys()) == {
        "quando", "fase", "ferramenta", "alvo", "risco", "regra", "ciclo",
    }
    assert linha["fase"] == "DESCOBERTA"
    assert linha["ferramenta"] == "Bash"
    assert linha["alvo"] == "pytest -q"
    assert linha["risco"] == "rastreado"
    assert linha["ciclo"] == estado.carregar(tmp_path)["ciclo"]["id"]


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


def test_avisos_com_teto_apertado_e_muitas_decisoes_fica_dentro_do_teto(tmp_path):
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
    cartao = contexto.montar_cartao_estendido(dados, cfg, tmp_path, str(tmp_path))
    cartao = contexto._com_avisos(cartao, cfg)
    assert len(cartao.splitlines()) <= cfg["teto_cartao_linhas"]


# --- Correção: do_motor casa qualquer forma de invocar a CLI, não só a --------
# --- substring exata "ferramentas/cli.py" --------------------------------------
#
# Revisor achou o furo: `cd ferramentas && py cli.py fase BUILD` (forma normal de
# shell depois de `cd` para dentro da pasta) não continha a substring
# "ferramentas/cli.py" nem "ferramentas.cli" — só o "cli.py" pelado sobrava — e
# por isso a linha NÃO era marcada `do_motor`, contava como evidência de fase, e
# o Stop saía 0 quando devia cobrar. A correção trocou a comparação por um regex
# de fronteira (`_RE_DO_MOTOR`); os três casos abaixo são as formas mínimas que o
# pedido de correção exige que casem.


@pytest.mark.parametrize(
    "comando",
    [
        "cd ferramentas && py cli.py fase BUILD",
        "python -m ferramentas.cli fase BUILD",
        'py "C:\\caminho\\ENGINE\\ferramentas\\cli.py" status',
    ],
)
def test_trilha_marca_do_motor_em_qualquer_forma_do_comando(tmp_path, comando):
    _ligar(tmp_path)
    saida = _rodar(
        HOOK_TRILHA,
        {"tool_name": "Bash", "tool_input": {"command": comando}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida.returncode == 0
    dados = trilha.ler(tmp_path)
    assert len(dados["linhas"]) == 1
    assert dados["linhas"][0].get("do_motor") is True


def test_trilha_nao_marca_do_motor_um_cli_py_de_outro_arquivo_colado_no_nome(tmp_path):
    """Fronteira do regex: `algum_cli.py` não é o `cli.py` pelado do ENGINE — o
    `_` antes não é separador de caminho, espaço, aspa nem início de string."""
    _ligar(tmp_path)
    saida = _rodar(
        HOOK_TRILHA,
        {
            "tool_name": "Bash",
            "tool_input": {"command": "python algum_cli.py --ajuda"},
            "cwd": str(tmp_path),
        },
        tmp_path,
    )
    assert saida.returncode == 0
    dados = trilha.ler(tmp_path)
    assert len(dados["linhas"]) == 1
    assert "do_motor" not in dados["linhas"][0]


# --- Hook PreCompact: engine_salvar.py -------------------------------------------


def _definir_fase(raiz: Path, fase: str) -> None:
    """Ajusta a fase do estado direto no disco, sem passar pelo grafo de
    transições — os testes de gate/salvar querem uma fase específica, não a
    jornada inteira até ela."""
    dados = estado.carregar(raiz)
    dados["fase"] = fase
    estado.gravar(raiz, dados)


_ISO_APROX = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"


def test_salvar_motor_ligado_grava_ultima_consolidacao_e_resumo_trilha(tmp_path):
    import re

    _ligar(tmp_path)
    trilha.registrar(
        tmp_path,
        {"quando": "x", "fase": "BUILD", "ferramenta": "Bash", "alvo": "a", "risco": "rastreado", "regra": "-"},
    )
    trilha.registrar(
        tmp_path,
        {"quando": "x", "fase": "BUILD", "ferramenta": "Edit", "alvo": "b", "risco": "rastreado", "regra": "-"},
    )
    trilha.registrar(
        tmp_path,
        {"quando": "x", "fase": "BUILD", "ferramenta": "Bash", "alvo": "c", "risco": "travado", "regra": "R2"},
    )

    saida = _rodar(
        HOOK_SALVAR,
        {"cwd": str(tmp_path), "hook_event_name": "PreCompact", "compaction_trigger": "manual"},
        tmp_path,
    )
    assert saida.returncode == 0

    dados = estado.carregar(tmp_path)
    assert re.match(_ISO_APROX, dados["ultima_consolidacao"])
    assert dados["resumo_trilha"] == {"rastreado": 2, "travado": 1}


def test_salvar_motor_desligado_nao_cria_nada(tmp_path):
    saida = _rodar(
        HOOK_SALVAR,
        {"cwd": str(tmp_path), "hook_event_name": "PreCompact", "compaction_trigger": "auto"},
        tmp_path,
    )
    assert saida.returncode == 0
    assert not estado.caminho(tmp_path).is_file()


def test_salvar_estado_desligado_apos_ciclo_nao_grava_resumo(tmp_path):
    _ligar(tmp_path)
    estado.desligar(tmp_path)
    saida = _rodar(
        HOOK_SALVAR,
        {"cwd": str(tmp_path), "hook_event_name": "PreCompact", "compaction_trigger": "manual"},
        tmp_path,
    )
    assert saida.returncode == 0
    dados = estado.carregar(tmp_path)
    assert "ultima_consolidacao" not in dados


def test_salvar_stdin_malformado_sai_0(tmp_path):
    _ligar(tmp_path)
    saida = _rodar_stdin_cru(HOOK_SALVAR, "isso nao e json", tmp_path)
    assert saida.returncode == 0
    dados = estado.carregar(tmp_path)
    assert "ultima_consolidacao" not in dados


# --- Correção: resumo_trilha do PreCompact soma só o ciclo corrente -------------
#
# Mesmo defeito já corrigido em `ferramentas/relatorio.py`: `estado.novo_ciclo`
# zera o estado mas não a trilha (append-only por contrato), então sem filtro por
# `ciclo` a consolidação do PreCompact no ciclo 2 reportava as ações do ciclo 1
# junto. Espelha `test_relatorio_do_segundo_ciclo_nao_conta_acoes_do_primeiro`
# (test_relatorio.py), mas rodando o hook de verdade e conferindo `resumo_trilha`.


def test_salvar_resumo_trilha_conta_so_o_ciclo_corrente(tmp_path):
    primeiro = estado.novo_ciclo(tmp_path, "ciclo um", "2026-07-30T09:00:00")
    id_um = primeiro["ciclo"]["id"]
    for indice in range(4):
        trilha.registrar(
            tmp_path,
            {
                "quando": str(indice), "fase": "DESCOBERTA", "ferramenta": "Write",
                "alvo": f"do_ciclo_um_{indice}.py", "risco": "rastreado", "regra": "",
                "ciclo": id_um,
            },
        )

    segundo = estado.novo_ciclo(tmp_path, "ciclo dois", "2026-07-30T10:00:00", forcar=True)
    id_dois = segundo["ciclo"]["id"]
    assert id_dois != id_um
    trilha.registrar(
        tmp_path,
        {
            "quando": "9", "fase": "DESCOBERTA", "ferramenta": "Bash",
            "alvo": "so_do_ciclo_dois", "risco": "travado", "regra": "R2",
            "ciclo": id_dois,
        },
    )

    saida = _rodar(
        HOOK_SALVAR,
        {"cwd": str(tmp_path), "hook_event_name": "PreCompact", "compaction_trigger": "manual"},
        tmp_path,
    )
    assert saida.returncode == 0

    dados = estado.carregar(tmp_path)
    assert dados["resumo_trilha"] == {"travado": 1}, (
        "o ciclo 2 tem UMA ação travada, não quatro rastreadas do ciclo 1 somadas"
    )


# --- Hook Stop: engine_gate.py -----------------------------------------------


def test_gate_cobra_na_primeira_chamada_em_build_sem_acoes(tmp_path):
    _ligar(tmp_path)
    _definir_fase(tmp_path, "BUILD")
    saida = _rodar(HOOK_GATE, {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert saida.returncode == 2
    assert "BUILD" in saida.stderr
    dados = estado.carregar(tmp_path)
    assert dados["cobrancas_por_fase"]["BUILD"] == 1


def test_gate_nao_cobra_na_segunda_chamada_contador_persistido_entre_subprocessos(tmp_path):
    _ligar(tmp_path)
    _definir_fase(tmp_path, "BUILD")
    payload = {"cwd": str(tmp_path), "stop_hook_active": False}

    primeira = _rodar(HOOK_GATE, payload, tmp_path)
    assert primeira.returncode == 2

    segunda = _rodar(HOOK_GATE, payload, tmp_path)
    assert segunda.returncode == 0
    dados = estado.carregar(tmp_path)
    assert dados["cobrancas_por_fase"]["BUILD"] == 1


def test_gate_nao_cobra_em_descoberta(tmp_path):
    _ligar(tmp_path)  # fase default é DESCOBERTA
    saida = _rodar(HOOK_GATE, {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert saida.returncode == 0
    dados = estado.carregar(tmp_path)
    assert dados.get("cobrancas_por_fase", {}) == {}


@pytest.mark.parametrize("fase", ["BUILD", "TESTE", "REVISAO"])
def test_gate_nao_cobra_quando_trilha_ja_tem_acao_da_fase(tmp_path, fase):
    _ligar(tmp_path)
    _definir_fase(tmp_path, fase)
    trilha.registrar(
        tmp_path,
        {"quando": "x", "fase": fase, "ferramenta": "Bash", "alvo": "y", "risco": "rastreado", "regra": "-"},
    )
    saida = _rodar(HOOK_GATE, {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert saida.returncode == 0
    dados = estado.carregar(tmp_path)
    assert dados.get("cobrancas_por_fase", {}).get(fase, 0) == 0


def test_gate_motor_desligado_nao_cobra(tmp_path):
    saida = _rodar(HOOK_GATE, {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert saida.returncode == 0


def test_gate_stop_hook_active_nao_cobra_mesmo_quando_cobraria(tmp_path):
    _ligar(tmp_path)
    _definir_fase(tmp_path, "TESTE")
    saida = _rodar(HOOK_GATE, {"cwd": str(tmp_path), "stop_hook_active": True}, tmp_path)
    assert saida.returncode == 0
    dados = estado.carregar(tmp_path)
    assert dados.get("cobrancas_por_fase", {}).get("TESTE", 0) == 0


def test_gate_stdin_malformado_sai_0(tmp_path):
    _ligar(tmp_path)
    _definir_fase(tmp_path, "BUILD")
    saida = _rodar_stdin_cru(HOOK_GATE, "isso nao e json", tmp_path)
    assert saida.returncode == 0
    dados = estado.carregar(tmp_path)
    assert dados.get("cobrancas_por_fase", {}) == {}


# --- Revisão adversarial, CRÍTICO 1: o cenário REAL de entrada em BUILD ----------
#
# Os testes de gate acima mudam a fase por `_definir_fase` (API + disco). Em
# operação real ninguém faz isso: entra-se em BUILD rodando `cli.py fase BUILD`
# por um comando de shell — e esse comando dispara o PostToolUse, que gravava na
# trilha uma linha JÁ com `fase: BUILD`. O gate então achava "ação da fase" e nunca
# cobrava nada. Os dois testes abaixo reproduzem o caminho real: transição pela CLI
# em subprocesso, `engine_trilha` sobre o mesmo comando, e só então o Stop.

CLI = RAIZ_PLUGIN / "ferramentas" / "cli.py"


def _cli_fase(raiz: Path, destino: str) -> tuple[subprocess.CompletedProcess, str]:
    """Roda `cli.py fase <destino>` como o Claude Code rodaria (via shell) e devolve
    também o texto do comando, para alimentar o PostToolUse logo em seguida."""
    argumentos = [sys.executable, str(CLI), "fase", destino]
    resultado = subprocess.run(
        argumentos,
        capture_output=True,
        text=True,
        cwd=str(raiz),
        env={**os.environ, "ENGINE_RAIZ": str(raiz)},
    )
    comando = f'{sys.executable} "{CLI}" fase {destino}'
    return resultado, comando


def _caminhar_ate_build_pela_cli(raiz: Path) -> None:
    """DESCOBERTA -> ANALISE -> PLANO -> BUILD, cada passo pela CLI de verdade,
    cada um seguido do PostToolUse sobre o próprio comando que rodou a CLI."""
    for destino in ("ANALISE", "PLANO", "BUILD"):
        resultado, comando = _cli_fase(raiz, destino)
        assert resultado.returncode == 0, resultado.stdout + resultado.stderr
        saida_trilha = _rodar(
            HOOK_TRILHA,
            {"tool_name": "Bash", "tool_input": {"command": comando}, "cwd": str(raiz)},
            raiz,
        )
        assert saida_trilha.returncode == 0


def test_gate_cobra_quando_a_unica_acao_da_fase_e_a_propria_cli_do_motor(tmp_path):
    _ligar(tmp_path)
    _caminhar_ate_build_pela_cli(tmp_path)

    linhas = trilha.ler(tmp_path)["linhas"]
    assert any(linha["fase"] == "BUILD" for linha in linhas), (
        "a trilha precisa ter a linha carimbada com BUILD — é ela que cegava o gate"
    )
    assert all(linha.get("do_motor") for linha in linhas), (
        "toda ação até aqui é chamada da própria CLI do ENGINE"
    )

    saida = _rodar(HOOK_GATE, {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert saida.returncode == 2, (
        "chamar a CLI do motor não é evidência de trabalho da fase: o gate tem de cobrar"
    )
    assert "BUILD" in saida.stderr
    assert estado.carregar(tmp_path)["cobrancas_por_fase"]["BUILD"] == 1


def test_gate_nao_cobra_quando_ha_acao_de_verdade_alem_da_cli_do_motor(tmp_path):
    _ligar(tmp_path)
    _caminhar_ate_build_pela_cli(tmp_path)

    # Uma ação de trabalho de verdade na fase BUILD (não é a CLI do motor).
    saida_trilha = _rodar(
        HOOK_TRILHA,
        {"tool_name": "Bash", "tool_input": {"command": "pytest -q"}, "cwd": str(tmp_path)},
        tmp_path,
    )
    assert saida_trilha.returncode == 0

    saida = _rodar(HOOK_GATE, {"cwd": str(tmp_path), "stop_hook_active": False}, tmp_path)
    assert saida.returncode == 0
    assert estado.carregar(tmp_path).get("cobrancas_por_fase", {}).get("BUILD", 0) == 0
