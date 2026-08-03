#!/usr/bin/env python3
"""Teste real: Simula ciclo ENGINE com motores + volumes injetados.

Testa o hook VIVO hooks/engine_contexto.py com estado fake em diferentes fases.
Os volumes são detectados dinamicamente de volumes/prontos/ do projeto de teste
(nada de lista hardcoded), por isso o projeto fake também recebe essa estrutura.
"""
import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Forçar UTF-8 no Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Setup
PROJETO_ENGINE = Path(__file__).resolve().parent.parent
HOOK_CONTEXTO = PROJETO_ENGINE / "hooks" / "engine_contexto.py"

# Volumes PRONTO do projeto fake — o hook vivo os descobre dinamicamente
VOLUMES_FAKE = ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING"]

# Estado fake para cada fase
ESTADOS = {
    "DESCOBERTA": {
        "versao": 1,
        "ativo": True,
        "ciclo": {
            "id": "2026-07-31-test",
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
            "id": "2026-07-31-test",
            "objetivo": "Revisar e otimizar módulo de autenticação",
            "iniciado_em": "2026-07-31T14:00:00",
            "modo": "normal",
        },
        "fase": "PLANO",
        "fases_concluidas": ["DESCOBERTA", "ANALISE"],
        "cartoes": ["python", "pytest"],
        "decisoes": [
            {
                "o_que": "Estrutura em camadas (Handler, Service, Repository)",
                "porque": "Isolamento de responsabilidade; testabilidade; reduz acoplamento",
            }
        ],
        "pendencias": [],
        "diffs_pendentes": [],
    },
    "BUILD": {
        "versao": 1,
        "ativo": True,
        "ciclo": {
            "id": "2026-07-31-test",
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
                "porque": "Isolamento de responsabilidade",
            }
        ],
        "pendencias": [],
        "diffs_pendentes": ["auth/handler.py", "auth/service.py"],
    },
    "REVISAO": {
        "versao": 1,
        "ativo": True,
        "ciclo": {
            "id": "2026-07-31-test",
            "objetivo": "Revisar e otimizar módulo de autenticação",
            "iniciado_em": "2026-07-31T14:00:00",
            "modo": "normal",
        },
        "fase": "REVISAO",
        "fases_concluidas": ["DESCOBERTA", "ANALISE", "PLANO", "BUILD", "TESTE"],
        "cartoes": ["python", "pytest"],
        "decisoes": [
            {
                "o_que": "Estrutura em camadas",
                "porque": "Isolamento",
            }
        ],
        "pendencias": ["Verificar performance de login sob carga"],
        "diffs_pendentes": ["auth/handler.py", "auth/service.py"],
    },
    "DOC": {
        "versao": 1,
        "ativo": True,
        "ciclo": {
            "id": "2026-07-31-test",
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
                "o_que": "Estrutura em camadas",
                "porque": "Isolamento",
            }
        ],
        "pendencias": [],
        "diffs_pendentes": [],
    },
}

CONFIG = {
    "porta_plano": True,
    "teto_cartao_linhas": 50,
}


def rodar_hook(fase: str, cwd: str) -> str:
    """Roda o hook vivo hooks/engine_contexto.py com estado fake."""
    if fase not in ESTADOS:
        raise ValueError(f"Fase desconhecida: {fase}")

    evento = {
        "cwd": cwd,
        "session_id": "test-session",
        "agent_id": "main",
    }

    try:
        result = subprocess.run(
            [sys.executable, str(HOOK_CONTEXTO)],
            input=json.dumps(evento),
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd,
        )
        return result.stdout
    except Exception as e:
        return f"ERRO ao rodar hook: {e}"


