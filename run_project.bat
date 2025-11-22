@echo off
echo ========================================
echo E-commerce Sales Analysis Project
echo ========================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo.

echo Checking required libraries...
python -c "import pandas, matplotlib, seaborn, jupyter" 2>nul
if errorlevel 1 (
    echo Some libraries are missing. Installing...
    pip install pandas matplotlib seaborn jupyter
    if errorlevel 1 (
        echo ERROR: Failed to install libraries
        pause
        exit /b 1
    )
) else (
    echo All required libraries are installed!
)
echo.

echo Starting Jupyter Notebook...
echo.
echo The notebook will open in your default browser.
echo Press Ctrl+C in this window to stop the server when done.
echo.
jupyter notebook ecommerce_sales.ipynb
