#!/usr/bin/env python3
"""FASE 3: Teste automatizado do hook V3 com simulação de ciclo.

Testa V3 com 4 fases (PLANO, BUILD, REVISAO, DOC).
Valida que:
1. Hook carrega sem erro
2. Cartão é montado
3. Sugestão apareça (quando apropriado)
4. Teto de 50 linhas respeitado
"""
import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# UTF-8 para Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class TesteV3:
    """Teste automatizado de Fase 3 V3."""

    def __init__(self):
        self.repo_dir = Path(__file__).resolve().parent
        self.hook_path = self.repo_dir / "hooks" / "engine_contexto_v3.py"
        self.resultados = {}
        self.inicio = datetime.now()

    def criar_estado_fake(self, fase: str) -> dict:
        """Cria estado fake para uma fase."""
        estados_base = {
            "PLANO": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-v3-test",
                    "objetivo": "Testar sugestão automática de motor",
                    "iniciado_em": "2026-07-31T10:00:00",
                    "modo": "normal",
                },
                "fase": "PLANO",
                "fases_concluidas": ["DESCOBERTA", "ANALISE"],
                "cartoes": ["python"],
                "decisoes": [{"o_que": "Usar arquitetura em camadas"}],
                "pendencias": [],
                "diffs_pendentes": [],
            },
            "BUILD": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-v3-test",
                    "objetivo": "Testar sugestão automática de motor",
                    "iniciado_em": "2026-07-31T10:00:00",
                    "modo": "normal",
                },
                "fase": "BUILD",
                "fases_concluidas": ["DESCOBERTA", "ANALISE", "PLANO"],
                "cartoes": ["python", "pytest"],
                "decisoes": [],
                "pendencias": [],
                "diffs_pendentes": ["src/auth.py"],
            },
            "REVISAO": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-v3-test",
                    "objetivo": "Testar sugestão automática de motor",
                    "iniciado_em": "2026-07-31T10:00:00",
                    "modo": "normal",
                },
                "fase": "REVISAO",
                "fases_concluidas": [
                    "DESCOBERTA",
                    "ANALISE",
                    "PLANO",
                    "BUILD",
                    "TESTE",
                ],
                "cartoes": ["python", "pytest"],
                "decisoes": [],
                "pendencias": ["Performance"],
                "diffs_pendentes": ["src/auth.py"],
            },
            "DOC": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-v3-test",
                    "objetivo": "Testar sugestão automática de motor",
                    "iniciado_em": "2026-07-31T10:00:00",
                    "modo": "normal",
                },
                "fase": "DOC",
                "fases_concluidas": [
                    "DESCOBERTA",
                    "ANALISE",
                    "PLANO",
                    "BUILD",
                    "TESTE",
                    "REVISAO",
                ],
                "cartoes": ["python", "pytest", "mermaid"],
                "decisoes": [],
                "pendencias": [],
                "diffs_pendentes": [],
            },
        }
        return estados_base.get(fase, {})

    def rodar_hook_v3(self, fase: str, cwd: str) -> tuple[str, int]:
        """Roda engine_contexto_v3.py com estado fake."""
        estado = self.criar_estado_fake(fase)
        config = {"porta_plano": True, "teto_cartao_linhas": 50}

        # Criar diretório .engine
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

        # Criar volumes
        volumes_dir = Path(cwd) / "volumes" / "prontos"
        volumes_dir.mkdir(parents=True, exist_ok=True)
        for vol_nome in ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING"]:
            vol_dir = volumes_dir / vol_nome
            vol_dir.mkdir(exist_ok=True)
            readme = vol_dir / "README.md"
            readme.write_text(f"# {vol_nome}\n\nDescrição")

        # Escrever estado e config
        (engine_dir / "estado.json").write_text(
            json.dumps(estado, indent=2), encoding="utf-8"
        )
        (engine_dir / "config.json").write_text(
            json.dumps(config, indent=2), encoding="utf-8"
        )

        # Evento do hook
        evento = {
            "cwd": cwd,
            "session_id": "test-session",
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

    def validar_cartao_v3(self, fase: str, cartao: str) -> dict:
        """Valida cartão V3 de uma fase."""
        validacoes = {
            "contém_fase": fase in cartao,
            "contém_objetivo": "Objetivo:" in cartao,
            "contém_invariantes": "Nunca afirmar sucesso" in cartao,
            "respeita_teto": cartao.count("\n") + 1 <= 50,
        }

        # Validações específicas por fase
        if fase in ["PLANO", "BUILD", "REVISAO", "DOC"]:
            # Deve ter sugestão ou motores listados
            validacoes["tem_motores_ou_sugestao"] = (
                "Motores desta fase:" in cartao or "💡 Sugestão" in cartao
            )

        return validacoes

    def testar_fase_v3(self, fase: str, cwd: str) -> bool:
        """Testa uma fase com V3."""
        print(f"\n{'=' * 80}")
        print(f"TESTE V3: Fase {fase}")
        print(f"{'=' * 80}")

        # Rodar hook
        cartao, retcode = self.rodar_hook_v3(fase, cwd)

        if retcode != 0 or not cartao.strip():
            print(f"❌ Hook falhou ou retornou vazio")
            print(f"Retcode: {retcode}")
            print(f"Saída: {cartao[:200]}")
            self.resultados[fase] = {
                "status": "ERRO",
                "cartao": cartao,
                "validacoes": {},
                "passou": False,
            }
            return False

        # Validar
        validacoes = self.validar_cartao_v3(fase, cartao)
        todos_ok = all(validacoes.values())

        # Relatório
        print(f"\n--- CARTÃO INJETADO ---")
        print(cartao[:500])
        if len(cartao) > 500:
            print(f"... (truncado, {len(cartao)} chars total)")
        print(f"--- FIM DO CARTÃO ---")

        print(f"\n--- VALIDAÇÕES ---")
        for desc, ok in validacoes.items():
            status = "✅" if ok else "❌"
            print(f"{status} {desc}")

        linhas = cartao.count("\n") + 1
        print(f"\n📊 Cartão: {linhas} linhas (máx 50)")

        self.resultados[fase] = {
            "status": "OK" if todos_ok else "FALHOU",
            "cartao": cartao,
            "validacoes": validacoes,
            "passou": todos_ok,
            "linhas": linhas,
        }

        return todos_ok

    def executar(self):
        """Executa teste completo V3."""
        print("\n" + "=" * 80)
        print("FASE 3 V3: TESTE AUTOMATIZADO COM SUGESTÃO DE MOTOR")
        print("=" * 80)
        print(f"Hook: {self.hook_path}")
        print(f"Início: {self.inicio.isoformat()}")

        # Criar diretório de teste
        cwd = Path("./engine-phase3-v3") if sys.platform == "win32" else Path("/tmp/engine-phase3-v3")
        cwd.mkdir(exist_ok=True)

        # Testar cada fase
        fases = ["PLANO", "BUILD", "REVISAO", "DOC"]
        for fase in fases:
            try:
                self.testar_fase_v3(fase, str(cwd))
            except Exception as e:
                print(f"❌ ERRO em {fase}: {e}")
                self.resultados[fase] = {
                    "status": "ERRO",
                    "passou": False,
                    "erro": str(e),
                }

        # Sumário final
        passou = sum(1 for r in self.resultados.values() if r["passou"])
        total = len(self.resultados)

        print("\n" + "=" * 80)
        print("RESUMO FINAL V3")
        print("=" * 80)
        print(f"Fases testadas: {total}")
        print(f"Fases que passaram: {passou}")
        print(f"Fases que falharam: {total - passou}")

        if passou == total:
            print(f"\n✅ TODOS OS TESTES PASSARAM - V3 PRONTO PARA PRODUÇÃO")
            return 0
        else:
            print(f"\n❌ ALGUMAS FALHAS DETECTADAS")
            return 1


if __name__ == "__main__":
    teste = TesteV3()
    sys.exit(teste.executar())
