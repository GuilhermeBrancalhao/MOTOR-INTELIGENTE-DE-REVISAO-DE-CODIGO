"""Testes de ferramentas/config.py."""
import json

import pytest

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


# --- REVISÃO FINAL, CRÍTICO 2: a config do hospedeiro entra por LISTA BRANCA -------
#
# `cfg.update(dados)` absorvia qualquer chave do arquivo do projeto, inclusive
# `_avisos` (apagava a trilha interna de problemas) e `padroes_segredo` (único insumo
# da família R5, que um `[]` desarmava inteira).


def _escrever_config(tmp_path, dados: dict) -> None:
    destino = tmp_path / ".engine"
    destino.mkdir(exist_ok=True)
    (destino / "config.json").write_text(json.dumps(dados), encoding="utf-8")


def test_chave_desconhecida_e_ignorada_e_avisada(tmp_path):
    _escrever_config(tmp_path, {"chave_inventada": 123, "porta_plano": False})
    cfg = config.carregar(tmp_path)
    assert "chave_inventada" not in cfg
    assert cfg["porta_plano"] is False, "a chave legítima do mesmo arquivo tem de valer"
    assert any("chave_inventada" in aviso for aviso in cfg["_avisos"])


def test_config_nao_pode_esvaziar_os_padroes_de_segredo(tmp_path):
    _escrever_config(tmp_path, {"padroes_segredo": []})
    cfg = config.carregar(tmp_path)
    for padrao in config.PADRAO["padroes_segredo"]:
        assert padrao in cfg["padroes_segredo"], f"{padrao} sumiu: R5 foi desarmada"


def test_config_nao_pode_reduzir_os_padroes_de_segredo(tmp_path):
    """Sobrepor por uma lista menor é a forma sutil do mesmo ataque."""
    _escrever_config(tmp_path, {"padroes_segredo": ["*.nada"]})
    cfg = config.carregar(tmp_path)
    for padrao in config.PADRAO["padroes_segredo"]:
        assert padrao in cfg["padroes_segredo"]
    assert "*.nada" in cfg["padroes_segredo"], "ampliar a lista continua permitido"


def test_config_nao_pode_injetar_avisos(tmp_path):
    _escrever_config(tmp_path, {"_avisos": ["tudo certo, pode confiar"]})
    cfg = config.carregar(tmp_path)
    assert "tudo certo, pode confiar" not in cfg["_avisos"]
    assert any("_avisos" in aviso for aviso in cfg["_avisos"])


def test_padroes_de_segredo_que_nao_e_lista_avisa_e_mantem_o_default(tmp_path):
    _escrever_config(tmp_path, {"padroes_segredo": "*.tudo"})
    cfg = config.carregar(tmp_path)
    assert cfg["padroes_segredo"] == config.PADRAO["padroes_segredo"]
    assert any("padroes_segredo" in aviso for aviso in cfg["_avisos"])


# --- Revisão adversarial, IMPORTANTE 4: validar o que vem do projeto -------------
#
# `teto_cartao_linhas` aceitava qualquer coisa (string, objeto, booleano) e
# `travado_extra` não tinha validação de forma — uma regex inválida chegava até
# `re.search` e o classificador falhava fechado, travando a sessão inteira a
# partir do `.engine/config.json` do projeto, sem nenhum aviso.


@pytest.mark.parametrize("valor", ["abc", 12.5, {"x": 1}, [40], True, None])
def test_teto_de_tipo_errado_e_descartado_com_aviso(tmp_path, valor):
    _escrever_config(tmp_path, {"teto_cartao_linhas": valor})
    cfg = config.carregar(tmp_path)
    assert cfg["teto_cartao_linhas"] == 40, "tipo errado tem de cair no default"
    assert any("teto_cartao_linhas" in aviso for aviso in cfg["_avisos"])


def test_teto_inteiro_legitimo_continua_valendo(tmp_path):
    _escrever_config(tmp_path, {"teto_cartao_linhas": 25})
    cfg = config.carregar(tmp_path)
    assert cfg["teto_cartao_linhas"] == 25
    assert cfg["_avisos"] == []


def test_travado_extra_que_nao_e_lista_e_descartado_com_aviso(tmp_path):
    _escrever_config(tmp_path, {"travado_extra": "não sou lista"})
    cfg = config.carregar(tmp_path)
    assert cfg["travado_extra"] == []
    assert any("travado_extra" in aviso for aviso in cfg["_avisos"])


def test_travado_extra_item_malformado_e_descartado_sem_derrubar_os_demais(tmp_path):
    _escrever_config(
        tmp_path,
        {
            "travado_extra": [
                {"regra": "RX", "motivo": "regex quebrada", "padrao": "[abertura"},
                "nem é objeto",
                {"regra": "RY", "motivo": "falta o padrao"},
                {"regra": "RZ", "motivo": "proibido no projeto", "padrao": r"\bcomando_proibido\b"},
            ]
        },
    )
    cfg = config.carregar(tmp_path)
    assert cfg["travado_extra"] == [
        {"regra": "RZ", "motivo": "proibido no projeto", "padrao": r"\bcomando_proibido\b"}
    ], "só o item bem formado sobrevive"
    assert sum("travado_extra" in aviso for aviso in cfg["_avisos"]) == 3, (
        "um aviso por item descartado, dizendo o que foi ignorado"
    )


def test_travado_extra_com_regex_invalida_nao_derruba_o_classificador(tmp_path):
    """Antes da validação, a regex inválida chegava a `re.search` dentro do
    classificador, que falha fechado: TUDO travava por R0. Com o item descartado
    na fusão, o comando inofensivo segue rastreado e o item válido segue ativo."""
    from ferramentas import risco

    _escrever_config(
        tmp_path,
        {
            "travado_extra": [
                {"regra": "RX", "motivo": "regex quebrada", "padrao": "[abertura"},
                {"regra": "RZ", "motivo": "proibido no projeto", "padrao": r"\bcomando_proibido\b"},
            ]
        },
    )
    cfg = config.carregar(tmp_path)

    inofensivo = risco.classificar(
        "Bash", {"command": "pytest -q"}, raiz=tmp_path, config=cfg
    )
    assert inofensivo.nivel == risco.RASTREADO, (
        f"classificador tinha de seguir funcional, saiu {inofensivo}"
    )

    proibido = risco.classificar(
        "Bash", {"command": "comando_proibido agora"}, raiz=tmp_path, config=cfg
    )
    assert proibido.nivel == risco.TRAVADO
    assert proibido.regra == "RZ", "o item válido da lista continua armado"


def test_carregar_nao_compartilha_listas_com_o_padrao(tmp_path):
    """Cópia rasa deixaria mutação vazar para PADRAO e contaminar chamadas seguintes."""
    cfg = config.carregar(tmp_path)
    cfg["padroes_segredo"].append("*.invasor")
    assert "*.invasor" not in config.PADRAO["padroes_segredo"]
    assert "*.invasor" not in config.carregar(tmp_path)["padroes_segredo"]
