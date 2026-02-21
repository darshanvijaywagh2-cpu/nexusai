# X AI Desktop Setup - Windows PowerShell
# Run as Administrator

Write-Host "🤖 Setting up X AI Desktop Agent..." -ForegroundColor Green

# Check if Python installed
Write-Host "`n📋 Checking Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Python not found. Install from python.org" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Python found" -ForegroundColor Green

# Install dependencies
Write-Host "`n📦 Installing Python packages..." -ForegroundColor Yellow
pip install requests fastapi uvicorn pillow >$null 2>&1
Write-Host "✅ Packages installed" -ForegroundColor Green

# Create folder
$folder = "$env:USERPROFILE\nexusai"
New-Item -ItemType Directory -Force -Path $folder | Out-Null

# Download files
Write-Host "`n📥 Downloading X AI..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/darshanvijaywagh2-cpu/nexusai/main/server/agent.py" -OutFile "$folder\agent.py" -UseBasicParsing
Write-Host "✅ Downloaded" -ForegroundColor Green

Write-Host "`n🎯 Setup Complete!" -ForegroundColor Green
Write-Host "`nTo connect to VPS, set VPS_URL environment variable:" -ForegroundColor Cyan
Write-Host '  $env:VPS_URL="https://your-tunnel-url.trycloudflare.com"' -ForegroundColor White
Write-Host "`nTo run:" -ForegroundColor Cyan
Write-Host "  cd $folder" -ForegroundColor White
Write-Host "  python agent.py" -ForegroundColor White
