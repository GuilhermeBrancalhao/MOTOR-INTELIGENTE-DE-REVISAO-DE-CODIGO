# Integração: ENGINE + Motores + Volumes

**Data**: 2026-07-31  
**Status**: Fase 1 em execução  
**Objetivo**: Unificar ENGINE (máquina + agentes) com Motores (critério) e Volumes (conhecimento)

---

## Mapeamento: Agentes ↔ Motores

| Fase | Agente(s) | Motores consultados | O que faz |
|---|---|---|---|
| **DESCOBERTA** | descobridor | — | Entende o pedido real, requisitos, restrições |
| **ANALISE** | cartografo | — | Mapeia projeto, detecta stack, carrega cartões |
| **PLANO** | arquiteto + designer | `arquitetar-sistema`, `materializar-ideia` | Decide stack com trade-offs, propõe visual |
| **BUILD** | implementador | `materializar-ideia` (se novo), `revisar-codigo` (auto-review) | Escreve código completo, valida |
| **TESTE** | testador | — | Escreve teste, roda, reporta saída |
| **REVISAO** | revisor + sentinela | `revisar-codigo`, `otimizar-performance` | Revisa código, segurança, performance |
| **DOC** | documentador | `diagramar` | Gera docs, ADRs, diagramas |
| **ENTREGA** | — | — | Fecha ciclo, gera relatório |

---

## Estrutura de Arquivos

### Hoje (ENGINE)

```
planejamento-do-motor-de-revisao-de-codigo/
├── agents/              ← 9 agentes de papel
├── cartoes/             ← 12 cartões de tecnologia
├── ferramentas/         ← 4338 linhas Python
├── hooks/               ← 5 hooks (Python)
├── skills/engine/       ← 1 skill de entrada
└── INTEGRACAO.md        ← Este arquivo (novo)
```

### Adicionar (Integração)

```
planejamento-do-motor-de-revisao-de-codigo/
├── motores/             ← 5 motores com critério (NOVO)
│   ├── revisar-codigo/
│   ├── materializar-ideia/
│   ├── arquitetar-sistema/
│   ├── otimizar-performance/
│   └── diagramar/
├── volumes/             ← Link aos volumes do acervo de conhecimento (NOVO)
│   ├── _catalogo.md
│   └── prontos/         ← 3 volumes PRONTO consultáveis
│       ├── 07-PROMPT-ENGINE/
│       ├── 12-MEMORY/
│       └── 31-TESTING/
├── hooks/
│   ├── engine_contexto.py   ← Modificar: injeta motor + volume
│   ├── engine_gate.py
│   ├── engine_risco.py
│   ├── engine_salvar.py
│   ├── engine_trilha.py
│   └── hooks.json
└── INTEGRACAO.md
```

---

## O que muda

### 1. Motores como referências

Cada agente recebe um bloco no cartão de contexto injetado:

```
## REFERENCIAS DESTE AGENTE

- Motor: revisar-codigo
  Checklist de severidade, critérios por domínio
  File: motores/revisar-codigo/references/checklist-por-severidade.md

- Volume: 31-TESTING (PRONTO)
  Estratégia de teste, padrões, anti-patterns
  File: volumes/prontos/31-TESTING/
```

O hook `engine_contexto.py` carrega os motores + volumes relevantes na fase atual e injeta.

### 2. Detecção automática de motor

Quando o agente `revisor` recebe um diff, ele automaticamente:

1. Lê o diff
2. Detecta a linguagem/domínio
3. Consulta `motores/revisar-codigo/SKILL.md` para o checklist
4. Consulta `volumes/prontos/31-TESTING/` para padrões de teste se aplicável
5. Reporta por severidade

Isso não é uma invocação de motor — é uma **consulta de referência** dentro do agente.

### 3. Volume consultável dinamicamente

Hook `engine_contexto.py` antes de cada turno:

```python
# Pseudocódigo
fase_atual = estado['fase']
cartoes = estado['cartoes']

referencias = []
referencias.extend(motores_por_fase[fase_atual])
referencias.extend(volumes_prontos)  # Sempre disponível

bloco_referencias = gerar_bloco_contexto(referencias)
injeta_no_turno(bloco_referencias, max_linhas=60)
```

