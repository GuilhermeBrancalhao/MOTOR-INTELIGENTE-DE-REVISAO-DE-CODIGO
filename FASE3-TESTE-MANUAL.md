# FASE 3: Teste Manual - Detecção Automática de Motor

**Data**: 31 de julho de 2026  
**Hook novo**: `engine_analisa_diff.py` (PreToolUse)  
**Hook modificado**: `engine_contexto_v3.py` (injeta sugestão)

---

## Setup

1. **Ativar Fase 3**
   ```bash
   # Backup do v2
   cp hooks/engine_contexto.py hooks/engine_contexto.py.backup-fase2
   
   # Copiar v3 (será criado em seguida)
   cp hooks/engine_contexto_v3.py hooks/engine_contexto.py
   ```

2. **Verificar que hook está ativo**
   ```bash
   grep -q "engine_analisa_diff" hooks/engine_contexto.py && echo "✅ V3 ativo"
   ```

---

## Ciclos de Teste

### Ciclo 1: Review de Código (esperado: revisar-codigo)

**Ação do usuário**:
```python
# Editar arquivo de autenticação
+ try:
+     user = db.find_user(username)
+     if user.password == password:
+         return user
+ except Exception as e:
+     log.error(f"Auth failed: {e}")
+     return None
```

**Validar**:
- [ ] Cartão ENGINE aparece
- [ ] Sugestão contém `revisar-codigo`
- [ ] Confiança > 50%
- [ ] Descrição: "padrões de segurança/confiabilidade"

---

### Ciclo 2: Otimização de Query (esperado: otimizar-performance)

**Ação do usuário**:
```python
# Arquivo de dados
- results = []
- for user in all_users:
-     for order in all_orders:
-         if user.id == order.user_id:
-             results.append((user, order))

+ # Use SQL JOIN instead
+ query = "SELECT u.*, o.* FROM users u JOIN orders o ON u.id = o.user_id"
+ results = db.query(query)
```

**Validar**:
- [ ] Sugestão contém `otimizar-performance`
- [ ] Confiança > 50%
- [ ] Reconhece "JOIN" e "query"

---

### Ciclo 3: Refatoração Arquitetural (esperado: arquitetar-sistema)

**Ação do usuário**:
```python
# Novos padrões
+ abstract class BaseService:
+     abstract def execute(request): Response
+
+ class AuthService(BaseService):
+     def execute(request: AuthRequest):
+         user = self.verify(request.token)
+         return AuthResponse(user)
```

**Validar**:
- [ ] Sugestão contém `arquitetar-sistema`
- [ ] Reconhece "abstract" e "class"
- [ ] Diferencia de materializar-ideia

---

### Ciclo 4: Implementação de Feature (esperado: materializar-ideia)

**Ação do usuário**:
```python
+ def send_notification(user_id: int, message: str) -> bool:
+     user = db.get_user(user_id)
+     if not user:
+         return False
+     smtp.send(user.email, message)
+     return True
+
+ def test_send_notification():
+     assert send_notification(123, "hello") is True
+     assert send_notification(999, "hello") is False
```

**Validar**:
- [ ] Sugestão contém `materializar-ideia`
- [ ] Reconhece "def" e "test"

---

### Ciclo 5: Documentação/Modelo (esperado: diagramar)

**Ação do usuário**:
```markdown
# Sistema de Pedidos

## Entidades

User (1) ---- (N) Order
- id (PK)
- email
- name

Order
- id (PK)
- user_id (FK)
- total

## Fluxo de Pagamento

1. User submits order
2. Payment service validates
3. Order status → PAID
```

**Validar**:
- [ ] Sugestão contém `diagramar`
- [ ] Reconhece extensão `.md` ou palavras "entity", "flow"

---

## Checklist de Validação

### Analisador Funcionando
- [ ] `engine_analisa_diff.py` carrega sem erros
- [ ] 8 testes unitários passam
- [ ] Sugestão formatada corretamente

### Integração com Hook
- [ ] `engine_contexto_v3.py` criado e ativo
- [ ] Sugestão injeta no cartão (não em DESCOBERTA)
- [ ] Não quebra teto de 50 linhas
- [ ] Testado em PLANO, BUILD, REVISAO, DOC

### Cada Motor Detecta Corretamente
- [ ] revisar-codigo: segurança, tratamento de erro
- [ ] otimizar-performance: query, index, join, loop
- [ ] arquitetar-sistema: abstract, interface, pattern
- [ ] materializar-ideia: def, endpoint, test
- [ ] diagramar: modelo, flow, markdown

### Edge Cases
- [ ] Diff vazio → sem sugestão
- [ ] Palavras ambíguas → score balanceado
- [ ] Múltiplos motores → retorna maior confiança

---

## Reportar Resultados

Após completar os 5 ciclos, responda:

1. **Todos os motores foram detectados?** (Sim/Não)
   - Se Não: quais falharam?

2. **Sugestão estava precisa?** (Sim/Parcialmente/Não)
   - Exemplos de falsos positivos?

3. **Confiança era visível?** (Sim/Não)
   - Formato claro: "💡 Sugestão: motor-x (75%)"?

4. **Teto respeitado?** (Sim/Não)
   - Alguma fase ultrapassou 50 linhas?

5. **Algum erro?**
   - Python exceptions?
   - Hook não executou?

6. **Pronto para Fase 4?** (Sim/Não)

---

## Revert (se necessário)

```bash
cp hooks/engine_contexto.py.backup-fase2 hooks/engine_contexto.py
```

Hook voltará ao v2 (sem sugestão automática).

---

**Boa sorte! Reporte os resultados quando terminar.** 🚀
