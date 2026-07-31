#!/usr/bin/env python3
"""FASE 2: Automação completa do teste de integração.

Simula 1 ciclo ENGINE real com engine_contexto_v2.py ativo.
Testa 5 fases: DESCOBERTA, PLANO, BUILD, REVISAO, DOC.
Gera relatório FASE2-RESULTADO.md.
"""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# UTF-8 para Windows
if sys.platform == "win32":
    for _fluxo in (sys.stdout, sys.stderr):
        try:
            _fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


class Teste:
    """Teste de Fase 2."""

    def __init__(self):
        self.repo_dir = Path(__file__).resolve().parent
        self.hook_path = self.repo_dir / "hooks" / "engine_contexto.py"
        self.resultados = {}
        self.inicio = datetime.now()

    def criar_estado_fake(self, fase: str) -> dict:
        """Cria estado fake para uma fase."""
        estados_base = {
            "DESCOBERTA": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-fase2-auto",
                    "objetivo": "Revisar e otimizar módulo de autenticação",
                    "iniciado_em": "2026-07-31T14:00:00",
                    "modo": "normal",
                },
                "fase": "DESCOBERTA",
                "fases_concluidas": [],
                "cartoes": [],
                "decisoes": [],
                "pendencias": [],
                "diffs_pendentes": [],
            },
            "PLANO": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-fase2-auto",
                    "objetivo": "Revisar e otimizar módulo de autenticação",
                    "iniciado_em": "2026-07-31T14:00:00",
                    "modo": "normal",
                },
                "fase": "PLANO",
                "fases_concluidas": ["DESCOBERTA", "ANALISE"],
                "cartoes": ["python", "pytest"],
                "decisoes": [
                    {
                        "o_que": "Handler + Service + Repository",
                        "porque": "Isolamento de responsabilidade",
                    }
                ],
                "pendencias": [],
                "diffs_pendentes": [],
            },
            "BUILD": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-fase2-auto",
                    "objetivo": "Revisar e otimizar módulo de autenticação",
                    "iniciado_em": "2026-07-31T14:00:00",
                    "modo": "normal",
                },
                "fase": "BUILD",
                "fases_concluidas": ["DESCOBERTA", "ANALISE", "PLANO"],
                "cartoes": ["python", "pytest"],
                "decisoes": [
                    {
                        "o_que": "Estrutura em camadas",
                        "porque": "Isolamento",
                    }
                ],
                "pendencias": [],
                "diffs_pendentes": ["auth/handler.py", "auth/service.py"],
            },
            "REVISAO": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-fase2-auto",
                    "objetivo": "Revisar e otimizar módulo de autenticação",
                    "iniciado_em": "2026-07-31T14:00:00",
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
                "decisoes": [
                    {
                        "o_que": "Estrutura",
                        "porque": "Isolamento",
                    }
                ],
                "pendencias": ["Verificar performance"],
                "diffs_pendentes": ["auth/handler.py"],
            },
            "DOC": {
                "versao": 1,
                "ativo": True,
                "ciclo": {
                    "id": "2026-07-31-fase2-auto",
                    "objetivo": "Revisar e otimizar módulo de autenticação",
                    "iniciado_em": "2026-07-31T14:00:00",
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
                "decisoes": [
                    {
                        "o_que": "Estrutura",
                        "porque": "Isolamento",
                    }
                ],
                "pendencias": [],
                "diffs_pendentes": [],
            },
        }
        return estados_base.get(fase, {})

    def rodar_hook(self, fase: str, cwd: str) -> tuple[str, int]:
        """Roda engine_contexto.py com estado fake."""
        estado = self.criar_estado_fake(fase)
        config = {"porta_plano": True, "teto_cartao_linhas": 50}

        # Criar diretório .engine
        engine_dir = Path(cwd) / ".engine"
        engine_dir.mkdir(exist_ok=True)

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

    def validar_cartao(self, fase: str, cartao: str) -> dict:
        """Valida cartão de uma fase."""
        validacoes = {
            "contém_fase": fase in cartao,
            "contém_objetivo": "Revisar e otimizar" in cartao,
            "contém_invariantes": "Nunca afirmar sucesso" in cartao,
            "respeita_teto": cartao.count("\n") + 1 <= 50,
        }

        # Validações específicas por fase
        if fase == "DESCOBERTA":
            validacoes["sem_motores"] = "Motores desta fase:" not in cartao
            validacoes["tem_volumes"] = "Volumes PRONTO" in cartao

        elif fase == "PLANO":
            validacoes["tem_arquitetar"] = "arquitetar-sistema" in cartao
            validacoes["tem_materializar"] = "materializar-ideia" in cartao
            validacoes["tem_volumes"] = "Volumes PRONTO" in cartao

        elif fase == "BUILD":
            validacoes["tem_materializar"] = "materializar-ideia" in cartao
            validacoes["tem_revisar"] = "revisar-codigo" in cartao
            validacoes["tem_volumes"] = "Volumes PRONTO" in cartao

        elif fase == "REVISAO":
            validacoes["tem_revisar"] = "revisar-codigo" in cartao
            validacoes["tem_otimizar"] = "otimizar-performance" in cartao
            validacoes["tem_volumes"] = "Volumes PRONTO" in cartao
            validacoes["tem_31_testing"] = "31-TESTING" in cartao

        elif fase == "DOC":
            validacoes["tem_diagramar"] = "diagramar" in cartao
            validacoes["tem_volumes"] = "Volumes PRONTO" in cartao

        return validacoes

    def testar_fase(self, fase: str, cwd: str) -> bool:
        """Testa uma fase completa."""
        print(f"\n{'=' * 80}")
        print(f"TESTE: Fase {fase}")
        print(f"{'=' * 80}")

        # Rodar hook
        cartao, retcode = self.rodar_hook(fase, cwd)

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
        validacoes = self.validar_cartao(fase, cartao)
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

    def gerar_relatorio(self):
        """Gera relatório FASE2-RESULTADO.md."""
        tempo_decorrido = datetime.now() - self.inicio
        passou = sum(1 for r in self.resultados.values() if r["passou"])
        total = len(self.resultados)

        conteudo = f"""# FASE 2: Resultado dos Testes Automatizados

**Data**: {datetime.now().isoformat()}
**Duração**: {tempo_decorrido}
**Hook**: engine_contexto_v2.py (ativo)
**Status**: {"✅ TODOS PASSARAM" if passou == total else f"❌ {passed}/{total} PASSARAM"}

---

## Sumário

| Fase | Status | Linhas | Resultado |
|---|---|---|---|
"""

        for fase in ["DESCOBERTA", "PLANO", "BUILD", "REVISAO", "DOC"]:
            if fase in self.resultados:
                r = self.resultados[fase]
                status = "✅" if r["passou"] else "❌"
                linhas = r.get("linhas", "?")
                conteudo += (
                    f"| {fase} | {r['status']} | {linhas}/50 | {status} |\n"
                )

        conteudo += "\n---\n\n## Detalhes por Fase\n"

        for fase in ["DESCOBERTA", "PLANO", "BUILD", "REVISAO", "DOC"]:
            if fase in self.resultados:
                r = self.resultados[fase]
                conteudo += f"\n### {fase}\n\n"
                conteudo += f"**Status**: {r['status']}\n"
                conteudo += f"**Linhas**: {r.get('linhas', '?')}/50\n\n"
                conteudo += "**Validações**:\n"
                for desc, ok in r["validacoes"].items():
                    conteudo += f"- {'✅' if ok else '❌'} {desc}\n"

                conteudo += f"\n**Cartão (primeiras 300 chars)**:\n```\n{r['cartao'][:300]}\n```\n"

        conteudo += f"""
---

## Checklist de Aceite: Fase 2

- [{'x' if passou == total else ' '}] ✅ Hook V2 ativado
- [{'x' if self.resultados.get("DESCOBERTA", {}).get("passou") else ' '}] ✅ DESCOBERTA: sem motores, volumes aparecem
- [{'x' if self.resultados.get("PLANO", {}).get("passou") else ' '}] ✅ PLANO: motores arquitetar + materializar
- [{'x' if self.resultados.get("BUILD", {}).get("passou") else ' '}] ✅ BUILD: motores materializar + revisar
- [{'x' if self.resultados.get("REVISAO", {}).get("passou") else ' '}] ✅ REVISAO: motores revisar + otimizar + volume 31-TESTING
- [{'x' if self.resultados.get("DOC", {}).get("passou") else ' '}] ✅ DOC: motor diagramar

---

## Resultado Final

**Teste Automatizado**: {'✅ PASSOU' if passou == total else f'❌ FALHOU ({total - passou} falhas)'}

{'Próximo passo: Commit de Fase 2' if passou == total else 'Próximo passo: Investigar falhas'}

---

Gerado por: FASE2-AUTOMATE.py
Hook testado: {self.hook_path}
"""

        resultado_path = self.repo_dir / "FASE2-RESULTADO.md"
        resultado_path.write_text(conteudo, encoding="utf-8")
        print(f"\n✓ Relatório salvo: {resultado_path}")
        return resultado_path

    def executar(self):
        """Executa teste completo."""
        print("\n" + "=" * 80)
        print("FASE 2: TESTE AUTOMATIZADO COMPLETO")
        print("=" * 80)
        print(f"Hook: {self.hook_path}")
        print(f"Início: {self.inicio.isoformat()}")

        # Criar diretório de teste
        cwd = Path("/tmp/engine-phase2") if sys.platform != "win32" else Path("./engine-phase2")
        cwd.mkdir(exist_ok=True)

        # Testar cada fase
        fases = ["DESCOBERTA", "PLANO", "BUILD", "REVISAO", "DOC"]
        for fase in fases:
            try:
                self.testar_fase(fase, str(cwd))
            except Exception as e:
                print(f"❌ ERRO em {fase}: {e}")
                self.resultados[fase] = {
                    "status": "ERRO",
                    "passou": False,
                    "erro": str(e),
                }

        # Gerar relatório
        resultado_path = self.gerar_relatorio()

        # Sumário final
        passou = sum(1 for r in self.resultados.values() if r["passou"])
        total = len(self.resultados)

        print("\n" + "=" * 80)
        print("RESUMO FINAL")
        print("=" * 80)
        print(f"Fases testadas: {total}")
        print(f"Fases que passaram: {passou}")
        print(f"Fases que falharam: {total - passou}")
        print(f"\nRelatório: {resultado_path}")

        if passou == total:
            print(f"\n✅ TODOS OS TESTES PASSARAM")
            return 0
        else:
            print(f"\n❌ ALGUMAS FALHAS DETECTADAS")
            return 1


if __name__ == "__main__":
    teste = Teste()
    sys.exit(teste.executar())
