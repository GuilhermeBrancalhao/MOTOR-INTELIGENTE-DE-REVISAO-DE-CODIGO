#!/bin/bash
# FASE 2: Ativar engine_contexto_v2.py em produção

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR="$REPO_DIR/hooks"
ORIGINAL="$HOOKS_DIR/engine_contexto.py"
V2="$HOOKS_DIR/engine_contexto_v2.py"
BACKUP="$HOOKS_DIR/engine_contexto.py.backup-fase1"

echo "=== FASE 2: Ativar Hook V2 ==="
echo "Repositório: $REPO_DIR"
echo ""

# Verificar que arquivos existem
if [ ! -f "$ORIGINAL" ]; then
  echo "❌ ERRO: $ORIGINAL não encontrado"
  exit 1
fi

if [ ! -f "$V2" ]; then
  echo "❌ ERRO: $V2 não encontrado"
  exit 1
fi

# Fazer backup
if [ -f "$BACKUP" ]; then
  echo "✓ Backup já existe em $BACKUP"
else
  cp "$ORIGINAL" "$BACKUP"
  echo "✓ Backup criado: $BACKUP"
fi

# Substituir original por v2
cp "$V2" "$ORIGINAL"
echo "✓ $ORIGINAL substituído por versão v2"

# Verificar que está ativo
if grep -q "def montar_cartao_estendido" "$ORIGINAL"; then
  echo "✓ Verificado: nova função detectada em $ORIGINAL"
else
  echo "❌ ERRO: Substituição falhou"
  exit 1
fi

echo ""
echo "=== STATUS ==="
echo "✅ Hook v2 ATIVO"
echo ""
echo "Próximos passos:"
echo "1. Testar com ENGINE real: /engine"
echo "2. Navegar pelas fases até DOC"
echo "3. Validar que motor aparece no cartão"
echo "4. Relatar: OK ou problemas"
echo ""
echo "Para reverter: cp $BACKUP $ORIGINAL"
