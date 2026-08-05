"""Testes da CLI usada pela skill /engine."""
import json
import os
import subprocess
import sys
from pathlib import Path

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]


def _cli(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "ferramentas.cli", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(RAIZ_PLUGIN),
        env={**os.environ, "ENGINE_RAIZ": str(cwd)},
    )


def test_ligar_cria_o_estado(tmp_path):
    saida = _cli(tmp_path, "ligar", "somar dois numeros")
    assert saida.returncode == 0
    assert (tmp_path / ".engine" / "estado.json").is_file()
    assert "DESCOBERTA" in saida.stdout


def test_status_com_motor_desligado(tmp_path):
    saida = _cli(tmp_path, "status")
    assert saida.returncode == 0
    assert "desligado" in saida.stdout.lower()


def test_desligar_depois_de_ligar(tmp_path):
    _cli(tmp_path, "ligar", "x")
    saida = _cli(tmp_path, "desligar")
    assert saida.returncode == 0
    assert "desligado" in saida.stdout.lower()


def test_fase_invalida_reporta_erro_sem_estourar(tmp_path):
    _cli(tmp_path, "ligar", "x")
    saida = _cli(tmp_path, "fase", "ENTREGA")
    assert saida.returncode == 1
    assert "não existe no grafo" in saida.stdout + saida.stderr


def test_verbo_desconhecido_sai_com_erro(tmp_path):
    saida = _cli(tmp_path, "voar")
    assert saida.returncode == 1


def test_ligar_sem_objetivo_reporta_erro_sem_estourar(tmp_path):
    saida = _cli(tmp_path, "ligar")
    assert saida.returncode == 1


def test_ligar_duas_vezes_sem_forcar_reporta_erro_sem_estourar(tmp_path):
    _cli(tmp_path, "ligar", "primeiro objetivo")
    saida = _cli(tmp_path, "ligar", "segundo objetivo")
    assert saida.returncode == 1
    assert "primeiro objetivo" in saida.stdout + saida.stderr
    assert "Traceback" not in saida.stderr


def test_ligar_duas_vezes_com_forcar_sobrescreve(tmp_path):
    _cli(tmp_path, "ligar", "primeiro objetivo")
    saida = _cli(tmp_path, "ligar", "segundo objetivo", "--forcar")
    assert saida.returncode == 0
    assert "segundo objetivo" in saida.stdout


def test_fase_sem_ciclo_ativo_reporta_erro_sem_estourar(tmp_path):
    saida = _cli(tmp_path, "fase", "ANALISE")
    assert saida.returncode == 1


def test_desligar_sem_ciclo_nunca_ligado_nao_estoura(tmp_path):
    saida = _cli(tmp_path, "desligar")
    assert saida.returncode == 0
    assert "desligado" in saida.stdout.lower()


# --- REVISÃO FINAL, IMPORTANTE 5: `desligar` não suja projeto alheio --------------
#
# Num projeto que nunca teve ciclo, `desligar` CRIAVA `.engine/estado.json` com
# `{"ativo": false}` — e a partir dali `status` imprimia o relatório verboso para
# sempre naquele projeto.


def test_desligar_sem_ciclo_nao_cria_arquivo_nenhum(tmp_path):
    saida = _cli(tmp_path, "desligar")
    assert saida.returncode == 0
    assert not (tmp_path / ".engine" / "estado.json").exists()
    assert not (tmp_path / ".engine").exists()
    assert list(tmp_path.iterdir()) == []


def test_status_depois_de_desligar_sem_ciclo_segue_limpo(tmp_path):
    _cli(tmp_path, "desligar")
    saida = _cli(tmp_path, "status")
    assert saida.returncode == 0
    assert saida.stdout.strip() == "**ENGINE:** desligado (nenhum ciclo neste projeto)."


# --- REVISÃO FINAL, CRÍTICO 3: a CLI roda como SCRIPT, de qualquer diretório -------


