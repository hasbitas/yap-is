@echo off
REM YAP-IS — Windows single-process launcher
setlocal
set ROOT=%~dp0..
cd /d "%ROOT%\backend"

REM Use python or py, whichever is available
where python >nul 2>&1
if %ERRORLEVEL%==0 (
  set PYCMD=python
) else (
  where py >nul 2>&1
  if %ERRORLEVEL%==0 (
    set PYCMD=py
  ) else (
    echo ERROR: Python was not found. Install it from https://python.org/downloads
    pause
    exit /b 1
  )
)

echo [1/2] Installing dependencies...
%PYCMD% -m pip install -q -r requirements.txt
if errorlevel 1 (
  echo Dependency installation failed. Check your internet connection.
  pause
  exit /b 1
)

echo [2/2] Starting YAP-IS: http://127.0.0.1:8000/
start "" http://127.0.0.1:8000/
%PYCMD% main.py
endlocal
