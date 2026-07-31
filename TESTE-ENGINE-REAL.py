#!/usr/bin/env python3
"""Teste END-TO-END: Simula ciclo ENGINE real com V3 ativo.

Simula:
1. Inicialização de projeto
2. 5 fases com mudanças de código
3. Hook V3 executado em cada fase
4. Validação de sugestões apropriadas
"""
import json
import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


class TesteEngineReal:
    """Simula ciclo ENGINE real com V3."""

    def __init__(self):
        self.repo_dir = Path(__file__).resolve().parent
        self.hook_path = self.repo_dir / "hooks" / "engine_contexto.py"
        self.inicio = datetime.now()
        self.resultados = {}

        # Criar diretório de teste
        self.test_dir = Path(tempfile.mkdtemp(prefix="engine-real-"))
        print(f"\n📁 Diretório de teste: {self.test_dir}")

    def setup_estrutura(self):
        """Cria estrutura ENGINE mínima."""
        print("\n" + "=" * 80)
        print("SETUP: Criando estrutura ENGINE")
        print("=" * 80)

        # Criar .engine
        engine_dir = self.test_dir / ".engine"
        engine_dir.mkdir()

        # Criar motores
        motores_dir = self.test_dir / "motores"
        for motor_nome in [
            "revisar-codigo",
            "materializar-ideia",
            "arquitetar-sistema",
            "otimizar-performance",
            "diagramar",
        ]:
            motor_dir = motores_dir / motor_nome
            motor_dir.mkdir(parents=True)
            skill_file = motor_dir / "SKILL.md"
            skill_file.write_text(
                f'---\nname: {motor_nome}\ndescription: "Teste {motor_nome}"\n---\n'
            )

        # Criar volumes
        volumes_dir = self.test_dir / "volumes" / "prontos"
        volumes_dir.mkdir(parents=True)
        for vol_nome in ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING"]:
            vol_dir = volumes_dir / vol_nome
            vol_dir.mkdir()
            readme = vol_dir / "README.md"
            readme.write_text(f"# {vol_nome}\n\nDescrição do volume")

        # Inicializar git
        subprocess.run(
            ["git", "init"],
            cwd=self.test_dir,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "teste@test.com"],
            cwd=self.test_dir,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=self.test_dir,
            capture_output=True,
        )

        # Criar arquivo inicial
        (self.test_dir / "README.md").write_text("# Projeto de Teste")
        subprocess.run(
            ["git", "add", "README.md"],
            cwd=self.test_dir,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=self.test_dir,
            capture_output=True,
        )

        print("✓ Estrutura criada")

    def criar_estado_fase(self, fase: str) -> dict:
        """Cria estado para uma fase."""
        estado_base = {
            "versao": 1,
            "ativo": True,
            "ciclo": {
                "id": "teste-engine-real",
                "objetivo": "Implementar e otimizar módulo de autenticação",
                "iniciado_em": datetime.now().isoformat(),
                "modo": "normal",
            },
            "fase": fase,
            "fases_concluidas": self._fases_concluidas(fase),
            "cartoes": self._cartoes_da_fase(fase),
            "decisoes": self._decisoes_da_fase(fase),
            "pendencias": [],
            "diffs_pendentes": self._diffs_da_fase(fase),
        }
        return estado_base

    def _fases_concluidas(self, fase: str) -> list:
        fases_ordem = [
            "DESCOBERTA",
            "ANALISE",
            "PLANO",
            "EVOLUCAO",
            "BUILD",
            "TESTE",
            "REVISAO",
            "DOC",
        ]
        idx = fases_ordem.index(fase)
        return fases_ordem[:idx]

    def _cartoes_da_fase(self, fase: str) -> list:
        cartoes = {
            "DESCOBERTA": [],
            "ANALISE": [],
            "PLANO": ["python", "pytest"],
            "EVOLUCAO": ["python", "pytest"],
            "BUILD": ["python", "pytest", "docker"],
            "TESTE": ["python", "pytest"],
            "REVISAO": ["python", "pytest"],
            "DOC": ["python", "pytest", "mermaid"],
        }
        return cartoes.get(fase, [])

    def _decisoes_da_fase(self, fase: str) -> list:
        if fase in ["PLANO", "EVOLUCAO"]:
            return [{"o_que": "Usar padrão de autenticação OAuth2"}]
        return []

    def _diffs_da_fase(self, fase: str) -> list:
        diffs = {
            "DESCOBERTA": [],
            "ANALISE": [],
            "PLANO": [],
            "EVOLUCAO": [],
            "BUILD": ["src/auth.py", "src/service.py"],
            "TESTE": ["src/auth.py"],
            "REVISAO": ["src/auth.py"],
            "DOC": [],
        }
        return diffs.get(fase, [])

    def criar_codigo_fase(self, fase: str):
        """Cria código simulando mudanças em cada fase."""
        src_dir = self.test_dir / "src"
        src_dir.mkdir(exist_ok=True)

        if fase == "BUILD":
            # Implementar autenticação
            (src_dir / "auth.py").write_text(
                """
def authenticate_user(username, password):
    user = db.find_user(username)
    if user and user.verify_password(password):
        return generate_token(user.id)
    return None

class AuthService:
    def execute(request):
        try:
            user = authenticate_user(request.user, request.pass)
            return user
        except Exception as e:
            log.error(e)
            return None
"""
            )
            (src_dir / "service.py").write_text(
                """
class UserService:
    def find_user(id):
        return db.query(User).filter(id).first()

    def save_user(user):
        db.save(user)
        return user
"""
            )

        elif fase == "REVISAO":
            # Otimizar queries
            (src_dir / "auth.py").write_text(
                """
# Otimizado com cache
@cache(ttl=300)
def authenticate_user(username, password):
    query = "SELECT * FROM users WHERE username = ? LIMIT 1"
    user = db.query(query, [username])
    if user and user.verify_password(password):
        return generate_token(user.id)
    return None

class AuthService:
    def execute(request):
        try:
            user = authenticate_user(request.user, request.pass)
            if user is None:
                raise ValueError("Invalid credentials")
            return user
        except Exception as e:
            log.error(f"Auth failed: {e}")
            raise
"""
            )

        # Fazer commit
        subprocess.run(
            ["git", "add", "-A"],
            cwd=self.test_dir,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", f"Fase {fase}: mudanças"],
            cwd=self.test_dir,
            capture_output=True,
        )

    def rodar_hook_v3(self, fase: str) -> tuple[str, int]:
        """Roda hook V3 e retorna cartão."""
        estado = self.criar_estado_fase(fase)
        config = {"porta_plano": True, "teto_cartao_linhas": 50}

        engine_dir = self.test_dir / ".engine"
        (engine_dir / "estado.json").write_text(json.dumps(estado))
        (engine_dir / "config.json").write_text(json.dumps(config))

        evento = {
            "cwd": str(self.test_dir),
            "session_id": "test-real",
            "agent_id": "main",
        }

        try:
            result = subprocess.run(
                [sys.executable, str(self.hook_path)],
                input=json.dumps(evento),
                capture_output=True,
                text=True,
                timeout=10,
                cwd=str(self.test_dir),
            )
            return result.stdout, result.returncode
        except Exception as e:
            return f"ERRO: {e}", 1

    def validar_fase(self, fase: str, cartao: str) -> dict:
        """Valida cartão da fase."""
        validacoes = {
            "tem_fase": fase in cartao,
            "tem_invariantes": "Nunca afirmar sucesso" in cartao,
            "respeita_teto": cartao.count("\n") + 1 <= 50,
        }

        # Sugestão esperada por fase
        sugestoes_esperadas = {
            "BUILD": "materializar-ideia",
            "REVISAO": "revisar-codigo",
            "DOC": "diagramar",
        }

        if fase in sugestoes_esperadas:
            motor_esperado = sugestoes_esperadas[fase]
            validacoes[f"sugere_{motor_esperado}"] = motor_esperado in cartao

        return validacoes

    def testar_fase(self, fase: str):
        """Testa uma fase completa."""
        print(f"\n{'=' * 80}")
        print(f"FASE: {fase}")
        print(f"{'=' * 80}")

        # Criar código
        self.criar_codigo_fase(fase)
        print(f"✓ Código criado para fase {fase}")

        # Rodar hook
        cartao, retcode = self.rodar_hook_v3(fase)

        if retcode != 0 or not cartao.strip():
            print(f"❌ Hook falhou")
            self.resultados[fase] = {"passou": False, "erro": "Hook failed"}
            return False

        # Validar
        validacoes = self.validar_fase(fase, cartao)
        passou = all(validacoes.values())

        # Mostrar cartão
        print("\n--- CARTÃO ENGINE ---")
        print(cartao)
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
            "cartao": cartao,
        }

        return passou

    def executar(self):
        """Executa teste ENGINE real."""
        print("\n" + "=" * 80)
        print("TESTE END-TO-END: ENGINE REAL COM V3")
        print("=" * 80)

        try:
            self.setup_estrutura()

            # Testar fases selecionadas
            fases = ["PLANO", "BUILD", "REVISAO", "DOC"]
            for fase in fases:
                try:
                    self.testar_fase(fase)
                except Exception as e:
                    print(f"❌ ERRO em {fase}: {e}")
                    self.resultados[fase] = {"passou": False, "erro": str(e)}

            # Relatório final
            passou = sum(1 for r in self.resultados.values() if r["passou"])
            total = len(self.resultados)

            print("\n" + "=" * 80)
            print("RESULTADO FINAL")
            print("=" * 80)
            print(f"Fases testadas: {total}")
            print(f"Fases que passaram: {passou}")
            print(f"Fases que falharam: {total - passou}")

            if passou == total:
                print("\n✅ TESTE ENGINE REAL PASSOU - V3 FUNCIONA!")
                return 0
            else:
                print("\n⚠️  Alguns problemas detectados")
                return 1

        finally:
            # Limpeza
            if self.test_dir.exists():
                shutil.rmtree(self.test_dir)
                print(f"\n🧹 Diretório de teste removido")


if __name__ == "__main__":
    teste = TesteEngineReal()
    sys.exit(teste.executar())
