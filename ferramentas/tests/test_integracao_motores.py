"""Testes da integração: Motores + Engine + Volumes."""
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Imports do engine
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from hooks import engine_contexto_v2 as engine_novo  # noqa: E402


class TestCarregamentoMotores:
    """Verifica que motores são detectados e carregados."""

    def test_motores_por_fase_completo(self):
        """Fases relevantes têm motores."""
        assert engine_novo.MOTORES_POR_FASE["PLANO"] == [
            "arquitetar-sistema",
            "materializar-ideia",
        ]
        assert engine_novo.MOTORES_POR_FASE["REVISAO"] == [
            "revisar-codigo",
            "otimizar-performance",
        ]
        assert engine_novo.MOTORES_POR_FASE["BUILD"] == [
            "materializar-ideia",
            "revisar-codigo",
        ]

    def test_volumes_prontos_definidos(self):
        """Os 3 volumes PRONTO estão registrados."""
        assert "07-PROMPT-ENGINE" in engine_novo.VOLUMES_PRONTOS
        assert "12-MEMORY" in engine_novo.VOLUMES_PRONTOS
        assert "31-TESTING" in engine_novo.VOLUMES_PRONTOS
        assert len(engine_novo.VOLUMES_PRONTOS) == 3

    def test_ler_descricao_motor_existe(self, tmp_path):
        """Lê description de um SKILL.md válido."""
        # Cria estrutura fake
        motor_dir = tmp_path / "motores" / "revisar-codigo"
        motor_dir.mkdir(parents=True)

        skill_content = '''---
name: revisar-codigo
description: Motor que revisa código com critério escrito
---

# Motor de revisão
'''
        (motor_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")

        desc = engine_novo._ler_descricao_motor(tmp_path, "revisar-codigo")
        assert desc is not None
        assert "revisa código" in desc

    def test_ler_descricao_motor_nao_existe(self, tmp_path):
        """Retorna None se motor não existe."""
        desc = engine_novo._ler_descricao_motor(tmp_path, "inexistente")
        assert desc is None

    def test_cortar_respeita_limite(self):
        """Função de corte respeita limite de caracteres."""
        texto_longo = "a" * 200
        cortado = engine_novo._cortar(texto_longo, 50)
        assert len(cortado) <= 50
        assert cortado.endswith("…")

    def test_teto_efetivo_respeita_minimo(self):
        """Teto nunca fica abaixo do mínimo."""
        cfg = {"teto_cartao_linhas": 5}
        teto = engine_novo._teto_efetivo(cfg)
        assert teto >= engine_novo.MINIMO_CARTAO

    def test_teto_efetivo_normaliza_nao_numerico(self):
        """Valor não-numérico cai no default."""
        cfg = {"teto_cartao_linhas": "not_a_number"}
        teto = engine_novo._teto_efetivo(cfg)
        assert teto == 40


class TestMontaçãoCartão:
    """Verifica montagem do cartão com motores."""

    def test_cartao_com_motores_fase_revisao(self, tmp_path):
        """Cartão da fase REVISAO inclui motores corretos."""
        # Setup
        motor_dir = tmp_path / "motores" / "revisar-codigo"
        motor_dir.mkdir(parents=True)
        (motor_dir / "SKILL.md").write_text(
            '---\nname: revisar-codigo\ndescription: Revisa com severidade\n---\n'
        )

        dados = {
            "ativo": True,
            "fase": "REVISAO",
            "ciclo": {"objetivo": "Otimizar performance", "modo": "normal"},
            "cartoes": ["python", "pytest"],
        }
        cfg = {"teto_cartao_linhas": 60}

        cartao = engine_novo.montar_cartao_estendido(dados, cfg, tmp_path)

        # Verificações
        assert "REVISAO" in cartao
        assert "Motores desta fase:" in cartao
        assert "revisar-codigo" in cartao
        assert "otimizar-performance" in cartao

    def test_cartao_fase_sem_motores(self):
        """Fases sem motores não listam seção."""
        dados = {
            "ativo": True,
            "fase": "DESCOBERTA",
            "ciclo": {"objetivo": "Entender o pedido", "modo": "normal"},
        }
        cfg = {"teto_cartao_linhas": 60}

        cartao = engine_novo.montar_cartao_estendido(dados, cfg, Path("."))

        # DESCOBERTA não tem motores, então seção não deve aparecer
        assert "Motores desta fase:" not in cartao or "• " not in cartao.split("Motores desta fase:")[1].split("\n")[0]

    def test_cartao_respeita_teto(self, tmp_path):
        """Cartão nunca ultrapassa o teto de linhas."""
        motor_dir = tmp_path / "motores" / "revisar-codigo"
        motor_dir.mkdir(parents=True)
        (motor_dir / "SKILL.md").write_text(
            '---\nname: revisar-codigo\ndescription: Uma descrição bem longa que deveria ser cortada se for muito grande\n---\n'
        )

        dados = {
            "ativo": True,
            "fase": "REVISAO",
            "ciclo": {
                "objetivo": "Fazer algo bem complicado que exige muita explicação",
                "modo": "normal",
            },
            "cartoes": ["python", "pytest", "fastapi", "react"],
            "decisoes": [{"o_que": "coisa", "porque": "motivo"}],
        }
        cfg = {"teto_cartao_linhas": 30}

        cartao = engine_novo.montar_cartao_estendido(dados, cfg, tmp_path)
        linhas = cartao.count("\n") + 1

        assert linhas <= 30, f"Cartão tem {linhas} linhas, máximo é 30"


class TestInjeçãoNohook:
    """Verifica comportamento completo do hook."""

    def test_principal_com_engine_inativo(self):
        """Hook retorna 0 se engine está inativo."""
        evento = {"cwd": "/tmp"}
        entrada = json.dumps(evento).encode("utf-8")

        with patch("sys.stdin") as mock_stdin, patch(
            "engine_contexto_v2.estado.carregar"
        ) as mock_estado:
            mock_stdin.readlines.return_value = [entrada.decode()]
            mock_estado.return_value = {"ativo": False}

            # Resultado: nada é impresso, hook retorna 0
            assert engine_novo.principal() == 0

    def test_principal_entrada_invalida(self):
        """Hook retorna 0 se entrada JSON é inválida."""
        entrada = "isso não é JSON"

        with patch("sys.stdin") as mock_stdin:
            mock_stdin.read.return_value = entrada

            # Resultado: hook retorna 0 silenciosamente
            assert engine_novo.principal() == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
