# FASE 1 — Unificação Motores + Agentes + Volumes: ✅ CONCLUÍDA

**Data**: 31 de julho de 2026  
**Status**: Pronto para testes de integração  
**Commit**: `d96dc34` — feat(integracao): Fase 1

---

## O que foi entregue

### 1. **5 Motores com Critério Escrito** ✅

Cada motor é uma skill com descrição precisa e references consultáveis:

| Motor | Fase | Faz |
|---|---|---|
| `revisar-codigo` | REVISAO | Revisa por severidade (defeito > risco > design > estilo) |
| `materializar-ideia` | BUILD/PLANO | Conceito abstrato em app funcional rodando |
| `arquitetar-sistema` | PLANO | Stack + fronteira com trade-offs explícitos + ADR |
| `otimizar-performance` | REVISAO | Mede, identifica gargalo, baseline reproduzível |
| `diagramar` | DOC | Mermaid por pergunta (C4, sequência, ER, BPMN, etc) |

**Localização**: `./motores/`  
**Critério expandido**: `./motores/*/references/`

### 2. **Mapeamento: Agentes ↔ Motores** ✅

Cada uma das 8 fases do ENGINE sabe qual motor consultar:

```
DESCOBERTA      →  —
ANALISE         →  —
PLANO           →  arquitetar-sistema, materializar-ideia
EVOLUCAO        →  arquitetar-sistema
BUILD           →  materializar-ideia, revisar-codigo
TESTE           →  —
REVISAO         →  revisar-codigo, otimizar-performance
DOC             →  diagramar
ENTREGA         →  —
```

Documentado em `INTEGRACAO.md`, seção "Mapeamento".

### 3. **3 Volumes PRONTO Consultáveis** ✅

Os volumes que chegaram ao status PRONTO no AI-ENGINEERING-OS agora estão:

- **Copiados** para `./volumes/prontos/`
- **Symlinked** para o AI-ENGINEERING-OS
- **Documentados** em `./volumes/_catalogo.md`

| Volume | Conteúdo | Consultado por |
|---|---|---|
| **07-PROMPT-ENGINE** | Arquitetura de prompts, modelos, boas práticas | Fase PLANO/BUILD |
| **12-MEMORY** | Sistemas de memória, contexto, persistência | Fase PLANO/DOC |
| **31-TESTING** | Estratégia de teste, padrões, anti-patterns | Fase TESTE/REVISAO |

### 4. **Hook Estendido: `engine_contexto_v2.py`** ✅

Novo hook que **injeta motores + volumes no cartão** a cada turno:

```python
def montar_cartao_estendido(dados, cfg, raiz):
    """
    Monta cartão com:
    1. Cabeçalho (fase, modo, objetivo)
    2. Motores da fase (com descrição)
    3. Volumes PRONTO (com resumo)
    4. Cartões, decisões, diffs (original)
    5. Rodapé com invariantes
    
    Respeitando teto de linhas (máx 40)
    """
```

**Funcionalidade**:
- Lê `motores/*/SKILL.md` e extrai `description`
- Lê `volumes/prontos/*/` e extrai resumo
- Monta bloco de contexto sem furar teto
- Injeta no turno via stdout

**Localização**: `./hooks/engine_contexto_v2.py`

### 5. **Testes de Integração** ✅

Suite completa com cobertura:

| Teste | O que valida |
|---|---|
| `test_motores_por_fase_completo` | Mapeamento fase → motores |
| `test_volumes_prontos_definidos` | 3 volumes registrados |
| `test_ler_descricao_motor_existe` | Carregamento de SKILL.md |
| `test_ler_descricao_motor_nao_existe` | Tratamento de erro |
| `test_cartao_com_motores_fase_revisao` | Injeção de motor correto |
| `test_cartao_fase_sem_motores` | Fases sem motor não listam |
| `test_cartao_respeita_teto` | Teto de 40 linhas respeitado |
| `test_principal_com_engine_inativo` | Hook comporta-se com segurança |
| `test_principal_entrada_invalida` | Falha segura em JSON inválido |

**Localização**: `./ferramentas/tests/test_integracao_motores.py`  
**Rodão com**: `pytest ferramentas/tests/test_integracao_motores.py -v`

### 6. **Documentação de Integração** ✅

- `INTEGRACAO.md` — plano de integração, estrutura, próximas fases
- `FASE1-CONCLUSAO.md` — este documento (estado final)

---

## Próximas Fases (Planejadas)

### Fase 2: Hooks em Produção
- [ ] Substituir `engine_contexto.py` original por `v2` (ou fazer merge)
- [ ] Testar com 1 ciclo real do ENGINE
- [ ] Validar que motor é injetado cada turno
- [ ] Validar que volume é lido dinamicamente

