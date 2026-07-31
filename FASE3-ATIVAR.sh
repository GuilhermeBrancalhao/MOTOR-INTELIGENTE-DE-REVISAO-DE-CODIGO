#!/bin/bash
# FASE 3: Ativar engine_contexto_v3.py em produção

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$REPO_DIR/hooks"
ORIGINAL="$HOOKS_DIR/engine_contexto.py"
V3="$HOOKS_DIR/engine_contexto_v3.py"
BACKUP="$HOOKS_DIR/engine_contexto.py.backup-fase2"

echo "=== FASE 3: Ativar Hook V3 ==="
echo "Repositório: $REPO_DIR"
echo ""

# Verificar que arquivos existem
if [ ! -f "$ORIGINAL" ]; then
  echo "❌ ERRO: $ORIGINAL não encontrado"
  exit 1
fi

if [ ! -f "$V3" ]; then
  echo "❌ ERRO: $V3 não encontrado"
  exit 1
fi

if [ ! -f "$BACKUP" ]; then
  echo "❌ ERRO: $BACKUP não encontrado (Fase 2 não foi executada?)"
  exit 1
fi

# Fazer backup do v2
BACKUP_V2="$HOOKS_DIR/engine_contexto.py.backup-fase2-v2"
cp "$ORIGINAL" "$BACKUP_V2"
echo "✓ Backup do V2 criado: $BACKUP_V2"

# Substituir original por v3
cp "$V3" "$ORIGINAL"
echo "✓ $ORIGINAL substituído por versão v3"

# Verificar que está ativo
if grep -q "def _analisar_e_sugerir_motor" "$ORIGINAL"; then
  echo "✓ Verificado: nova função detectada em $ORIGINAL"
else
  echo "❌ ERRO: Substituição falhou"
  exit 1
fi

echo ""
echo "=== STATUS ==="
echo "✅ Hook v3 ATIVO com sugestão automática de motor"
echo ""
echo "Próximos passos:"
echo "1. Rodar testes: python3 FASE3-AUTOMATE.py"
echo "2. Testar com ENGINE real"
echo "3. Validar que sugestão de motor aparece"
echo "4. Relatar: OK ou problemas"
echo ""
echo "Para reverter: cp $BACKUP_V2 $ORIGINAL"
