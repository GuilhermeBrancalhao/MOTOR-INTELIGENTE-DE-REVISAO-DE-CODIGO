"""Testes da camada de aprendizado por relatorio (`ferramentas/conhecimento.py`)."""
from __future__ import annotations

import json

from ferramentas import conhecimento, estado


AGORA = "2026-08-05T10:00:00"


def _estado_base(tmp_path):
    dados = estado.novo_ciclo(tmp_path, "objetivo", AGORA)
    dados["fase"] = "DOC"
    dados["cartoes"] = ["python"]
    dados["pendencias"] = [
        "erro de concorrencia em programa.lock",
        "ajustar checklist de revisao",
    ]
    dados["diffs_pendentes"] = ["servico.py"]
    estado.gravar(tmp_path, dados)
    return dados


def test_extrair_do_relatorio_ler_pendencias_e_diffs():
    texto = """
# Relatorio de ciclo

## Diffs por apresentar
- app/servico.py

## Pendencias abertas
- erro critico no fluxo de aceite
- documentar cobertura
"""
    itens = conhecimento.extrair_do_relatorio(
        texto,
        ciclo="2026-08-05-1",
        fase="DOC",
        cartoes=["python"],
    )
    assert len(itens) == 3
    por_categoria = {item["categoria"] for item in itens}
    assert por_categoria == {"diff_pendente", "pendencia"}
    criticos = [item for item in itens if item["severidade"] == "critico"]
    assert criticos, "pendencia com 'erro' deveria ser critica"
    assert all("categoria_semantica" in item for item in itens)
    assert all("confianca" in item for item in itens)
    assert all("origem" in item for item in itens)


def test_extrair_do_relatorio_aceita_titulo_com_acento():
    texto = """
# Relatorio de ciclo

## Pend\u00eancias abertas
- erro critico no login
"""
    itens = conhecimento.extrair_do_relatorio(
        texto,
        ciclo="2026-08-05-1",
        fase="DOC",
        cartoes=["python"],
    )
    assert len(itens) == 1
    assert itens[0]["categoria"] == "pendencia"


def test_atualizar_por_relatorio_gera_lacunas_backlog_e_pendentes(tmp_path):
    dados = _estado_base(tmp_path)

    resumo = conhecimento.atualizar_por_relatorio(tmp_path, dados)

    assert resumo["novas"] >= 1
    assert conhecimento.caminho_lacunas(tmp_path).is_file()
    assert conhecimento.caminho_backlog(tmp_path).is_file()
    assert (conhecimento.caminho_pendentes(tmp_path) / "python.md").is_file()

    backlog = json.loads(conhecimento.caminho_backlog(tmp_path).read_text(encoding="utf-8"))
    assert "resumo" in backlog
    assert "itens" in backlog
    assert all("confianca" in item for item in backlog["itens"])


def test_atualizar_por_relatorio_deduplica_por_id(tmp_path):
    dados = _estado_base(tmp_path)

    primeiro = conhecimento.atualizar_por_relatorio(tmp_path, dados)
    segundo = conhecimento.atualizar_por_relatorio(tmp_path, dados)

    assert primeiro["novas"] >= 1
    assert segundo["novas"] == 0


def test_lacunas_criticas_do_estado_encontra_pendencia_bloqueante(tmp_path):
    dados = _estado_base(tmp_path)
    criticas = conhecimento.lacunas_criticas_do_estado(dados)
    assert criticas == ["erro de concorrencia em programa.lock"]
