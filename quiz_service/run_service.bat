@echo off
echo ========================================
echo    Quiz Service - LearnUp
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.11
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)

echo.
echo [3/4] Cleaning old database...
if exist data (
    rmdir /s /q data
    echo Old database removed.
)

echo.
echo [4/4] Starting Quiz Service...
echo.
echo Service will be available at: http://localhost:5004
echo Press Ctrl+C to stop the service
echo.
python app_simple.py

pause 