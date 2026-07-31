---
name: construir
description: Ativa o ENGINE para construir um novo projeto do zero. Use "/construir" seguido do seu objetivo.
---

# /construir — Ativar ENGINE Automaticamente

Um comando simples para começar um novo projeto com o ENGINE.

## Como usar

```bash
/construir "Seu objetivo aqui"
```

## Exemplos

```bash
/construir "Criar API REST de pedidos em Node.js"
/construir "App de todo list em React"
/construir "Dashboard de vendas em Vue.js"
/construir "Revisar e otimizar autenticação OAuth2"
```

## O que acontece

1. O ENGINE liga automaticamente em **DESCOBERTA**
2. Aparece um cartão mostrando:
   - Fase atual
   - Seu objetivo
   - 5 motores (aparecem conforme você avança)
   - 3 volumes com documentação
   - 5 invariantes (regras do projeto)

3. Você segue as 8 fases naturalmente:
   ```
   DESCOBERTA → ANALISE → PLANO → BUILD → TESTE → REVISAO → DOC → ENTREGA
   ```

## Fases (resumo)

| Fase | O que fazer |
|---|---|
| **DESCOBERTA** | Pesquisar, entender o que você quer |
| **ANALISE** | Investigar o que já existe |
| **PLANO** | Decidir stack, arquitetura, estrutura |
| **BUILD** | Código |
| **TESTE** | Valida o que foi feito |
| **REVISAO** | Olha de novo pra achar erros |
| **DOC** | Documenta tudo |
| **ENTREGA** | Pronto pro prod |

## Motores Disponíveis (quando aparecerem)

- **revisar-codigo** — encontra bugs, segurança, confiabilidade
- **otimizar-performance** — acha gargalos (queries lentas, loops aninhados, falta de cache)
- **arquitetar-sistema** — define padrões, estrutura, como organizar o código
- **materializar-ideia** — transforma conceito em código rodando
- **diagramar** — cria diagramas de arquitetura

## Volumes (Consulta Rápida)

A qualquer momento, rode:

```bash
/consultar "07-PROMPT-ENGINE"  # Técnicas de prompting
/consultar "12-MEMORY"         # State, cache, persistência
/consultar "31-TESTING"        # Padrões de teste
```

## 5 Invariantes (Regras do Projeto)

Aparecem em todo cartão. Respeite sempre:

1. **Nunca afirmar sucesso sem ter olhado**  
   Rodou? Cola saída. Não rodou? Diz que não rodou.

2. **Nunca ajustar teste pra código passar**  
   Teste é contrato. Código errado = código errado.

3. **Nunca inventar** (arquivo, API, número, regra)  
   Sem evidência, é pendência aberta.

4. **Nunca tocar fora do escopo**  
   Se disse "vou fazer X", não faz Y/Z sem avisar.

5. **Toda decisão técnica com justificativa**  
   Nunca "usei Redis porque sim". Sempre "porque: X (perf), Y (simples)".

## Avanço Manual de Fases

```bash
/engine fase PLANO
/engine fase BUILD
/engine fase TESTE
/engine fase REVISAO
/engine fase DOC
/engine fase ENTREGA
```

## Ver Status

```bash
/engine status
```

## Fechar o Ciclo

```bash
/engine desligar
```

---

**Resumo:** `/construir "seu objetivo"` = ENGINE rodando, pronto pra construir.
