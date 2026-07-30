"""Testes de ferramentas/config.py."""
import json

from ferramentas import config


def test_padrao_tem_as_chaves_do_contrato():
    for chave in ("porta_plano", "teto_cartao_linhas", "padroes_segredo", "travado_extra"):
        assert chave in config.PADRAO


def test_carregar_sem_arquivo_devolve_os_defaults(tmp_path):
    cfg = config.carregar(tmp_path)
    assert cfg["porta_plano"] is True
    assert cfg["teto_cartao_linhas"] == 40
    assert cfg["_avisos"] == []


def test_config_do_projeto_sobrepoe_o_default(tmp_path):
    destino = tmp_path / ".engine"
    destino.mkdir()
    (destino / "config.json").write_text(
        json.dumps({"porta_plano": False}), encoding="utf-8"
    )
    cfg = config.carregar(tmp_path)
    assert cfg["porta_plano"] is False
    assert cfg["teto_cartao_linhas"] == 40


def test_config_quebrada_cai_no_default_e_avisa(tmp_path):
    destino = tmp_path / ".engine"
    destino.mkdir()
    (destino / "config.json").write_text("{ isso nao e json", encoding="utf-8")
    cfg = config.carregar(tmp_path)
    assert cfg["porta_plano"] is True
    assert len(cfg["_avisos"]) == 1
    assert "config.json" in cfg["_avisos"][0]
