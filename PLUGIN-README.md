# AI Engineering Motor (ENGINE) - Claude Code Plugin

**Version**: 4.0.0  
**Status**: ✅ Production Ready  
**License**: MIT

---

## O Que é ENGINE?

ENGINE é um **motor inteligente de engenharia** para Claude Code que automatiza tarefas de revisão, otimização, arquitetura e documentação de código.

Integra-se seamlessly com seu workflow Claude Code, oferecendo:
- 🔍 **Revisão de Código** automática (segurança, confiabilidade)
- ⚡ **Otimização de Performance** (queries, algoritmos, cache)
- 🏗️ **Decisões de Arquitetura** (padrões, boundaries)
- 💡 **Materialização de Ideias** (de conceito a implementação)
- 📊 **Diagramação** (C4, ER, sequência, arquitetura)

---

## Instalação

### Via Claude Code

```bash
/plugin install ai-engineering-os-engines
```

### Manual

```bash
git clone https://github.com/AlphaContabilidade/planejamento-do-motor-de-revisao-de-codigo.git
cd planejamento-do-motor-de-revisao-de-codigo
# Configurar em .claude/plugins.json
```

---

## Como Usar

### 1. Inicializar ENGINE

```bash
/engine "Seu objetivo aqui"
```

Exemplo:
```bash
/engine "Implementar e otimizar módulo de autenticação"
```

### 2. Navegar pelas Fases

O ENGINE guia você através de **8 fases**:

```
DESCOBERTA  → ANALISE → PLANO → EVOLUCAO → BUILD → TESTE → REVISAO → DOC
```

Em cada fase, você recebe:
- 📋 **Motores**: ferramentas relevantes para a fase
- 💡 **Sugestões**: detecção automática por padrão de código
- 📚 **Volumes**: documentação consultável
- 📊 **Cartão**: resumo de estado e invariantes

### 3. Usar um Motor

Quando em uma fase com um motor disponível:

```bash
/revisar-codigo
/otimizar-performance
/arquitetar-sistema
/materializar-ideia
/diagramar
```

### 4. Consultar Volumes

Qualquer volume listado no cartão é consultável:

```bash
/consultar "07-PROMPT-ENGINE"
/consultar "12-MEMORY"
/consultar "31-TESTING"
```

---

## Motores Disponíveis

### 🔍 revisar-codigo
Identifica problemas de segurança, confiabilidade e práticas recomendadas.

**Detecta**:
- Try/except, null checks
- SQL injection, XSS, CSRF
- Deadlocks, race conditions
- Encoding issues
- Memory leaks

**Fases**: PLANO, BUILD, REVISAO

---

### ⚡ otimizar-performance
Encontra gargalos e sugere melhorias.

**Detecta**:
- Queries ineficientes
- Nested loops, algoritmos O(n²)
- Falta de índices
- Cache ausente
- Memory overhead

**Fases**: BUILD, REVISAO

---

### 🏗️ arquitetar-sistema
Define decisões arquiteturais e padrões.

**Define**:
- Fronteiras de serviço
- Padrões de design
- Camadas de arquitetura
- Dependências
- Trade-offs

**Fases**: PLANO, EVOLUCAO

---

### 💡 materializar-ideia
Transforma conceitos em implementações.

**Fases**:
1. Fixar conceito
2. Escolher stack
3. Implementar (inside-out)
4. Interface
5. Verificação

**Fases**: PLANO, BUILD

---

### 📊 diagramar
Cria diagramas de arquitetura.

**Tipos**:
- C4 (contexto, container, componente)
- Entity-Relationship
- Sequence
- State machine
- BPMN

**Fases**: DOC

---

## Volumes Consultáveis

### 07-PROMPT-ENGINE
Prompts curados para workflows de engenharia AI.
- Técnicas de prompting
- Padrões de instrução
- Exemplos de uso

### 12-MEMORY
Sistemas de memória e persistência de estado.
- Memória em Claude
- State machines
- Cache patterns
- Context management

### 31-TESTING
Estratégias e frameworks de teste.
- Unit testing
- Integration testing
- Test coverage
- Mocks e stubs

---

## Capacidades Avançadas

### Detecção Automática de Motor

ENGINE analisa seu código em tempo real:

```
Você escreve código com try/except
    ↓
ENGINE detecta padrão
    ↓
Sugere: "revisar-codigo (100%)"
```

### Volumes Dinâmicos

Crie novo volume sem editar código, com `_VOLUME.yml` marcando `status: PRONTO`:

```
volumes/prontos/99-MEU-NOVO-VOLUME/
  ├─ _VOLUME.yml       ← status: PRONTO (obrigatório — só volumes PRONTO aparecem)
  └─ 01-Introducao.md  ← capítulos numerados, ou README.md
```