Isso garante que:
- O motor correto está acessível na fase certa
- Os volumes não somem em contexto resumido
- Crescimento é controlado (teto de 60 linhas)

---

## Implementação — 4 arquivos modificar/criar

### 1. `motores/` — Copiar dos skills (já pronto)

```bash
cp -r ~/.claude/skills/{revisar-codigo,materializar-ideia,arquitetar-sistema,otimizar-performance,diagramar} \
      planejamento-do-motor-de-revisao-de-codigo/motores/
```

### 2. `volumes/prontos/` — Link (symlink) aos 42 volumes

```
volumes/
├── _catalogo.md
└── prontos/
    ├── 07-PROMPT-ENGINE → /caminho/do/acervo/07-PROMPT-ENGINE/
    ├── 12-MEMORY → /caminho/do/acervo/12-MEMORY/
    └── 31-TESTING → /caminho/do/acervo/31-TESTING/
```

### 3. `hooks/engine_contexto.py` — Modificar

Adicionar função `carregar_referencias(fase, cartoes)`:

```python
def carregar_referencias(fase: str, cartoes: List[str]) -> str:
    """Carrega motores e volumes relevantes para a fase."""
    referencias = []
    
    # Motores por fase
    motores_por_fase = {
        "PLANO": ["arquitetar-sistema", "materializar-ideia"],
        "BUILD": ["materializar-ideia", "revisar-codigo"],
        "REVISAO": ["revisar-codigo", "otimizar-performance"],
        "DOC": ["diagramar"],
    }
    
    for motor in motores_por_fase.get(fase, []):
        ref = ler_motor(f"motores/{motor}/SKILL.md", max_linhas=20)
        referencias.append(ref)
    
    # Volumes prontos (sempre)
    for volume in ["07-PROMPT-ENGINE", "12-MEMORY", "31-TESTING"]:
        ref = ler_volume(f"volumes/prontos/{volume}/", max_linhas=15)
        referencias.append(ref)
    
    return "\n\n".join(referencias)
```

### 4. `ferramentas/detectar.py` — Estender

Adicionar função `detectar_motor(diff, fase)`:

```python
def detectar_motor(diff: str, fase: str) -> str:
    """Sugere qual motor consultar baseado no diff."""
    
    if fase == "REVISAO":
        # Revisor sempre consulta revisar-codigo
        return "revisar-codigo"
    
    if "performance" in diff.lower() or "lento" in diff.lower():
        return "otimizar-performance"
    
    if "arquitetura" in diff.lower() or "fronteira" in diff.lower():
        return "arquitetar-sistema"
    
    # Default
    return None
```

---

## Workflow de teste (Fase 1)

1. **Estrutura pronta**
   - [x] Motores em `motores/`
   - [x] Volumes em `volumes/prontos/`
   - [ ] Symlinks criados

2. **Hook modificado**
   - [ ] `engine_contexto.py` carrega referências
   - [ ] Teto de 60 linhas testado
   - [ ] Injeção de motor correto por fase

3. **Agentes testados**
   - [ ] `revisor` consulta `revisar-codigo` em REVISAO
   - [ ] `arquiteto` consulta `arquitetar-sistema` em PLANO
   - [ ] `implementador` consulta `materializar-ideia` em BUILD

4. **Teste de integração**
   - [ ] 1 ciclo completo com o ENGINE
   - [ ] Motor injetado em cada fase
   - [ ] Volume consultado corretamente
   - [ ] Relatório de fim de ciclo mostra motores usados

---

## Próximas fases (depois de Fase 1)

### Fase 2: Volumes consultáveis ao vivo
- Integração com git para ler volumes do repositório do acervo de conhecimento em tempo real
- Sincronização automática quando novo volume fica PRONTO

### Fase 3: Detecção automática de motor
- Hook `PreToolUse` sugere motor baseado no diff
- Agente decide se consulta ou não

### Fase 4: Plugin publicável
- Empacotar ENGINE + Motores + Volumes como plugin único
- Publicar no marketplace do Claude Code
