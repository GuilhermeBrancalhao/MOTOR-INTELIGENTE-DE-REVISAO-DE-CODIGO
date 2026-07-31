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


# --- Revisão adversarial, CRÍTICO 3: a trilha não separava ciclos ----------------


def _gravar_trilha_crua(raiz: Path, entradas: list[dict]) -> None:
    """Escreve a trilha de uma vez, sem passar por `trilha.registrar`.

    Usado onde o teste precisa de volume (teto de linhas) ou de uma linha em claro
    (trilha ANTIGA, anterior à redação) — os dois casos que `registrar` não produz.
    """
    import json

    caminho = trilha.caminho(raiz)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8") as arquivo:
        for entrada in entradas:
            arquivo.write(json.dumps(entrada, ensure_ascii=False) + "\n")


def test_relatorio_do_segundo_ciclo_nao_conta_acoes_do_primeiro(tmp_path):
    """O caso verificado pelo revisor: `novo_ciclo` zera o estado mas não a trilha,
    e o relatório do ciclo 2 contava as 4 ações do ciclo 1 (número errado, não só
    verboso)."""
    primeiro = estado.novo_ciclo(tmp_path, "ciclo um", "2026-07-30T09:00:00")
    id_um = primeiro["ciclo"]["id"]
    for indice in range(4):
        trilha.registrar(
            tmp_path,
            {"quando": str(indice), "fase": "DESCOBERTA", "ferramenta": "Write",
             "alvo": f"do_ciclo_um_{indice}.py", "risco": "rastreado", "regra": "",
             "ciclo": id_um},
        )

    segundo = estado.novo_ciclo(
        tmp_path, "ciclo dois", "2026-07-30T10:00:00", forcar=True
    )
    id_dois = segundo["ciclo"]["id"]
    assert id_dois != id_um
    trilha.registrar(
        tmp_path,
        {"quando": "9", "fase": "DESCOBERTA", "ferramenta": "Write",
         "alvo": "do_ciclo_dois.py", "risco": "rastreado", "regra": "", "ciclo": id_dois},
    )

    texto = relatorio.de_ciclo(tmp_path)

    assert "ciclo dois" in texto
    assert "rastreado: 1" in texto, "o ciclo 2 tem UMA ação, não cinco"
    assert "do_ciclo_dois.py" in texto
    assert "do_ciclo_um_0.py" not in texto


def test_de_fase_do_segundo_ciclo_tambem_ignora_o_primeiro(tmp_path):
    primeiro = estado.novo_ciclo(tmp_path, "ciclo um", "2026-07-30T09:00:00")
    trilha.registrar(
        tmp_path,
        {"quando": "1", "fase": "DESCOBERTA", "ferramenta": "Write",
         "alvo": "so_do_ciclo_um.py", "risco": "rastreado", "regra": "",
         "ciclo": primeiro["ciclo"]["id"]},
    )
    segundo = estado.novo_ciclo(
        tmp_path, "ciclo dois", "2026-07-30T10:00:00", forcar=True
    )
    trilha.registrar(
        tmp_path,
        {"quando": "2", "fase": "DESCOBERTA", "ferramenta": "Write",
         "alvo": "so_do_ciclo_dois.py", "risco": "rastreado", "regra": "",
         "ciclo": segundo["ciclo"]["id"]},
    )

    texto = relatorio.de_fase(tmp_path, "DESCOBERTA")

    assert "so_do_ciclo_dois.py" in texto
    assert "so_do_ciclo_um.py" not in texto


def test_linhas_sem_id_de_ciclo_sao_ignoradas_e_o_relatorio_diz_quantas(tmp_path):
    """Trilha MISTA (linhas antigas sem id + linhas novas com id): as antigas saem
    do número e o relatório declara quantas foram ignoradas."""
    dados = estado.novo_ciclo(tmp_path, "ciclo com trilha mista", "2026-07-30T09:00:00")
    id_ciclo = dados["ciclo"]["id"]
    _gravar_trilha_crua(
        tmp_path,
        [
            {"quando": "1", "fase": "DESCOBERTA", "ferramenta": "Bash",
             "alvo": "antiga_um", "risco": "rastreado", "regra": ""},
            {"quando": "2", "fase": "DESCOBERTA", "ferramenta": "Bash",
             "alvo": "antiga_dois", "risco": "rastreado", "regra": ""},
            {"quando": "3", "fase": "DESCOBERTA", "ferramenta": "Bash",
             "alvo": "nova", "risco": "livre", "regra": "", "ciclo": id_ciclo},
        ],
    )

    texto = relatorio.de_ciclo(tmp_path)

    assert "livre: 1" in texto
    assert "rastreado: 0" in texto
    assert "2 ação(ões) sem id de ciclo" in texto


def test_de_fase_respeita_o_teto_de_linhas_e_diz_quantas_omitiu(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "ciclo gigante", "2026-07-30T09:00:00")
    id_ciclo = dados["ciclo"]["id"]
    _gravar_trilha_crua(
        tmp_path,
        [
            {"quando": str(i), "fase": "DESCOBERTA", "ferramenta": "Bash",
             "alvo": f"comando_{i}", "risco": "rastreado", "regra": "", "ciclo": id_ciclo}
            for i in range(5000)
        ],
    )

    texto = relatorio.de_fase(tmp_path, "DESCOBERTA")
    linhas = texto.splitlines()

    assert len(linhas) <= relatorio.TETO_LINHAS
    assert "omitida" in texto
    # O rodapé (diffs/pendências) sobrevive ao corte: quem corta é a listagem.
    assert "Pendências abertas" in texto


def test_de_ciclo_respeita_o_teto_de_linhas(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "ciclo gigante", "2026-07-30T09:00:00")
    id_ciclo = dados["ciclo"]["id"]
    _gravar_trilha_crua(
        tmp_path,
        [
            {"quando": str(i), "fase": "DESCOBERTA", "ferramenta": "Write",
             "alvo": f"arquivo_{i}.py", "risco": "rastreado", "regra": "", "ciclo": id_ciclo}
            for i in range(5000)
        ],
    )

    texto = relatorio.de_ciclo(tmp_path)
    linhas = texto.splitlines()

    assert len(linhas) <= relatorio.TETO_LINHAS
    assert "rastreado: 5000" in texto, "o teto corta a LISTAGEM, não falseia a contagem"
    assert "omitida" in texto


def test_de_fase_redige_segredo_de_trilha_antiga_gravada_em_claro(tmp_path):
    """Defesa em profundidade: a trilha de antes da correção tem o segredo em claro
    no arquivo; a impressão é a última barreira antes de ele voltar ao contexto."""
    _preparar_ciclo(tmp_path)
    _gravar_trilha_crua(
        tmp_path,
        [
            {"quando": "1", "fase": "ANALISE", "ferramenta": "Bash",
             "alvo": 'psql "postgresql://admin:S3nh4Secreta@db.prod:5432/app"',
             "risco": "rastreado", "regra": ""},
        ],
    )

    texto = relatorio.de_fase(tmp_path, "ANALISE")

    assert "S3nh4Secreta" not in texto
    assert trilha.MARCA_REDIGIDO in texto
