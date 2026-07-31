# FASE 3: Automação - Plano de Execução

**Objetivo**: Detecção automática de motor via análise de diff  
**Status**: 🚀 EM PROGRESSO  
**Data início**: 2026-07-31

---

## Sumário Executivo

Fase 3 adiciona **inteligência automática** ao ENGINE via novo hook `PreToolUse`.

Quando o usuário faz mudanças no código, o hook:
1. Analisa diff (padrões de código)
2. Classifica tipo de mudança (revisar, otimizar, arquitetar, materializar, diagramar)
3. Sugere motor apropriado no cartão ENGINE
4. Usuário aprova ou ignora

**Resultado**: ENGINE aprende com o trabalho do usuário e oferece ferramentas relevantes.

---

## Arquitetura

### Hook PreToolUse: `engine_analisa_diff.py`

```
Evento PreToolUse (antes de tool call)
    ↓
[AnalisadorDiff]
    ↓
- Extrai diff (git diff, arquivos locais)
- Analisa padrões (palavras-chave, extensões)
- Calcula score por motor
- Retorna motor + confiança
    ↓
Hook retorna sugestão formatada
    ↓
Injetado no cartão via "Sugestão de motor:"
```

### Classificador por Tipo

| Motor | Padrões-chave | Exemplo |
|---|---|---|
| **revisar-codigo** | try, except, null, injection, security, encoding | `try: db.query() except: handle()` |
| **otimizar-performance** | query, join, index, cache, algorithm, loop | `SELECT * JOIN orders` |
| **arquitetar-sistema** | abstract, interface, design, pattern, layer | `abstract class Repository` |
| **materializar-ideia** | def, function, endpoint, handler, test, assert | `def authenticate(user, pass)` |
| **diagramar** | flow, sequence, er, entity, relationship, model | Documentação markdown |

---

## Tarefas

### ✅ Tarefa 1: Criar Analisador de Diff
- [x] `hooks/engine_analisa_diff.py` criado
- [x] Classe `AnalisadorDiff` com 5 motores
- [x] Scoring via word boundaries (evita falsos positivos)
- [x] Método `gerar_sugestao()` para formatação

### ✅ Tarefa 2: Testes Unitários
- [x] `ferramentas/tests/test_fase3_analisa_diff.py` criado
- [x] 8 testes cobrindo: 5 motores + vazio + scores + formatação
- [x] **Resultado: 8/8 PASSARAM** ✅

### ⏳ Tarefa 3: Integração com Hook Existente
- [ ] Modificar `hooks/engine_contexto.py` (v3)
- [ ] Injetar sugestão de motor após invariantes
- [ ] Respeitar teto de 50 linhas

### ⏳ Tarefa 4: Teste Automatizado
- [ ] `FASE3-AUTOMATE.py` (simula 3 cycles)
- [ ] Valida sugestão de motor por tipo

### ⏳ Tarefa 5: Documentação
- [x] `FASE3-PLANO.md` (este arquivo)
- [ ] `FASE3-TESTE-MANUAL.md` (teste em ENGINE real)

---

## Próximo Passo

**Criar FASE3-TESTE-MANUAL.md** e **engine_contexto_v3.py** com integração do analisador.

---

## Checklist de Aceite

- [ ] Analisador detesta todos 5 motores corretamente
- [ ] Scores equilibrados (sem motor dominante)
- [ ] Sugestão aparece no cartão (fase PLANO em diante)
- [ ] Teto respeitado (≤50 linhas)
- [ ] Teste manual aprovado com ENGINE real
- [ ] Commit de Fase 3

---

Gerado: 2026-07-31  
Tempo estimado restante: ~1 hora
