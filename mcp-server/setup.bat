@echo off
echo ========================================
echo Vegan Fact Checker MCP Server Setup
echo ========================================
echo.

REM Check if .env exists
if exist .env (
    echo [OK] .env file found
) else (
    if exist .env.example (
        echo [ACTION NEEDED] Copying .env.example to .env
        copy .env.example .env
        echo.
        echo [IMPORTANT] Please edit .env and add your API keys!
        echo.
        pause
    ) else (
        echo [ERROR] .env.example not found!
        echo Please copy .env.example to this folder first.
        pause
        exit /b 1
    )
)

REM Check if venv exists
if exist venv (
    echo [OK] Virtual environment found
) else (
    echo [CREATING] Virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate venv and install requirements
echo.
echo [INSTALLING] Dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env and add your API keys
echo 2. Run: venv\Scripts\activate
echo 3. Run: python test_setup.py
echo.
pause