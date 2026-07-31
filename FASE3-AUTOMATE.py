#!/usr/bin/env python3
"""FASE 3: Automação completa do teste de detecção de motor.

Simula analisador de diff com 5 tipos de mudança.
Valida que cada tipo é detectado corretamente.
Gera relatório FASE3-RESULTADO.md.
"""
import json
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

sys.path.insert(0, str(Path(__file__).parent / "hooks"))
from engine_analisa_diff import AnalisadorDiff


class TesteFase3:
    """Teste automatizado de Fase 3."""

    def __init__(self):
        self.repo_dir = Path(__file__).resolve().parent
        self.resultados = {}
        self.inicio = datetime.now()

        # Diffs de teste por tipo
        self.diffs_teste = {
            "revisar-codigo": """
+ try:
+     cursor.execute(query)
+ except Exception as e:
+     logger.error(f"DB error: {e}")
+
+ if user is None:
+     raise ValueError("User not found")
+
+ # Avoid SQL injection
+ safe_query = "SELECT * FROM users WHERE id = ?"
+ cursor.execute(safe_query, [user_id])
            """,
            "otimizar-performance": """
- for user in all_users:
-     for order in all_orders:
-         if user.id == order.user_id:
-             results.append(user)

+ # Replace nested loop with JOIN
+ query = "SELECT u.* FROM users u JOIN orders o ON u.id = o.user_id"
+ results = db.query(query)
+ results.sort(key=lambda x: x.name)
            """,
            "arquitetar-sistema": """
+ abstract class BaseRepository {
+     abstract def findById(id): Entity
+     abstract def save(entity): Entity
+ }
+
+ class UserRepository(BaseRepository):
+     def findById(id):
+         return self.db.query(User).filter(id)
+
+ class OrderRepository(BaseRepository):
+     def findById(id):
+         return self.db.query(Order).filter(id)
            """,
            "materializar-ideia": """
+ def authenticate_user(username, password):
+     user = db.find_user(username)
+     if user and user.verify_password(password):
+         return generate_token(user.id)
+     return None
+
+ def test_authenticate_valid_user():
+     user = create_test_user()
+     token = authenticate_user(user.username, "password")
+     assert token is not None
            """,
            "diagramar": """
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
            """,
        }

    def testar_motor(self, tipo: str, diff: str) -> dict:
        """Testa detecção de um tipo de motor."""
        analisador = AnalisadorDiff()
        motor_detectado = analisador.analisar_diff(diff)
        sugestao = analisador.gerar_sugestao(motor_detectado) if motor_detectado else ""
        confianca = analisador.confianca.get(motor_detectado, 0)

        passou = motor_detectado == tipo
        return {
            "tipo": tipo,
            "motor_detectado": motor_detectado,
            "passou": passou,
            "sugestao": sugestao,
            "confianca": confianca,
        }

    def executar(self):
        """Executa teste completo."""
        print("\n" + "=" * 80)
        print("FASE 3: TESTE AUTOMATIZADO - DETECÇÃO DE MOTOR")
        print("=" * 80)
        print(f"Início: {self.inicio.isoformat()}")
        print(f"Analisador: engine_analisa_diff.py")
        print()

        # Testar cada tipo
        tipos_motores = [
            "revisar-codigo",
            "otimizar-performance",
            "arquitetar-sistema",
            "materializar-ideia",
            "diagramar",
        ]

        for tipo in tipos_motores:
            print(f"\n{'=' * 80}")
            print(f"TESTE: {tipo.upper()}")
            print(f"{'=' * 80}")

            diff = self.diffs_teste.get(tipo, "")
            resultado = self.testar_motor(tipo, diff)
            self.resultados[tipo] = resultado

            # Relatório
            status = "✅" if resultado["passou"] else "❌"
            print(f"{status} Motor detectado: {resultado['motor_detectado']}")
            print(f"   Confiança: {resultado['confianca']}")
            if resultado["sugestao"]:
                print(f"   {resultado['sugestao']}")
            else:
                print(f"   (sem sugestão)")

        # Gerar relatório
        self.gerar_relatorio()

        # Sumário
        passou = sum(1 for r in self.resultados.values() if r["passou"])
        total = len(self.resultados)

        print("\n" + "=" * 80)
        print("RESUMO FINAL")
        print("=" * 80)
        print(f"Tipos testados: {total}")
        print(f"Detectados corretamente: {passou}")
        print(f"Falharam: {total - passou}")

        if passou == total:
            print(f"\n✅ TODOS OS MOTORES FORAM DETECTADOS CORRETAMENTE")
            return 0
        else:
            print(f"\n❌ ALGUMAS DETECÇÕES FALHARAM")
            return 1

    def gerar_relatorio(self):
        """Gera relatório FASE3-RESULTADO.md."""
        tempo_decorrido = datetime.now() - self.inicio
        passou = sum(1 for r in self.resultados.values() if r["passou"])
        total = len(self.resultados)

        conteudo = f"""# FASE 3: Resultado dos Testes Automatizados

**Data**: {datetime.now().isoformat()}
**Duração**: {tempo_decorrido}
**Analisador**: engine_analisa_diff.py
**Status**: {"✅ TODOS DETECTADOS" if passou == total else f"❌ {passou}/{total} DETECTADOS"}

---

## Sumário

| Tipo de Motor | Detectado | Confiança | Resultado |
|---|---|---|---|
"""

        for tipo in [
            "revisar-codigo",
            "otimizar-performance",
            "arquitetar-sistema",
            "materializar-ideia",
            "diagramar",
        ]:
            if tipo in self.resultados:
                r = self.resultados[tipo]
                status = "✅" if r["passou"] else "❌"
                confianca = f"{int((r['confianca'] / max([x['confianca'] for x in self.resultados.values()]) * 100))}%"
                conteudo += f"| {tipo} | {r['motor_detectado']} | {confianca} | {status} |\n"

        conteudo += "\n---\n\n## Detalhes por Tipo\n"

        for tipo in [
            "revisar-codigo",
            "otimizar-performance",
            "arquitetar-sistema",
            "materializar-ideia",
            "diagramar",
        ]:
            if tipo in self.resultados:
                r = self.resultados[tipo]
                status_text = "✅ PASSOU" if r["passou"] else "❌ FALHOU"
                conteudo += f"\n### {tipo.upper()}\n\n"
                conteudo += f"**Status**: {status_text}\n"
                conteudo += f"**Motor detectado**: {r['motor_detectado']}\n"
                conteudo += f"**Confiança**: {r['confianca']}\n\n"
                if r["sugestao"]:
                    conteudo += f"**Sugestão**:\n```\n{r['sugestao']}\n```\n"

        conteudo += f"""

---

## Checklist de Aceite: Fase 3

- [{'x' if passou == total else ' '}] ✅ Analisador carrega sem erros
- [{'x' if self.resultados.get("revisar-codigo", {}).get("passou") else ' '}] ✅ Detecta revisar-codigo
- [{'x' if self.resultados.get("otimizar-performance", {}).get("passou") else ' '}] ✅ Detecta otimizar-performance
- [{'x' if self.resultados.get("arquitetar-sistema", {}).get("passou") else ' '}] ✅ Detecta arquitetar-sistema
- [{'x' if self.resultados.get("materializar-ideia", {}).get("passou") else ' '}] ✅ Detecta materializar-ideia
- [{'x' if self.resultados.get("diagramar", {}).get("passou") else ' '}] ✅ Detecta diagramar

---

## Resultado Final

**Teste Automatizado**: {'✅ PASSOU' if passou == total else f'❌ FALHOU ({total - passou} falhas)'}

{'Próximo passo: Criar engine_contexto_v3.py' if passou == total else 'Próximo passo: Revisar padrões no analisador'}

---

Gerado por: FASE3-AUTOMATE.py
Analisador testado: {Path(__file__).parent / "hooks" / "engine_analisa_diff.py"}
"""

        resultado_path = Path(__file__).parent / "FASE3-RESULTADO.md"
        resultado_path.write_text(conteudo, encoding="utf-8")
        print(f"\n✓ Relatório salvo: {resultado_path}")


if __name__ == "__main__":
    teste = TesteFase3()
    sys.exit(teste.executar())
