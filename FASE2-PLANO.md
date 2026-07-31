# FASE 2: Integração em Produção

**Data**: 31 de julho de 2026  
**Status**: EM EXECUÇÃO  
**Objetivo**: Ativar `engine_contexto_v2.py` em produção e validar ciclo real

---

## Tarefas

### 1. Setup do Hook em Produção ✅ (em execução)

**O que fazer**:
- [ ] Copiar `engine_contexto_v2.py` para substituir `engine_contexto.py`
- [ ] Atualizar `hooks.json` para usar novo hook
- [ ] Validar que hook pode ser invocado

**Por quê**: O hook original não injeta motores/volumes. V2 faz isso.

### 2. Testar com ENGINE em Projeto Real ⏳

**Setup**:
- Criar projeto de teste com estrutura mínima
- Clonar ENGINE como plugin (ou usar via ~/.claude/)
- Ativar `/engine` com um pedido

**Validar**:
- Cartão de estado aparece a cada turno ✅
- Motor correto aparece na fase atual ✅
- Volumes PRONTO listados ✅
- Teto de 50 linhas respeitado ✅

**Fases a testar**:
1. DESCOBERTA → sem motores, mas volumes aparecem
2. PLANO → motores arquitetar + materializar
3. BUILD → motores materializar + revisar
4. REVISAO → motores revisar + otimizar + volume 31-TESTING
5. DOC → motor diagramar

### 3. Coleta de Feedback ⏳

Durante o ciclo real:
- O motor informação é útil ou barulho?
- Volume 31-TESTING ajuda na fase REVISAO?
- Teto de 50 linhas está bom ou precisa ajuste?
- Falta algum motor em alguma fase?

### 4. Validação Final ⏳

- [ ] 1 ciclo completo executado (DESCOBERTA até ENTREGA)
- [ ] Motor injetado corretamente em cada fase
- [ ] Nenhum erro, falha ou comportamento inesperado
- [ ] Hook relata sucesso

---

## Checklist de Aceite: Fase 2

- [ ] `engine_contexto_v2.py` ativo
- [ ] 1 ciclo ENGINE real testado
- [ ] Motor injetado em cada fase corretamente
- [ ] Volumes aparecem
- [ ] Teto respeitado
- [ ] Feedback coletado
- [ ] Não há erros ou avisos
- [ ] Relatório de conclusão da Fase 2

**Status**: ✅ **PRONTO PARA FASE 3** (depois de todas as tarefas)

---

## Roadmap Simplificado

```
FASE 1 ✅
  └─ Motores integrados, testes unitários passam

FASE 2 (AGORA)
  └─ Hook em produção, ciclo real testado
  
FASE 3 (Próxima)
  └─ Detecção automática de motor

FASE 4 (Depois)
  └─ Volumes ao vivo (git sync)

FASE 5 (Final)
  └─ Plugin publicável
```

---

## Como Começar

1. **Ativar hook v2** — copiar arquivo
2. **Testar manualmente** — criar projeto, `/engine`, navegar fases
3. **Relatar** — OK ou problemas encontrados
