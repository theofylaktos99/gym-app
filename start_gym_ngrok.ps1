# Gym App with Ngrok - PowerShell Script
# Author: GitHub Copilot
# Date: June 29, 2025

Write-Host "🏋️ Gym App with Ngrok - Starting..." -ForegroundColor Green
Write-Host ""

# Check if ngrok is installed
try {
    $ngrokVersion = ngrok version 2>$null
    if ($ngrokVersion) {
        Write-Host "✅ Ngrok found: $($ngrokVersion)" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Ngrok is not installed or not in PATH" -ForegroundColor Red
    Write-Host "📥 Please download ngrok from: https://ngrok.com/download" -ForegroundColor Yellow
    Write-Host "📂 Extract and add to PATH, or install via: choco install ngrok" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "✅ Python found: $($pythonVersion)" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "📥 Please install Python from: https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📦 Installing/Updating dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting Gym App with Ngrok..." -ForegroundColor Green
Write-Host "📱 The app will be accessible from anywhere once ngrok tunnel is created" -ForegroundColor Cyan
Write-Host "🔗 Look for the public URL in the output below" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the application
python gym_app.py

Read-Host "Press Enter to exit"
