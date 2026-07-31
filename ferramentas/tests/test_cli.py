"""Testes da CLI usada pela skill /engine."""
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
