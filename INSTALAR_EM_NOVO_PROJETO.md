# Como Usar o ENGINE em um Novo Projeto

## TL;DR (2 passos)

```bash
# 1. Clone o motor em um lugar permanente
git clone https://github.com/GuilhermeBrancalhao/MOTOR-INTELIGENTE-DE-REVISAO-DE-CODIGO.git ~/motor-engine

# 2. No seu novo projeto, crie um symlink
ln -s ~/motor-engine .claude/plugins/engine

# 3. Pronto! Agora você pode usar
/construir "seu objetivo"
```

---

## Passo-a-Passo (Windows/Mac/Linux)

### 1. Clone o Repositório do ENGINE (uma única vez)

```bash
# Coloque em um lugar que você não vai deletar
# (recomendo home directory ou /opt)

git clone https://github.com/GuilhermeBrancalhao/MOTOR-INTELIGENTE-DE-REVISAO-DE-CODIGO.git ~/motor-engine

# Verifique que funcionou
ls ~/motor-engine/skills/construir/SKILL.md
```

### 2. Para CADA novo projeto

```bash
# Entre no diretório do seu novo projeto
cd ~/novo-projeto

# Crie a pasta .claude/plugins se não existir
mkdir -p .claude/plugins

# Crie um symlink para o motor
# (assim ele sempre usa a versão mais nova)
ln -s ~/motor-engine .claude/plugins/engine

# Verifique
ls -la .claude/plugins/engine
```

### 3. Pronto! Agora você pode usar:

```bash
# No Claude Code, digite:
/construir "Criar API REST de pedidos em Node.js"

# Ou qualquer dos seus objetivos
/construir "App de notas com React"
/construir "Dashboard de vendas"
/construir "Revisar e otimizar autenticação"
```

---

## Alternativa: Copiar em vez de Symlink

Se não quiser symlink:

```bash
# Clone do repositório
git clone https://github.com/GuilhermeBrancalhao/MOTOR-INTELIGENTE-DE-REVISAO-DE-CODIGO.git

# Copie para o novo projeto
cp -r MOTOR-INTELIGENTE-DE-REVISAO-DE-CODIGO .claude/plugins/engine

# Pronto!
/construir "seu objetivo"
```

⚠️ **Problema:** Cada projeto tem uma cópia. Atualizações do ENGINE não chegam automaticamente.  
✅ **Vantagem:** Funciona mesmo se deletar a cópia original.

---

## Comandos Disponíveis

```bash
# Iniciar um novo ciclo
/construir "seu objetivo"

# Ver status
/engine status

# Avançar para próxima fase
/engine fase PLANO
/engine fase BUILD
/engine fase TESTE
/engine fase REVISAO
/engine fase DOC
/engine fase ENTREGA

# Pausar e retomar depois
/engine desligar
/engine retomar  # na sessão nova

# Consultar documentação
/consultar "07-PROMPT-ENGINE"
/consultar "12-MEMORY"
/consultar "31-TESTING"
```

---

## O que o `/construir` faz

Internamente, é um alias para:

```bash
/engine "seu objetivo"
```

Mas é mais amigável — você digita `/construir` em vez de lembrar que é `/engine`.

---

## Cheklist: Pronto?

- [ ] Clonei o repositório em `~/motor-engine`
- [ ] Criei `.claude/plugins/engine` (symlink ou cópia) no novo projeto
- [ ] Digitei `/construir "meu objetivo"` no Claude Code
- [ ] Apareceu o cartão do ENGINE com a Fase DESCOBERTA
- [ ] Estou seguindo as 8 fases

**✅ Pronto pra construir!**
