# FASE 3: Ativar engine_contexto_v3.py em produção (PowerShell)

$repo_dir = (Get-Item $PSScriptRoot).FullName
$hooks_dir = Join-Path $repo_dir "hooks"
$original = Join-Path $hooks_dir "engine_contexto.py"
$v3 = Join-Path $hooks_dir "engine_contexto_v3.py"
$backup = Join-Path $hooks_dir "engine_contexto.py.backup-fase2"

Write-Host "=== FASE 3: Ativar Hook V3 ===" -ForegroundColor Green
Write-Host "Repositório: $repo_dir"
Write-Host ""

# Verificar que arquivos existem
if (-not (Test-Path $original)) {
    Write-Host "❌ ERRO: $original não encontrado" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $v3)) {
    Write-Host "❌ ERRO: $v3 não encontrado" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $backup)) {
    Write-Host "❌ ERRO: $backup não encontrado (Fase 2 não foi executada?)" -ForegroundColor Red
    exit 1
}

# Fazer backup do v2
$backup_v2 = Join-Path $hooks_dir "engine_contexto.py.backup-fase2-v2"
Copy-Item $original $backup_v2 -Force
Write-Host "✓ Backup do V2 criado: $backup_v2" -ForegroundColor Green

# Substituir original por v3
Copy-Item $v3 $original -Force
Write-Host "✓ $original substituído por versão v3" -ForegroundColor Green

# Verificar que está ativo
$content = Get-Content $original -Raw
if ($content -match "def _analisar_e_sugerir_motor") {
    Write-Host "✓ Verificado: nova função detectada em $original" -ForegroundColor Green
} else {
    Write-Host "❌ ERRO: Substituição falhou" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== STATUS ===" -ForegroundColor Green
Write-Host "✅ Hook v3 ATIVO com sugestão automática de motor" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos passos:"
Write-Host "1. Rodar testes: python3 FASE3-AUTOMATE.py"
Write-Host "2. Testar com ENGINE real"
Write-Host "3. Validar que sugestão de motor aparece"
Write-Host "4. Relatar: OK ou problemas"
Write-Host ""
Write-Host "Para reverter: Copy-Item $backup_v2 $original -Force"
