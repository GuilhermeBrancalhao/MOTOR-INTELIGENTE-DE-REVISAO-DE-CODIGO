#!/usr/bin/env python3
"""Testes unitários para FASE 3: Análise de diff."""
import sys
import os
from pathlib import Path

# UTF-8 para Windows
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Adicionar hooks ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "hooks"))

from engine_analisa_diff import AnalisadorDiff


def test_detectar_revisar_codigo():
    """Detecta padrões de review/segurança."""
    diff = """
    + try:
    +     cursor.execute(query)
    + except Exception as e:
    +     log.error(e)
    +
    + # Verificar null pointer
    + if user is None:
    """
    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff(diff)
    assert motor == "revisar-codigo", f"Esperado 'revisar-codigo', obteve {motor}"
    print("✅ test_detectar_revisar_codigo PASSOU")


def test_detectar_otimizar_performance():
    """Detecta padrões de otimização."""
    diff = """
    - for user in all_users:
    -     for order in all_orders:
    -         if user.id == order.user_id:
    + # Usar JOIN em vez de nested loop
    + query = "SELECT * FROM users u JOIN orders o ON u.id = o.user_id"
    + results = db.query(query)
    """
    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff(diff)
    assert motor == "otimizar-performance", f"Esperado 'otimizar-performance', obteve {motor}"
    print("✅ test_detectar_otimizar_performance PASSOU")


def test_detectar_arquitetar_sistema():
    """Detecta padrões de arquitetura."""
    diff = """
    + abstract class BaseRepository {
    +     abstract def findById(id): Entity
    +     abstract def save(entity): Entity
    + }
    +
    + class UserRepository(BaseRepository):
    +     def findById(id):
    +         return self.db.query(User).filter(id)
    """
    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff(diff)
    assert motor == "arquitetar-sistema", f"Esperado 'arquitetar-sistema', obteve {motor}"
    print("✅ test_detectar_arquitetar_sistema PASSOU")


def test_detectar_materializar_ideia():
    """Detecta implementação de feature."""
    diff = """
    + def authenticate_user(username, password):
    +     user = db.find_user(username)
    +     if user and user.verify_password(password):
    +         return generate_token(user.id)
    +     return None
    +
    + def test_authenticate_valid_user():
    +     user = create_test_user()
    +     token = authenticate_user(user.username, "password123")
    +     assert token is not None
    """
    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff(diff)
    assert motor == "materializar-ideia", f"Esperado 'materializar-ideia', obteve {motor}"
    print("✅ test_detectar_materializar_ideia PASSOU")


def test_detectar_diagramar():
    """Detecta mudanças em documentação/modelos."""
    diff = """
    + # Entity-Relationship Diagram
    +
    + User (1) ---- (N) Order
    +
    + User:
    +   - id (PK)
    +   - email
    +   - name
    +
    + Order:
    +   - id (PK)
    +   - user_id (FK)
    +   - amount
    """
    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff(diff)
    assert motor == "diagramar", f"Esperado 'diagramar', obteve {motor}"
    print("✅ test_detectar_diagramar PASSOU")


def test_diff_vazio():
    """Retorna None para diff vazio."""
    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff("")
    assert motor is None, f"Esperado None, obteve {motor}"
    print("✅ test_diff_vazio PASSOU")


def test_confianca_scores():
    """Valida que scores aumentam com mais padrões."""
    diff_pequeno = "+ try:\n+     x = 1"
    diff_grande = "+ try:\n+     cursor.execute(query)\n+ except Exception:\n+     pass\n+ if user is None:\n+     return None"

    analisador1 = AnalisadorDiff()
    motor1 = analisador1.analisar_diff(diff_pequeno)
    score1 = analisador1.confianca.get(motor1, 0)

    analisador2 = AnalisadorDiff()
    motor2 = analisador2.analisar_diff(diff_grande)
    score2 = analisador2.confianca.get(motor2, 0)

    assert score2 > score1, f"Score maior deveria ter confiança > {score1}, obteve {score2}"
    print("✅ test_confianca_scores PASSOU")


def test_gerar_sugestao():
    """Valida formato de sugestão."""
    diff = "+ try:\n+     pass\n+ except:\n+     pass"
    analisador = AnalisadorDiff()
    motor = analisador.analisar_diff(diff)
    sugestao = analisador.gerar_sugestao(motor)

    assert "💡" in sugestao
    assert motor in sugestao
    assert "%" in sugestao
    print("✅ test_gerar_sugestao PASSOU")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TESTES UNITÁRIOS: FASE 3 - Análise de Diff")
    print("=" * 80)

    test_detectar_revisar_codigo()
    test_detectar_otimizar_performance()
    test_detectar_arquitetar_sistema()
    test_detectar_materializar_ideia()
    test_detectar_diagramar()
    test_diff_vazio()
    test_confianca_scores()
    test_gerar_sugestao()

    print("\n" + "=" * 80)
    print("✅ TODOS OS TESTES PASSARAM")
    print("=" * 80)
