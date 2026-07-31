# FASE 2: Teste Manual com ENGINE Real

**Data**: 31 de julho de 2026  
**Hook ativo**: ✅ engine_contexto_v2.py (substituiu original)  
**Backup**: hooks/engine_contexto.py.backup-fase1

---

## Plano de Teste

Você vai simular um ciclo ENGINE real navegando pelas fases manualmente.

### Setup

1. **Criar projeto de teste** (ou usar um existente)
   ```bash
   mkdir -p ~/test-engine
   cd ~/test-engine
   git init
   echo "# Test Project" > README.md
   ```

2. **Copiar ENGINE como estrutura** (ou instalar como plugin via `/plugin install`)
   - O ENGINE está em `~/planejamento-do-motor-de-revisao-de-codigo/`
   - Hook ativo: `hooks/engine_contexto.py` (agora v2)

3. **Ativar o ENGINE**
   ```bash
   /engine "Revisar e otimizar módulo de autenticação"
   ```
   
   Esperado: Cartão aparece com:
   - Fase: DESCOBERTA
   - Objetivo: Revisar e otimizar...
   - Volumes PRONTO: 07-PROMPT-ENGINE, 12-MEMORY, 31-TESTING
   - Invariantes (5 linhas)
   - ≤50 linhas total ✓

---

## Fases a Testar

### Fase 1: DESCOBERTA

**O que fazer**:
- Ativar `/engine "Revisar e otimizar módulo de autenticação"`
- Responder perguntas do descobridor

**Validar**:
- [ ] Cartão aparece
- [ ] Fase = DESCOBERTA
- [ ] NÃO há motores listados (correto, descoberta não tem)
- [ ] Volumes aparecem
- [ ] ≤50 linhas

**Resultado esperado**:
```
== ENGINE ativo ==
Fase: DESCOBERTA   Modo: normal
Objetivo: Revisar e otimizar módulo...

📚 Volumes PRONTO (consultáveis):
  • 07-PROMPT-ENGINE: Introdução
  • 12-MEMORY: Introdução
  • 31-TESTING: Introdução

Invariantes:
1. Nunca afirmar sucesso...
```

---

### Fase 2: PLANO

**Como chegar**:
- Responda o descobridor
- Cartografo mapeia (automático)
- Chegue em PLANO (aproximadamente turno 3-4)

**Validar**:
- [ ] Cartão aparece
- [ ] Fase = PLANO
- [ ] **Motores listados**:
  - `📋 Motores desta fase:`
  - `  • arquitetar-sistema`
  - `  • materializar-ideia`
- [ ] Volumes aparecem
- [ ] Cartões (python, pytest)
- [ ] ≤50 linhas

**Resultado esperado**:
```
== ENGINE ativo ==
Fase: PLANO   Modo: normal
Objetivo: Revisar e otimizar...

📋 Motores desta fase:
  • arquitetar-sistema
  • materializar-ideia

📚 Volumes PRONTO:
  • 07-PROMPT-ENGINE...
  • 12-MEMORY...
  • 31-TESTING...

Cartões: python, pytest
Decisões:
  - [arquitetura proposta]
```

---

### Fase 3: BUILD

**Validar**:
- [ ] Fase = BUILD
- [ ] **Motores**:
  - `  • materializar-ideia`
  - `  • revisar-codigo`
- [ ] Volumes aparecem
- [ ] Diffs pendentes listados
- [ ] ≤50 linhas

---

### Fase 4: REVISAO

**Validar**:
- [ ] Fase = REVISAO
- [ ] **Motores**:
  - `  • revisar-codigo`
  - `  • otimizar-performance`
- [ ] **Volume 31-TESTING aparece** (crítico: teste strategy)
- [ ] ≤50 linhas

---

### Fase 5: DOC

**Validar**:
- [ ] Fase = DOC
- [ ] **Motor**:
  - `  • diagramar`
- [ ] Volumes aparecem
- [ ] ≤50 linhas

---

## Checklist de Validação

Preencha conforme avança:

### Hook V2 Ativo
- [x] `engine_contexto.py` substituído
- [x] `montar_cartao_estendido` detectada
- [x] Backup criado

### Cartão Injetado
- [ ] Fase DESCOBERTA mostra
- [ ] Fase PLANO mostra motores arquitetar + materializar
- [ ] Fase BUILD mostra motores materializar + revisar
- [ ] Fase REVISAO mostra motores revisar + otimizar
- [ ] Fase DOC mostra motor diagramar

### Volumes Consultáveis
- [ ] 07-PROMPT-ENGINE aparece (todas fases)
- [ ] 12-MEMORY aparece (todas fases)
- [ ] 31-TESTING aparece (especialmente REVISAO)

### Teto de Linhas
- [ ] DESCOBERTA ≤50 linhas
- [ ] PLANO ≤50 linhas
- [ ] BUILD ≤50 linhas
- [ ] REVISAO ≤50 linhas
- [ ] DOC ≤50 linhas

### Invariantes
- [ ] 5 invariantes aparecem em cada cartão
- [ ] Ordem mantida
- [ ] Legível

---

## O que Relatar

Depois de testar, responda:

1. **Hook funcionou?** (Sim/Não)
   - Se Não: qual foi o erro?

2. **Motores apareceram nas fases certas?** (Sim/Não)
   - Se Não: quais fases tiveram problema?

3. **Volumes apareceram?** (Sim/Não)
   - Se Não: algum ausente?

4. **Teto foi respeitado?** (Sim/Não)
   - Se Não: qual fase ultrapassou 50?

5. **Cartão era útil/legível?** (Comentário livre)
   - Texto muito denso?
   - Informação importante faltando?
   - Algo que deveria ser removido?

6. **Problemas encontrados?**
   - Erros na console?
   - Comportamento inesperado?
   - Hook quebrou em algum turno?

---

## Revert (se necessário)

Se algo der errado:

```bash
cd ~/planejamento-do-motor-de-revisao-de-codigo
cp hooks/engine_contexto.py.backup-fase1 hooks/engine_contexto.py
```

Hook voltará ao original (sem motores/volumes).

---

## Próximas Ações

**Se tudo passar**:
→ Documentar em FASE2-RESULTADO.md  
→ Commit da Fase 2  
→ Iniciar Fase 3 (Detecção Automática)

**Se houver problemas**:
→ Coletar feedback  
→ Ajustar engine_contexto_v2.py  
→ Testar novamente

---

**Boa sorte! Reporte os resultados aqui depois.** 🚀
