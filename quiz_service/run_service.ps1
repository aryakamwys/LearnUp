Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    Quiz Service - LearnUp" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found! Please install Python 3.11" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[2/4] Installing dependencies..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install dependencies!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Cleaning old database..." -ForegroundColor Yellow
if (Test-Path "data") {
    Remove-Item -Recurse -Force "data"
    Write-Host "Old database removed." -ForegroundColor Green
}

Write-Host ""
Write-Host "[4/4] Starting Quiz Service..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Service will be available at: http://localhost:5004" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the service" -ForegroundColor Yellow
Write-Host ""

python app_simple.py

Read-Host "Press Enter to exit" 