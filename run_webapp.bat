@echo off
echo ========================================
echo E-commerce Sales Analysis Web App
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)
echo.

echo Checking required libraries...
python -c "import flask, pandas" 2>nul
if errorlevel 1 (
    echo Installing required libraries...
    pip install -r requirements_web.txt
)
echo.

echo Preparing data...
if not exist "powerbi_data" (
    echo Running data preparation...
    python prepare_powerbi_data.py
)
echo.

echo Starting Flask web server...
echo.
echo ========================================
echo Dashboard will open at:
echo http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
