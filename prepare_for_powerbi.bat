@echo off
echo ========================================
echo Power BI Data Preparation
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo Checking required libraries...
python -c "import pandas" 2>nul
if errorlevel 1 (
    echo Installing pandas...
    pip install pandas
)
echo.

echo Preparing data for Power BI...
echo.
python prepare_powerbi_data.py

echo.
echo ========================================
echo Process Complete!
echo ========================================
echo.
echo Your Power BI-ready files are in the 'powerbi_data' folder
echo.
pause
