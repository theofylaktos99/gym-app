@echo off
echo 🏋️ Gym App with Ngrok - Starting...
echo.

REM Check if ngrok is installed
where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Ngrok is not installed or not in PATH
    echo 📥 Please download ngrok from: https://ngrok.com/download
    echo 📂 Extract and add to PATH, or install via: choco install ngrok
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo 📥 Please install Python from: https://python.org
    pause
    exit /b 1
)

echo ✅ Ngrok found: 
ngrok version
echo.

echo ✅ Python found:
python --version
echo.

echo 📦 Installing/Updating dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🚀 Starting Gym App with Ngrok...
echo 📱 The app will be accessible from anywhere once ngrok tunnel is created
echo 🔗 Look for the public URL in the output below
echo.
echo ⏹️  Press Ctrl+C to stop the server
echo.

python gym_app.py

pause