O resumo mostrado no cartão vem do campo `escopo:` de `_VOLUME.yml`; sem ele, cai na
primeira linha não vazia do `README.md`.

Próxima execução ENGINE:
```
📚 Volumes PRONTO:
  • 07-PROMPT-ENGINE
  • 12-MEMORY
  • 31-TESTING
  • 99-MEU-NOVO-VOLUME ← Descoberto automaticamente!
```

### Cache Inteligente

Volumes descobertos em cache (TTL 300s) para performance.

Invalida automaticamente quando:
- Novo volume detectado
- Estrutura muda
- Cache expira

---

## Invariantes (Regras do ENGINE)

Essas 5 invariantes definem comportamento esperado:

1. **Nunca afirmar sucesso sem ter olhado**  
   Rodou? Cola a saída. Não rodou? Diz que não rodou.

2. **Nunca ajustar teste para código passar**  
   O teste é o contrato. Código que falha no teste foi errado.

3. **Nunca inventar (arquivo, API, número, regra)**  
   Sem evidência no código/sistema, é uma pendência.

4. **Nunca tocar fora do escopo**  
   Se o ciclo declara escopo, respeita.

5. **Toda decisão técnica sai com justificativa**  
   Nunca implementa sem explicar por quê.

---

## Configuração

### `.engine/config.json` no projeto hospedeiro (opcional)

Chaves fora desta lista são ignoradas e geram aviso no cartão — só o que está em
`ferramentas/config.py::PADRAO` pode ser sobreposto:

```json
{
  "porta_plano": true,
  "teto_cartao_linhas": 50,
  "padroes_segredo": [".env", "*.pem", "*.key"],
  "travado_extra": []
}
```

---

## Troubleshooting

### "Motor não aparece em minha fase"

Verify fase com `/engine` command. Motores aparecem apenas em fases designadas.

### "Volume não é descoberto"

Verifique que:
1. Está em `volumes/prontos/NOME/`
2. Tem `_VOLUME.yml` com `status: PRONTO` (sem esse arquivo, cai no fallback: `README.md` ou qualquer `.md`)
3. Estrutura é válida (não vazio)

### "Sugestão de motor incorreta"

ENGINE usa análise de padrão. Se incorreta:
1. Verifique diff tem palavras-chave esperadas
2. Pode ser por ambiguidade (múltiplos padrões)
3. Você pode ignorar e usar motor diferente

---

## Exemplos de Uso Real

### Exemplo 1: Implementar Feature

```
/engine "Implementar autenticação OAuth2"
  └─ PLANO: revisar arquitetar-sistema + materializar-ideia
  └─ BUILD: implementar, ENGINE sugere revisar-codigo (detectou try/except)
  └─ REVISAO: otimizar queries, revisar segurança
  └─ DOC: diagramar fluxo de autenticação
```

### Exemplo 2: Otimizar Performance

```
/engine "Otimizar queries N+1 em pedidos"
  └─ BUILD: implementar join, ENGINE sugere otimizar-performance
  └─ TESTE: validar performance (antes/depois)
  └─ REVISAO: revisar, otimizar cache
  └─ DOC: documentar padrão de query otimizada
```

---

## Contribuindo

Para contribuir:

```bash
git clone https://github.com/AlphaContabilidade/planejamento-do-motor-de-revisao-de-codigo.git
# Criar feature branch
# Adicionar motores/volumes
# Testar
# Submit PR
```

---

## Changelog

### v4.0.0 (2026-07-31)
- ✨ Volumes dinâmicos (auto-discovery)
- ✨ Detecção automática de motor
- ✨ Cache inteligente (TTL 300s)
- 🐛 Corrigido: truncamento de resumos
- 📚 Documentação completa

### v3.0.0 (2026-07-31)
- ✨ Sugestão automática via diff
- ✨ 5 motores funcionais
- 🐛 Teto de 50 linhas garantido

### v2.0.0 (2026-07-31)
- ✨ Motores por fase
- ✨ Volumes consultáveis
- 📚 Invariantes

### v1.0.0 (2026-07-31)
- Initial release

---

## Suporte

- 📖 [Documentação Completa](docs/)
- 🐛 [Reportar Issue](https://github.com/AlphaContabilidade/planejamento-do-motor-de-revisao-de-codigo/issues)
- 💬 [Discussões](https://github.com/AlphaContabilidade/planejamento-do-motor-de-revisao-de-codigo/discussions)

---

## Licença

MIT - Veja [LICENSE](LICENSE) para detalhes.

---

**Made with ❤️ for Claude Code Engineers**

```
ENGINE v4.0.0 - AI Engineering Motor
Status: ✅ Production Ready
```