def test_cli_roda_como_script_de_qualquer_diretorio(tmp_path):
    """A forma que a skill documenta: `py <plugin>/ferramentas/cli.py`, cwd alheio.

    A forma antiga (`python -m ferramentas.cli`) rodada da raiz de um projeto
    hospedeiro dá `ModuleNotFoundError: No module named 'ferramentas'`.
    """
    projeto = tmp_path / "projeto"
    projeto.mkdir()
    saida = subprocess.run(
        [sys.executable, str(RAIZ_PLUGIN / "ferramentas" / "cli.py"), "status"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=str(projeto),
        env={**os.environ, "ENGINE_RAIZ": str(projeto)},
    )
    assert saida.returncode == 0, saida.stderr
    assert "desligado" in saida.stdout.lower()
    assert "Traceback" not in saida.stderr


def test_cli_como_script_liga_e_desliga_um_ciclo(tmp_path):
    def _script(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(RAIZ_PLUGIN / "ferramentas" / "cli.py"), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            cwd=str(tmp_path),
            env={**os.environ, "ENGINE_RAIZ": str(tmp_path)},
        )

    assert _script("ligar", "objetivo pela forma de script").returncode == 0
    assert (tmp_path / ".engine" / "estado.json").is_file()
    saida = _script("desligar")
    assert saida.returncode == 0
    assert "desligado" in saida.stdout.lower()


def test_desligar_com_estado_corrompido_nao_estoura(tmp_path):
    _corromper_estado(tmp_path)
    saida = _cli(tmp_path, "desligar")
    assert saida.returncode == 0
    assert "Traceback" not in saida.stderr


def test_acentuacao_sai_em_utf8(tmp_path):
    saida = _cli(tmp_path, "ligar", "verificar acentuação e ç")
    assert saida.returncode == 0
    assert "verificar acentuação e ç" in saida.stdout
    assert "�" not in saida.stdout


def _corromper_estado(tmp_path: Path) -> None:
    alvo = tmp_path / ".engine"
    alvo.mkdir(parents=True)
    (alvo / "estado.json").write_text("{isto nao e json", encoding="utf-8")


def test_status_com_estado_corrompido_reporta_erro_sem_estourar(tmp_path):
    _corromper_estado(tmp_path)
    saida = _cli(tmp_path, "status")
    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr


def test_fase_com_estado_corrompido_reporta_erro_sem_estourar(tmp_path):
    _corromper_estado(tmp_path)
    saida = _cli(tmp_path, "fase", "ANALISE")
    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr


# --- F2-T5: ligar --dry ------------------------------------------------------------


def test_ligar_com_dry_grava_modo_dry(tmp_path):
    saida = _cli(tmp_path, "ligar", "planejar sem escrever", "--dry")
    assert saida.returncode == 0
    conteudo = (tmp_path / ".engine" / "estado.json").read_text(encoding="utf-8")
    assert '"modo": "dry"' in conteudo
    assert "dry" in saida.stdout.lower()


def test_ligar_com_dry_e_forcar_coexistem(tmp_path):
    _cli(tmp_path, "ligar", "primeiro")
    saida = _cli(tmp_path, "ligar", "segundo", "--dry", "--forcar")
    assert saida.returncode == 0
    assert "segundo" in saida.stdout
    conteudo = (tmp_path / ".engine" / "estado.json").read_text(encoding="utf-8")
    assert '"modo": "dry"' in conteudo


def test_ligar_sem_dry_grava_modo_normal(tmp_path):
    _cli(tmp_path, "ligar", "objetivo normal")
    conteudo = (tmp_path / ".engine" / "estado.json").read_text(encoding="utf-8")
    assert '"modo": "normal"' in conteudo


# --- F2-T5: ligar detecta cartões ---------------------------------------------------


def test_ligar_detecta_cartoes_do_projeto(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    saida = _cli(tmp_path, "ligar", "detectar stack")
    assert saida.returncode == 0
    conteudo = (tmp_path / ".engine" / "estado.json").read_text(encoding="utf-8")
    assert "python" in conteudo
    assert "python" in saida.stdout


def test_ligar_sem_nenhuma_tecnologia_grava_cartoes_vazio(tmp_path):
    saida = _cli(tmp_path, "ligar", "projeto vazio")
    assert saida.returncode == 0
    conteudo = (tmp_path / ".engine" / "estado.json").read_text(encoding="utf-8")
    assert '"cartoes": []' in conteudo


# --- F2-T5: retomar ------------------------------------------------------------------


def test_retomar_sem_estado_sai_1_com_mensagem(tmp_path):
    saida = _cli(tmp_path, "retomar")
    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr
    assert saida.stdout.strip() != ""


def test_retomar_com_estado_corrompido_sai_1_sem_tocar_no_arquivo(tmp_path):
    _corromper_estado(tmp_path)
    caminho_estado = tmp_path / ".engine" / "estado.json"
    conteudo_antes = caminho_estado.read_text(encoding="utf-8")
    saida = _cli(tmp_path, "retomar")
    assert saida.returncode == 1
    assert "Traceback" not in saida.stderr
    assert caminho_estado.read_text(encoding="utf-8") == conteudo_antes


def test_retomar_com_estado_e_trilha_imprime_fase_objetivo_e_ultima_acao(tmp_path):
    _cli(tmp_path, "ligar", "concluir a tarefa F2-T5")
    trilha_path = tmp_path / ".engine" / "trilha.jsonl"
    entradas = [
        {"quando": "1", "fase": "DESCOBERTA", "ferramenta": "Read", "alvo": "a.py",
         "risco": "livre", "regra": ""},
        {"quando": "2", "fase": "DESCOBERTA", "ferramenta": "Write", "alvo": "b.py",
         "risco": "rastreado", "regra": ""},
    ]
    with trilha_path.open("a", encoding="utf-8") as arquivo:
        for entrada in entradas:
            arquivo.write(json.dumps(entrada) + "\n")

    saida = _cli(tmp_path, "retomar")
    assert saida.returncode == 0
    assert "DESCOBERTA" in saida.stdout
    assert "concluir a tarefa F2-T5" in saida.stdout
    assert "b.py" in saida.stdout


# --- F2-T5: relatorio ----------------------------------------------------------------


def test_relatorio_ciclo_imprime_o_objetivo(tmp_path):
    _cli(tmp_path, "ligar", "objetivo do relatorio de ciclo")
    saida = _cli(tmp_path, "relatorio", "ciclo")
    assert saida.returncode == 0
    assert "objetivo do relatorio de ciclo" in saida.stdout


def test_relatorio_sem_argumento_usa_ciclo_por_padrao(tmp_path):
    _cli(tmp_path, "ligar", "objetivo padrao")
    saida = _cli(tmp_path, "relatorio")
    assert saida.returncode == 0
    assert "objetivo padrao" in saida.stdout


def test_relatorio_fase_build_roda_com_saida_0(tmp_path):
    _cli(tmp_path, "ligar", "objetivo qualquer")
    saida = _cli(tmp_path, "relatorio", "fase", "BUILD")
    assert saida.returncode == 0
    assert "Traceback" not in saida.stderr


def test_relatorio_fase_inexistente_nao_estoura(tmp_path):
    _cli(tmp_path, "ligar", "objetivo qualquer")
    saida = _cli(tmp_path, "relatorio", "fase", "NAO_EXISTE")
    assert saida.returncode == 0
    assert "Traceback" not in saida.stderr


def test_conhecimento_atualizar_gera_artefatos_de_lacunas(tmp_path):
    _cli(tmp_path, "ligar", "objetivo com aprendizado")
    caminho = tmp_path / ".engine" / "estado.json"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["pendencias"] = ["erro de segurança no fluxo de login"]
    dados["diffs_pendentes"] = ["api/login.py"]
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

    saida = _cli(tmp_path, "conhecimento", "atualizar")

    assert saida.returncode == 0
    assert (tmp_path / ".engine" / "lacunas.jsonl").is_file()
    assert (tmp_path / ".engine" / "backlog_conhecimento.json").is_file()
    assert "Lacunas novas" in saida.stdout


def test_conhecimento_revisar_lista_propostas_pendentes(tmp_path):
    _cli(tmp_path, "ligar", "objetivo com revisao")
    caminho = tmp_path / ".engine" / "estado.json"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["cartoes"] = ["python"]
    dados["pendencias"] = ["erro de seguranca no login"]
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    _cli(tmp_path, "conhecimento", "atualizar")

    saida = _cli(tmp_path, "conhecimento", "revisar")

    assert saida.returncode == 0
    assert "Propostas de conhecimento" in saida.stdout
    assert (tmp_path / ".engine" / "aprovacoes_conhecimento.json").is_file()


def test_conhecimento_revisar_id_mostra_detalhe(tmp_path):
    _cli(tmp_path, "ligar", "objetivo com detalhe")
    caminho = tmp_path / ".engine" / "estado.json"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["cartoes"] = ["python"]
    dados["pendencias"] = ["erro de seguranca no login"]
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")
    _cli(tmp_path, "conhecimento", "pipeline")

    aprovacoes = json.loads((tmp_path / ".engine" / "aprovacoes_conhecimento.json").read_text(encoding="utf-8"))
    pid = aprovacoes["propostas"][0]["id"]

    saida = _cli(tmp_path, "conhecimento", "revisar", pid)

    assert saida.returncode == 0
    assert "Detalhe da proposta" in saida.stdout
    assert pid in saida.stdout


def test_conhecimento_aprovar_id_inexistente_retorna_1(tmp_path):
    saida = _cli(tmp_path, "conhecimento", "aprovar", "inexistente")
    assert saida.returncode == 1
    assert "nao encontrada" in saida.stdout.lower()


def test_conhecimento_pipeline_gera_resumo_unificado(tmp_path):
    _cli(tmp_path, "ligar", "objetivo com pipeline")
    caminho = tmp_path / ".engine" / "estado.json"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["cartoes"] = ["python"]
    dados["pendencias"] = ["erro de concorrencia no lock do estado"]
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

    saida = _cli(tmp_path, "conhecimento", "pipeline")

    assert saida.returncode == 0
    assert "Pipeline de conhecimento" in saida.stdout
    assert (tmp_path / ".engine" / "backlog_conhecimento.json").is_file()
    assert (tmp_path / ".engine" / "aprovacoes_conhecimento.json").is_file()


def test_fase_doc_para_entrega_bloqueia_com_lacuna_critica(tmp_path):
    _cli(tmp_path, "ligar", "objetivo qualquer")
    caminho = tmp_path / ".engine" / "estado.json"
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    dados["fase"] = "DOC"
    dados["pendencias"] = ["erro crítico ainda aberto"]
    caminho.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

    saida = _cli(tmp_path, "fase", "ENTREGA")

    assert saida.returncode == 1
    assert "DOC -> ENTREGA recusada" in saida.stdout
    estado_final = json.loads(caminho.read_text(encoding="utf-8"))
    assert estado_final["fase"] == "DOC"
