# FASE 2: Ativar engine_contexto_v2.py em produção (PowerShell)

$repo_dir = (Get-Item $PSScriptRoot).FullName
$hooks_dir = Join-Path $repo_dir "hooks"
$original = Join-Path $hooks_dir "engine_contexto.py"
$v2 = Join-Path $hooks_dir "engine_contexto_v2.py"
$backup = Join-Path $hooks_dir "engine_contexto.py.backup-fase1"

Write-Host "=== FASE 2: Ativar Hook V2 ===" -ForegroundColor Green
Write-Host "Repositório: $repo_dir"
Write-Host ""

# Verificar que arquivos existem
if (-not (Test-Path $original)) {
    Write-Host "❌ ERRO: $original não encontrado" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $v2)) {
    Write-Host "❌ ERRO: $v2 não encontrado" -ForegroundColor Red
    exit 1
}

# Fazer backup
if (Test-Path $backup) {
    Write-Host "✓ Backup já existe em $backup" -ForegroundColor Yellow
} else {
    Copy-Item $original $backup -Force
    Write-Host "✓ Backup criado: $backup" -ForegroundColor Green
}

# Substituir original por v2
Copy-Item $v2 $original -Force
Write-Host "✓ $original substituído por versão v2" -ForegroundColor Green

# Verificar que está ativo
$content = Get-Content $original -Raw
if ($content -match "def montar_cartao_estendido") {
    Write-Host "✓ Verificado: nova função detectada em $original" -ForegroundColor Green
} else {
    Write-Host "❌ ERRO: Substituição falhou" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== STATUS ===" -ForegroundColor Green
Write-Host "✅ Hook v2 ATIVO" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos passos:"
Write-Host "1. Testar com ENGINE real: /engine"
Write-Host "2. Navegar pelas fases até DOC"
Write-Host "3. Validar que motor aparece no cartão"
Write-Host "4. Relatar: OK ou problemas"
Write-Host ""
Write-Host "Para reverter: Copy-Item $backup $original -Force"
