#!/usr/bin/env python3
"""FASE 4: Teste automatizado de volumes dinâmicos ao vivo.

Testa V4 com detecção dinâmica de volumes.
Valida que novos volumes aparecem sem hardcoding.
"""
import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class TesteFase4:
    """Teste automatizado de Fase 4 - Volumes ao Vivo."""

    def __init__(self):
        self.repo_dir = Path(__file__).resolve().parent
        self.hook_path = self.repo_dir / "hooks" / "engine_contexto_v4.py"
        self.resultados = {}
        self.inicio = datetime.now()

    def criar_estado_fase(self, fase: str, com_novos_volumes: bool = False) -> dict:
        """Cria estado para teste."""
        estado_base = {
            "versao": 1,
            "ativo": True,
            "ciclo": {
                "id": "fase4-test",
                "objetivo": "Testar volumes dinâmicos ao vivo",
                "iniciado_em": datetime.now().isoformat(),
                "modo": "normal",
            },
            "fase": fase,
            "fases_concluidas": ["DESCOBERTA", "ANALISE"],
            "cartoes": ["python"],
            "decisoes": [],
            "pendencias": [],
            "diffs_pendentes": [],
        }
        return estado_base

    def rodar_hook_v4(self, fase: str, cwd: str) -> tuple[str, int]:
        """Roda hook V4."""
        estado = self.criar_estado_fase(fase)
        config = {"porta_plano": True, "teto_cartao_linhas": 50}

        engine_dir = Path(cwd) / ".engine"
        engine_dir.mkdir(exist_ok=True)

        # Criar motores
        motores_dir = Path(cwd) / "motores"
        for motor_nome in [
            "revisar-codigo",
            "materializar-ideia",
            "arquitetar-sistema",
            "otimizar-performance",
            "diagramar",
        ]:
            motor_dir = motores_dir / motor_nome
            motor_dir.mkdir(parents=True, exist_ok=True)
            skill_file = motor_dir / "SKILL.md"
            skill_file.write_text(
                f'---\nname: {motor_nome}\ndescription: "Teste {motor_nome}"\n---\n'
            )

        # Criar volumes PRONTO (hardcoded inicialmente)
        volumes_dir = Path(cwd) / "volumes" / "prontos"
        volumes_dir.mkdir(parents=True, exist_ok=True)

        volumes_base = ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING"]
        for vol_nome in volumes_base:
            vol_dir = volumes_dir / vol_nome
            vol_dir.mkdir(exist_ok=True)
            readme = vol_dir / "README.md"
            readme.write_text(f"# {vol_nome}\n\nDescrição do volume")

        # Criar novos volumes
        for i in range(40, 45):
            vol_nome = f"{i:02d}-VOLUME-NOVO"
            vol_dir = volumes_dir / vol_nome
            vol_dir.mkdir(exist_ok=True)
            readme = vol_dir / "README.md"
            readme.write_text(
                f"# {vol_nome}\n\nNovo volume descoberto dinamicamente {i}"
            )

        # Escrever estado e config
        (engine_dir / "estado.json").write_text(json.dumps(estado))
        (engine_dir / "config.json").write_text(json.dumps(config))

        evento = {
            "cwd": cwd,
            "session_id": "test-fase4",
            "agent_id": "main",
        }

        try:
            result = subprocess.run(
                [sys.executable, str(self.hook_path)],
                input=json.dumps(evento),
                capture_output=True,
                text=True,
                timeout=10,
                cwd=cwd,
            )
            return result.stdout, result.returncode
        except Exception as e:
            return f"ERRO: {e}", 1

    def validar_cartao_v4(self, fase: str, cartao: str) -> dict:
        """Valida cartão V4."""
        validacoes = {
            "contém_fase": fase in cartao,
            "contém_invariantes": "Nunca afirmar sucesso" in cartao,
            "respeita_teto": cartao.count("\n") + 1 <= 50,
            "contém_volumes": "Volumes PRONTO" in cartao,
        }

        # Validar que volumes aparecem
        volumes_esperados = [
            "07-PROMPT-ENGINE",
            "12-MEMORY",
            "31-TESTING",
        ]
        novos_volumes = ["40-VOLUME-NOVO", "41-VOLUME-NOVO", "42-VOLUME-NOVO"]

        for vol in volumes_esperados:
            validacoes[f"tem_{vol}"] = vol in cartao

        # Pelo menos um novo volume deve aparecer (demonstra detecção dinâmica)
        validacoes["tem_novo_volume"] = any(v in cartao for v in novos_volumes)

        return validacoes

    def testar_fase_v4(self, fase: str, cwd: str) -> bool:
        """Testa uma fase com V4."""
        print(f"\n{'=' * 80}")
        print(f"TESTE V4: Fase {fase}")
        print(f"{'=' * 80}")

        # Rodar hook
        cartao, retcode = self.rodar_hook_v4(fase, cwd)

        if retcode != 0 or not cartao.strip():
            print(f"❌ Hook falhou")
            self.resultados[fase] = {"passou": False, "erro": "Hook failed"}
            return False

        # Validar
        validacoes = self.validar_cartao_v4(fase, cartao)
        passou = all(validacoes.values())

        # Mostrar cartão
        print("\n--- CARTÃO ENGINE (V4) ---")
        print(cartao[:600])
        if len(cartao) > 600:
            print(f"... (truncado, {len(cartao)} chars total)")
        print("--- FIM CARTÃO ---")

        # Validações
        print("\n--- VALIDAÇÕES ---")
        for nome, ok in validacoes.items():
            status = "✅" if ok else "❌"
            print(f"{status} {nome}")

        linhas = cartao.count("\n") + 1
        print(f"\n📊 Linhas: {linhas}/50")

        self.resultados[fase] = {
            "passou": passou,
            "linhas": linhas,
            "validacoes": validacoes,
        }

        return passou

    def executar(self):
        """Executa teste Fase 4."""
        print("\n" + "=" * 80)
        print("FASE 4: TESTE AUTOMATIZADO - VOLUMES AO VIVO")
        print("=" * 80)
        print(f"Hook: {self.hook_path}")

        # Criar diretório de teste
        cwd = Path("./engine-phase4-v4") if sys.platform == "win32" else Path("/tmp/engine-phase4-v4")
        cwd.mkdir(exist_ok=True)

        # Testar cada fase
        fases = ["PLANO", "BUILD", "REVISAO", "DOC"]
        for fase in fases:
            try:
                self.testar_fase_v4(fase, str(cwd))
            except Exception as e:
                print(f"❌ ERRO em {fase}: {e}")
                self.resultados[fase] = {
                    "passou": False,
                    "erro": str(e),
                }

        # Sumário
        passou = sum(1 for r in self.resultados.values() if r["passou"])
        total = len(self.resultados)

        print("\n" + "=" * 80)
        print("RESUMO FINAL - FASE 4")
        print("=" * 80)
        print(f"Fases testadas: {total}")
        print(f"Fases que passaram: {passou}")
        print(f"Fases que falharam: {total - passou}")

        if passou == total:
            print(f"\n✅ TODOS OS TESTES PASSARAM - V4 PRONTO!")
            return 0
        else:
            print(f"\n❌ Algumas falhas")
            return 1


if __name__ == "__main__":
    teste = TesteFase4()
    sys.exit(teste.executar())
