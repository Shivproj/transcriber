@echo off

REM --- Configuration ---
SET APP_DIR="src"
REM Remove quotes from the command definitions themselves
SET FASTAPI_COMMAND=uvicorn backend_app:app --host 127.0.0.1 --port 7400 --reload
SET STREAMLIT_COMMAND=streamlit run frontend_app.py

REM --- Optional: Specify virtual environment paths (relative to script location) ---
REM --- Assuming .venv is in the same directory as this batch script ---
SET BACKEND_VENV_ACTIVATE=".venv\Scripts\activate.bat"
SET FRONTEND_VENV_ACTIVATE=".venv\Scripts\activate.bat"

REM --- Optional: Any commands to run BEFORE starting ---
echo Running pre-startup commands...
cd /D "%APP_DIR%"
echo Pre-startup commands finished.
cd /D "%~dp0"

echo Starting FastAPI server...
cd /D "%APP_DIR%"
IF EXIST "%~dp0%BACKEND_VENV_ACTIVATE%" (
    start "FastAPI" cmd /k call "%~dp0%BACKEND_VENV_ACTIVATE%" ^& %FASTAPI_COMMAND%
) ELSE (
    echo WARNING: Backend venv activation script not found at %~dp0%BACKEND_VENV_ACTIVATE%. Running without venv.
    start "FastAPI" cmd /k %FASTAPI_COMMAND%
)
timeout /t 2 /nobreak > nul
echo FastAPI server started.
cd /D "%~dp0"

echo Starting Streamlit frontend...
cd /D "%APP_DIR%"
IF EXIST "%~dp0%FRONTEND_VENV_ACTIVATE%" (
    start "Streamlit" cmd /k call "%~dp0%FRONTEND_VENV_ACTIVATE%" ^& %STREAMLIT_COMMAND%
) ELSE (
    echo WARNING: Frontend venv activation script not found at %~dp0%FRONTEND_VENV_ACTIVATE%. Running without venv.
    start "Streamlit" cmd /k %STREAMLIT_COMMAND%
)
echo Streamlit frontend started.
cd /D "%~dp0"

echo Press Ctrl+C in the FastAPI window or close both windows to stop...