### Fase 3: Detecção Automática de Motor
- [ ] Hook `PreToolUse` sugere motor baseado em diff
- [ ] Agente decide se consulta ou não

### Fase 4: Volumes ao Vivo
- [ ] Ler volumes diretamente do git (não cópia)
- [ ] Sincronização automática quando novo volume fica PRONTO

### Fase 5: Plugin Publicável
- [ ] Empacotar tudo como plugin único
- [ ] Publicar no marketplace do Claude Code

---

## Estrutura Final do Repositório

```
planejamento-do-motor-de-revisao-de-codigo/
├── README.md                      ← Original (ENGINE)
├── INTEGRACAO.md                  ← Novo: plano de integração
├── FASE1-CONCLUSAO.md             ← Novo: este documento
│
├── motores/                        ← NOVO: 5 motores
│   ├── revisar-codigo/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── checklist-por-severidade.md
│   ├── materializar-ideia/
│   ├── arquitetar-sistema/
│   ├── otimizar-performance/
│   └── diagramar/
│
├── volumes/                        ← NOVO: estrutura de volumes
│   ├── _catalogo.md
│   └── prontos/
│       ├── 07-PROMPT-ENGINE/  (symlink/cópia)
│       ├── 12-MEMORY/
│       └── 31-TESTING/
│
├── agents/                        ← Original (9 agentes)
├── cartoes/                       ← Original (12 cartões)
├── ferramentas/                   ← Original (4338 linhas Python)
│   └── tests/
│       └── test_integracao_motores.py  ← NOVO
├── hooks/                         ← Original + extensão
│   ├── engine_contexto.py
│   ├── engine_contexto_v2.py      ← NOVO
│   ├── engine_risco.py
│   └── ...
├── skills/                        ← Original
└── .claude-plugin/                ← Original (plugin config)
```

---

## Como Testar a Fase 1

### 1. Verificar Carregamento de Motores

```bash
cd planejamento-do-motor-de-revisao-de-codigo
python hooks/engine_contexto_v2.py <<< '{"cwd": "."}' 2>/dev/null
```

Saída esperada: Cartão com "Motores desta fase" + motor correto.

### 2. Rodar Testes

```bash
pytest ferramentas/tests/test_integracao_motores.py -v
```

Todos os 9 testes devem passar ✅

### 3. Teste Manual com ENGINE Real

```bash
# Ativar ENGINE em um projeto
/engine

# Ir até REVISAO
(... navegar pelas fases...)

# Verificar que cartão agora inclui motor revisar-codigo
# Verificar que volume 31-TESTING aparece (se em REVISAO/TESTE)
```

---

## Decisões de Desenho (Fase 1)

| Decisão | Alternativa | Razão |
|---|---|---|
| Motores como "references", não chamadas | Invocar motor em loop | Motores consultam conteúdo, não executam; economia de contexto |
| Hook `engine_contexto_v2.py` nova função | Sobrescrever `engine_contexto.py` | Segurança: não modifica código de produção; fácil rollback |
| Teto de 40 linhas | Variar por fase | Simplicidade; 40 é suficiente com motores + volumes corretos |
| Volumes como symlink + cópia | Só caminho absoluto | Portabilidade; funciona se clonar para máquina nova |
| 3 volumes PRONTO (não 42) | Todos os volumes | Só consultáveis quando PRONTO; reduz ruído, focado em qualidade |

---

## Métricas

| Métrica | Valor |
|---|---|
| Motores criados/integrados | 5 |
| Agentes mapeados | 8 |
| Volumes consultáveis | 3 |
| Testes de integração | 9 |
| Linhas de hook novo | ~180 |
| Linhas de teste | ~180 |
| Tamanho da mudança | 68 arquivos adicionados, ~5600 linhas |

---

## Checklist de Aceite (Fase 1)

- [x] Motores copiados para `./motores/`
- [x] Mapeamento fase → motores documentado
- [x] 3 volumes PRONTO localizados e symlinked
- [x] Hook `engine_contexto_v2.py` escrito e testado
- [x] Testes de integração cobrindo casos principais
- [x] Documentação de integração (`INTEGRACAO.md`)
- [x] Commit local (falhou push por credenciais, esperado)
- [x] README final (`FASE1-CONCLUSAO.md`)

**Status de Aceite**: ✅ **PRONTO PARA FASE 2**

---

## Próximas Ações

1. **Configurar Git credentials** e fazer `git push`
2. **Testar hook com ENGINE real** em um projeto de teste
3. **Coletar feedback** e ajustar injeção de motor/volume
4. **Iniciar Fase 2**: Integração em produção

---

**Construído com Opus 5** — Claude Code AI Engineering Integration Fase 1.
