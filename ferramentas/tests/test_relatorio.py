"""Testes de `ferramentas/relatorio.py`: relatório de ciclo e de fase a partir da trilha."""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ_PLUGIN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ_PLUGIN))

from ferramentas import estado, relatorio, trilha  # noqa: E402


def _preparar_ciclo(raiz: Path) -> dict:
    dados = estado.novo_ciclo(raiz, "concluir F2-T3", "2026-07-30T09:00:00")
    dados["decisoes"] = [
        {"o_que": "usar Markdown puro", "porque": "consistente com o cartão da CLI"},
    ]
    dados["pendencias"] = ["confirmar contrato do hook Stop"]
    dados["diffs_pendentes"] = ["ferramentas/relatorio.py"]
    dados = estado.transicionar(dados, "ANALISE")
    estado.gravar(raiz, dados)
    return dados


def _gravar_trilha_sintetica(raiz: Path) -> None:
    # 5 ações sintéticas: 2 livres, 2 rastreadas, 1 travada.
    entradas = [
        {"quando": "1", "fase": "DESCOBERTA", "ferramenta": "Read", "alvo": "a.py",
         "risco": "livre", "regra": ""},
        {"quando": "2", "fase": "DESCOBERTA", "ferramenta": "Grep", "alvo": "padrao",
         "risco": "livre", "regra": ""},
        {"quando": "3", "fase": "ANALISE", "ferramenta": "Write",
         "alvo": "ferramentas/relatorio.py", "risco": "rastreado", "regra": ""},
        {"quando": "4", "fase": "ANALISE", "ferramenta": "Edit",
         "alvo": "ferramentas/relatorio.py", "risco": "rastreado", "regra": ""},
        {"quando": "5", "fase": "ANALISE", "ferramenta": "Bash", "alvo": "rm -rf /",
         "risco": "travado", "regra": "R3"},
    ]
    for entrada in entradas:
        trilha.registrar(raiz, entrada)


def test_de_ciclo_com_trilha_sintetica_contem_objetivo_decisoes_e_contagens(tmp_path):
    _preparar_ciclo(tmp_path)
    _gravar_trilha_sintetica(tmp_path)

    texto = relatorio.de_ciclo(tmp_path)

    assert isinstance(texto, str)
    assert "concluir F2-T3" in texto
    assert "usar Markdown puro" in texto
    assert "consistente com o cartão da CLI" in texto
    assert "livre: 2" in texto
    assert "rastreado: 2" in texto
    assert "travado: 1" in texto
    assert "ferramentas/relatorio.py" in texto


def test_de_ciclo_sem_trilha_contem_frase_de_ausencia(tmp_path):
    _preparar_ciclo(tmp_path)

    texto = relatorio.de_ciclo(tmp_path)

    assert "nenhuma ação registrada" in texto.lower()


def test_de_ciclo_sem_estado_contem_frase_de_motor_nunca_ligou(tmp_path):
    texto = relatorio.de_ciclo(tmp_path)

    assert isinstance(texto, str)
    assert "nunca ligou" in texto.lower()


def test_de_ciclo_com_estado_corrompido_nao_levanta(tmp_path):
    caminho_estado = estado.caminho(tmp_path)
    caminho_estado.parent.mkdir(parents=True, exist_ok=True)
    caminho_estado.write_text("isso nao e json", encoding="utf-8")

    texto = relatorio.de_ciclo(tmp_path)

    assert isinstance(texto, str)
    assert "nunca ligou" in texto.lower()


def test_de_fase_filtra_so_a_fase_pedida(tmp_path):
    _preparar_ciclo(tmp_path)
    _gravar_trilha_sintetica(tmp_path)

    texto = relatorio.de_fase(tmp_path, "ANALISE")

    assert "ferramentas/relatorio.py" in texto
    assert "a.py" not in texto
    assert "padrao" not in texto


def test_de_fase_sem_acao_diz_isso(tmp_path):
    _preparar_ciclo(tmp_path)
    _gravar_trilha_sintetica(tmp_path)

    texto = relatorio.de_fase(tmp_path, "BUILD")

    assert "nenhuma ação" in texto.lower()


def test_de_fase_traz_diffs_e_pendencias_do_estado(tmp_path):
    _preparar_ciclo(tmp_path)

    texto = relatorio.de_fase(tmp_path, "ANALISE")

    assert "ferramentas/relatorio.py" in texto
    assert "confirmar contrato do hook Stop" in texto


def test_trilha_com_aviso_aparece_no_relatorio_como_nota(tmp_path):
    _preparar_ciclo(tmp_path)
    caminho_trilha = trilha.caminho(tmp_path)
    caminho_trilha.parent.mkdir(parents=True, exist_ok=True)
    with caminho_trilha.open("w", encoding="utf-8") as arquivo:
        arquivo.write("isso nao e json\n")

    texto_ciclo = relatorio.de_ciclo(tmp_path)
    texto_fase = relatorio.de_fase(tmp_path, "DESCOBERTA")

    assert "aviso" in texto_ciclo.lower()
    assert "ilegível" in texto_ciclo.lower()
    assert "aviso" in texto_fase.lower()


def test_de_fase_com_argumento_estranho_nao_levanta(tmp_path):
    _preparar_ciclo(tmp_path)
    texto = relatorio.de_fase(tmp_path, None)  # type: ignore[arg-type]
    assert isinstance(texto, str)


def test_de_fase_com_estado_ausente_nao_levanta(tmp_path):
    texto = relatorio.de_fase(tmp_path, "BUILD")
    assert isinstance(texto, str)
    assert "nenhuma ação" in texto.lower()
