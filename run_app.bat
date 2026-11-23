@echo off
title AquaSafe
echo ======================================================================
echo   Launching AquaSafe Water Quality and Hydrochemical Decision Platform
echo ======================================================================
echo.
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.9+ from https://www.python.org/downloads/
  echo and tick "Add Python to PATH" during setup.
  pause
  exit /b 1
)
python -c "import streamlit, pandas, numpy, matplotlib, seaborn, reportlab" >nul 2>nul
if errorlevel 1 (
  echo Installing required packages - this is only needed the first time...
  python -m pip install -r requirements.txt
)
echo.
echo Opening http://localhost:8501  (press CTRL+C in this window to stop)
python -m streamlit run app.py
pause
