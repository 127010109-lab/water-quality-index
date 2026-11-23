@echo off
echo ======================================================================
echo   Running AquaSafe CLI Test & Automated PDF Certificate Compilation
echo ======================================================================
echo.
cd /d "%~dp0"
python cli.py --generate_pdf --sample_id FIELD-DEMO-2026
echo.
pause