def testar_fase(fase: str, projeto_root: Path):
    """Testa uma fase: cria estado, roda hook, valida saída."""
    print(f"\n{'=' * 80}")
    print(f"TESTE: Fase {fase}")
    print(f"{'=' * 80}")

    # Criar .engine/estado.json fake
    engine_dir = projeto_root / ".engine"
    engine_dir.mkdir(exist_ok=True)

    estado_path = engine_dir / "estado.json"
    estado_path.write_text(json.dumps(ESTADOS[fase], indent=2), encoding="utf-8")

    config_path = engine_dir / "config.json"
    config_path.write_text(json.dumps(CONFIG, indent=2), encoding="utf-8")

    # Volumes PRONTO fake: o hook vivo detecta dinamicamente em volumes/prontos/
    for vol_nome in VOLUMES_FAKE:
        vol_dir = projeto_root / "volumes" / "prontos" / vol_nome
        vol_dir.mkdir(parents=True, exist_ok=True)
        (vol_dir / "_VOLUME.yml").write_text(
            f'status: PRONTO\nescopo: "Volume fake {vol_nome} para o aceite"\n',
            encoding="utf-8",
        )

    print(f"✓ Estado criado em {estado_path}")

    # Rodar hook
    print(f"\nRodando hook engine_contexto.py...")
    saida = rodar_hook(fase, str(projeto_root))

    if not saida.strip():
        print("⚠️  Hook retornou vazio (esperado se ENGINE inativo)")
        return False

    # Verificar saída
    print("\n--- CARTÃO INJETADO ---")
    print(saida)
    print("--- FIM DO CARTÃO ---")

    # Validações
    validacoes = {
        "Contém fase": fase in saida,
        "Contém objetivo": "Revisar e otimizar" in saida,
        "Contém invariantes": "Nunca afirmar sucesso" in saida,
    }

    # Validações específicas por fase
    if fase == "PLANO":
        validacoes["Contém motor arquitetar-sistema"] = (
            "arquitetar-sistema" in saida
        )
        validacoes["Contém motor materializar-ideia"] = (
            "materializar-ideia" in saida
        )
    elif fase == "BUILD":
        validacoes["Contém motor materializar-ideia"] = (
            "materializar-ideia" in saida
        )
        validacoes["Contém motor revisar-codigo"] = "revisar-codigo" in saida
    elif fase == "REVISAO":
        validacoes["Contém motor revisar-codigo"] = "revisar-codigo" in saida
        validacoes["Contém motor otimizar-performance"] = (
            "otimizar-performance" in saida
        )
        validacoes["Contém volume 31-TESTING"] = "31-TESTING" in saida
    elif fase == "DOC":
        validacoes["Contém motor diagramar"] = "diagramar" in saida

    print("\n--- VALIDAÇÕES ---")
    todos_ok = True
    for desc, resultado in validacoes.items():
        status = "✅" if resultado else "❌"
        print(f"{status} {desc}")
        if not resultado:
            todos_ok = False

    # Contar linhas
    linhas = saida.count("\n") + 1
    print(f"\n📊 Cartão tem {linhas} linhas (máximo: {CONFIG['teto_cartao_linhas']})")
    if linhas > CONFIG["teto_cartao_linhas"]:
        print("❌ ERRO: Ultrapassou o teto!")
        todos_ok = False
    else:
        print("✅ Respeitou teto de linhas")

    return todos_ok


def main():
    """Executa testes de todas as fases."""
    print("\n" + "=" * 80)
    print("TESTE DE INTEGRAÇÃO: Motores + Agentes + Volumes")
    print("=" * 80)
    print(f"Hook testado: {HOOK_CONTEXTO}")
    print(f"Data: {datetime.now().isoformat()}")

    # Criar diretório de teste
    projeto_teste = Path("/tmp/engine-test") if sys.platform != "win32" else Path("./engine-test")
    projeto_teste.mkdir(exist_ok=True)
    print(f"Projeto de teste: {projeto_teste}")

    # Testar cada fase
    fases_teste = ["DESCOBERTA", "PLANO", "BUILD", "REVISAO", "DOC"]
    resultados = {}

    for fase in fases_teste:
        try:
            ok = testar_fase(fase, projeto_teste)
            resultados[fase] = "✅ PASSOU" if ok else "❌ FALHOU"
        except Exception as e:
            print(f"❌ ERRO em {fase}: {e}")
            resultados[fase] = f"❌ ERRO: {e}"

    # Resumo
    print("\n" + "=" * 80)
    print("RESUMO DOS TESTES")
    print("=" * 80)
    for fase, resultado in resultados.items():
        print(f"{fase:15s} {resultado}")

    # Limpeza
    print(f"\n✓ Arquivos de teste em {projeto_teste}")
    print("  (Manter para debug ou deletar conforme necessário)")

    # Status final
    todos_ok = all("✅" in r for r in resultados.values())
    print("\n" + "=" * 80)
    if todos_ok:
        print("✅ TODOS OS TESTES PASSARAM")
        return 0
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        return 1


if __name__ == "__main__":
    sys.exit(main())
